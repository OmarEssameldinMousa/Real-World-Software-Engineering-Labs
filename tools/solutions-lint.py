# tools/solutions-lint.py
import json
import sys
import re

SOLUTIONS_FILE = 'solutions.json'
URL_PATTERN = re.compile(r'^https?://\S+$')

def main():
    print(f"--- Linting {SOLUTIONS_FILE} ---")
    try:
        with open(SOLUTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {SOLUTIONS_FILE}. Please fix syntax.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: {SOLUTIONS_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print(f"ERROR: The root of {SOLUTIONS_FILE} must be a list ( [...] ).", file=sys.stderr)
        sys.exit(1)

    lint_passed = True
    seen_entries = set()

    for i, entry in enumerate(data, 1):
        if not isinstance(entry, dict):
            print(f"ERROR: Entry #{i} is not a JSON object ( {{...}} ).", file=sys.stderr)
            lint_passed = False
            continue

        # Check for required keys
        required_keys = {"github_username", "lab_slug", "solution_link"}
        actual_keys = set(entry.keys())
        if actual_keys != required_keys:
            print(f"ERROR: Entry #{i} has incorrect keys.", file=sys.stderr)
            print(f"  > Expected: {required_keys}", file=sys.stderr)
            print(f"  > Found:    {actual_keys}", file=sys.stderr)
            lint_passed = False
            continue
        
        # Check value types and formats
        for key, value in entry.items():
            if not isinstance(value, str) or not value.strip():
                print(f"ERROR: Entry #{i}, key '{key}' must be a non-empty string.", file=sys.stderr)
                lint_passed = False
            
            if key == 'solution_link' and not URL_PATTERN.match(value):
                print(f"ERROR: Entry #{i}, 'solution_link' is not a valid URL: {value}", file=sys.stderr)
                lint_passed = False

        # Check for duplicates
        entry_tuple = (entry.get('github_username', ''), entry.get('lab_slug', ''))
        if entry_tuple in seen_entries:
            print(f"ERROR: Duplicate entry found for user '{entry_tuple[0]}' on lab '{entry_tuple[1]}'.", file=sys.stderr)
            lint_passed = False
        seen_entries.add(entry_tuple)

    if lint_passed:
        print(f"{SOLUTIONS_FILE} is valid.")
        sys.exit(0)
    else:
        print(f"\nLinting failed. Please check the errors above.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()