#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 "Lab Name"

Creates a new lab directory under the parent `labs/` folder by copying the contents
of the current `_template-lab` directory. It will update the new lab's `lab.yaml`
with the provided name and a slug derived from it.

Example:
  $0 "My Awesome Lab"

This will create: labs/my-awesome-lab/ with files copied from _template-lab/
EOF
  exit 2
}

if [ "$#" -lt 1 ]; then
  usage
fi

# Join all args to form the lab name so names with spaces work
LAB_NAME="$*"

# Create a slug: lowercase, replace non-alphanum sequences with '-', trim leading/trailing '-'
slug() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g'
}

SLUG=$(slug "$LAB_NAME")

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# When this script is in `tools/`, compute the repository root and the
# template folder at `labs/_template-lab` so the script works regardless
# of its location inside the repo.
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$REPO_ROOT/labs/_template-lab"
LABS_DIR="$REPO_ROOT/labs"
DEST_DIR="$LABS_DIR/$SLUG"

if [ -e "$DEST_DIR" ]; then
  echo "Error: destination already exists: $DEST_DIR"
  exit 1
fi

echo "Creating new lab '$LAB_NAME' -> $DEST_DIR"
mkdir -p "$DEST_DIR"

# Verify template exists
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "Error: template directory not found: $TEMPLATE_DIR"
  exit 1
fi

# Copy template files. Exclude any .git dirs and any initializer inside the
# template's scripts folder (if present).
rsync -a --exclude '.git' --exclude 'scripts/init_lab.sh' "$TEMPLATE_DIR/" "$DEST_DIR/"

# Update lab.yaml name and slug fields if the file exists
LAB_YAML="$DEST_DIR/lab.yaml"
if [ -f "$LAB_YAML" ]; then
  # Escape forward slashes and ampersands in the lab name for sed
  esc_name=$(printf '%s' "$LAB_NAME" | sed -e 's/[\/&]/\\&/g')
  # Replace lines that start with name: and slug:
  if grep -q '^name:' "$LAB_YAML"; then
    sed -E -i "s/^name:.*/name: \"$esc_name\"/" "$LAB_YAML"
  else
    # Prepend name at the top
    sed -i "1s;^;name: \"$esc_name\"\n;" "$LAB_YAML"
  fi
  if grep -q '^slug:' "$LAB_YAML"; then
    sed -E -i "s/^slug:.*/slug: \"$SLUG\"/" "$LAB_YAML"
  else
    sed -i "1s;^;slug: \"$SLUG\"\n;" "$LAB_YAML"
  fi
  echo "Updated $LAB_YAML with name and slug"
else
  echo "Warning: $LAB_YAML not found; skipping YAML update"
fi

echo "Done. New lab created at: $DEST_DIR"
echo "Next steps:"
echo "  cd $DEST_DIR"
echo "  git init && git add . && git commit -m 'chore: add new lab from template'"
