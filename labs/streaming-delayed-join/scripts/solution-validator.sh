#!/bin/bash
# A local validator for solvers to test their solution.
# It runs the pipeline, measures the consumer's execution time, and checks correctness.

# Strict mode
set -euo pipefail

# --- Configuration ---
TIME_TARGET_SECONDS=15
EXPECTED_RECORDS=1000
TIMEOUT_SECONDS=120

# --- Main Logic ---
cd "$(dirname "$0")/.." # Go to lab root directory

echo "--- Running Solution Validator ---"

# Cleanup any previous runs
echo "Cleaning up previous Docker containers..."
docker compose down -v --remove-orphans &>/dev/null || true

echo "Building and starting the pipeline..."
# Run in detached mode
docker compose up --build -d

# Wait for containers to be healthy
echo "Waiting for services to be ready..."
sleep 10

# Create a log file to capture all consumer output
LOG_FILE=$(mktemp)
echo "Capturing consumer logs to: $LOG_FILE"

echo "Waiting for the consumer to process $EXPECTED_RECORDS records..."

# --- FIXED LOG MONITORING ---
# Start streaming logs in the background using 'docker compose logs --follow'.
# This is more reliable than polling with '--since 0s'.
docker compose logs consumer --no-log-prefix --follow > "$LOG_FILE" 2>/dev/null &
LOG_PID=$!

# Ensure the background log process is always killed when the script exits
trap "kill $LOG_PID 2>/dev/null || true" EXIT

TIMEOUT_REACHED=true # Assume timeout until we confirm success
PROCESSED_COUNT=0

# Wait for the expected count or timeout by checking the log file size
for ((i=0; i<$TIMEOUT_SECONDS; i++)); do
    # Count enriched events in the captured log file
    PROCESSED_COUNT=$(grep -c 'Enriched Event:' "$LOG_FILE" || true)

    if [ "$PROCESSED_COUNT" -ge "$EXPECTED_RECORDS" ]; then
        TIMEOUT_REACHED=false
        break
    fi

    # Check if the consumer container has exited unexpectedly
    # If the container is not running, stop waiting.
    if ! docker ps -q --filter "name=consumer-1" | grep -q .; then
        echo "❌ Consumer container has exited prematurely."
        break
    fi

    sleep 1 # Wait for 1 second between checks
done

# Stop the background log capture process
kill $LOG_PID 2>/dev/null || true
trap - EXIT # Remove the trap since we've cleaned up manually
# --- END FIXED LOG MONITORING ---

# Get the actual processing time from the complete consumer logs
ELAPSED_TIME=$(grep "Processed.*events in" "$LOG_FILE" | tail -1 | sed 's/.*in \([0-9.]*\) seconds.*/\1/')

if [ "$TIMEOUT_REACHED" = true ]; then
    # Recalculate count one last time to be sure
    PROCESSED_COUNT=$(grep -c 'Enriched Event:' "$LOG_FILE" || true)
    echo "❌ TIMEOUT: Only processed $PROCESSED_COUNT/$EXPECTED_RECORDS records in $TIMEOUT_SECONDS seconds"
    echo "Consumer logs:"
    cat "$LOG_FILE"
fi

# --- Validation Checks ---
VALIDATION_PASSED=true

# Only run validation if we didn't time out
if [ "$TIMEOUT_REACHED" = false ]; then
    echo "--- Consumer finished processing in $ELAPSED_TIME seconds ---"

    # 1. Check Performance
    if [ $(echo "$ELAPSED_TIME <= $TIME_TARGET_SECONDS" | bc -l 2>/dev/null) -eq 1 ]; then
        echo "✅ SUCCESS: Consumer finished under the ${TIME_TARGET_SECONDS}-second target."
    else
        echo "❌ FAILURE: Consumer took too long ($ELAPSED_TIME seconds). Target is < $TIME_TARGET_SECONDS seconds."
        VALIDATION_PASSED=false
    fi

    # 2. Check Correctness (count check)
    if [ "$PROCESSED_COUNT" -eq "$EXPECTED_RECORDS" ]; then
        echo "✅ SUCCESS: Correct number of records processed ($PROCESSED_COUNT/$EXPECTED_RECORDS)."
    else
        echo "❌ FAILURE: Incorrect number of records processed. Expected $EXPECTED_RECORDS, got $PROCESSED_COUNT."
        VALIDATION_PASSED=false
    fi
else
    # If we timed out, the validation fails.
    VALIDATION_PASSED=false
fi

# --- Cleanup and Final Result ---
echo "Shutting down the pipeline..."
docker compose down -v --remove-orphans &>/dev/null || true
rm -f "$LOG_FILE"

if [ "$VALIDATION_PASSED" = true ]; then
    echo -e "\n--- 🎉 VALIDATION PASSED! ---"
    echo "Performance: ${ELAPSED_TIME}s (target: <${TIME_TARGET_SECONDS}s)"
    echo "Records: ${PROCESSED_COUNT}/${EXPECTED_RECORDS}"
    exit 0
else
    echo -e "\n--- 🚨 VALIDATION FAILED. Please review the errors above. ---"
    exit 1
fi