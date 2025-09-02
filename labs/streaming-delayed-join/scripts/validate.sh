#!/bin/bash
# CI validation script.
# Performs a quick, non-interactive check to ensure the lab is well-formed.

# Move to the lab's root directory
cd "$(dirname "$0")/.."

echo "--- [CI] Running Lab Sanity Check ---"

# 1. Build the Docker images
echo "Step 1: Building Docker images..."
if ! docker compose build; then
    echo "Error: Docker build failed." >&2
    exit 1
fi
echo "✅ Docker build successful."

# 2. Briefly start and stop the services to check for configuration errors
echo "Step 2: Testing service startup..."
if ! docker compose up --no-start; then
    echo "Error: Docker compose configuration seems invalid." >&2
    exit 1
fi

# Bring up services in detached mode and then immediately shut them down
docker compose up -d
sleep 5 # Give them a moment to start
docker compose down

echo "✅ Service startup test successful."
echo "--- [CI] Sanity Check PASSED ---"

exit 0