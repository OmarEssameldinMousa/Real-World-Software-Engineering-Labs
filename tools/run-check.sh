#!/bin/bash
set -euo pipefail

if [ -z "$1" ]; then
  echo "Error: Lab name must be provided." >&2
  echo "Usage: $0 <lab-name>" >&2
  exit 1
fi

LAB_NAME="$1"
LAB_DIR="labs/$LAB_NAME"

validate_structure() {
  local lab_path="$1"
  local is_valid=true
  echo "--- Validating directory structure for '$LAB_NAME' ---"

  # Define all required files and directories (solutions dir removed)
  local required_paths=(
    "$lab_path/README.md"
    "$lab_path/lab.yaml"
    "$lab_path/docker-compose.yml"
    "$lab_path/app"
    "$lab_path/app/Dockerfile"
    "$lab_path/scripts"
    "$lab_path/scripts/run.sh"
    "$lab_path/scripts/validate.sh"
  )

  for path in "${required_paths[@]}"; do
    if [ ! -e "$path" ]; then
      echo "Error: Missing required file or directory: $path" >&2
      is_valid=false
    fi
  done

  if [ ! -f "$lab_path/scripts/solution-validator.sh" ]; then
    echo "Warning: Optional 'scripts/solution-validator.sh' not found."
  fi

  if [ "$is_valid" = true ]; then
    echo "Directory structure is valid."
    return 0
  else
    return 1
  fi
}

if [ ! -d "$LAB_DIR" ]; then
  echo "Error: Lab directory '$LAB_DIR' not found." >&2
  exit 1
fi

validate_structure "$LAB_DIR"

echo "--- Running lab-specific validation for: $LAB_NAME ---"
cd "$LAB_DIR" || exit 1
echo "Executing ./scripts/validate.sh from within $(pwd)"
chmod +x ./scripts/validate.sh

if ./scripts/validate.sh; then
  echo "--- Lab-specific validation for '$LAB_NAME' PASSED ---"
  exit 0
else
  echo "--- Lab-specific validation for '$LAB_NAME' FAILED ---" >&2
  exit 1
fi