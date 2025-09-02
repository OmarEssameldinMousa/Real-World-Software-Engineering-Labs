#!/bin/bash
# Starts the lab environment.

# Move to the script's directory to ensure docker-compose command works correctly
cd "$(dirname "$0")/.."

echo "--- Cleaning up any previous runs ---"
docker compose down -v --remove-orphans &>/dev/null

echo "--- Building Docker image and starting Kafka pipeline ---"
echo "This will take a moment..."
echo "To stop, press Ctrl+C."

# Build and run the services in the foreground
docker compose up --build
