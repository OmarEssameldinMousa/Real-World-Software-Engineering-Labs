# tools/render-solutions.py
import json
from collections import defaultdict
import sys

SOLUTIONS_JSON_FILE = 'solutions.json'
SOLUTIONS_MD_FILE = 'SOLUTIONS.md'
LABS_DIR = 'labs'

def main():
    print(f"--- Rendering {SOLUTIONS_MD_FILE} from {SOLUTIONS_JSON_FILE} ---")
    try:
        with open(SOLUTIONS_JSON_FILE, 'r', encoding='utf-8') as f:
            solutions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {SOLUTIONS_JSON_FILE}: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Group solutions by lab slug
    labs = defaultdict(list)
    for solution in solutions:
        lab_slug = solution.get('lab_slug')
        if lab_slug:
            labs[lab_slug].append(solution)
            
    # Sort labs by slug and solutions by username within each lab
    sorted_labs = sorted(labs.items())
    for _, solution_list in sorted_labs:
        solution_list.sort(key=lambda x: x['github_username'].lower())

    # Generate Markdown content
    md_content = ["# 🏆 Community Solutions\n"]
    md_content.append("This page is auto-generated from the `solutions/solutions.json` file. Please do not edit it directly.\n")

    for lab_slug, solution_list in sorted_labs:
        md_content.append(f"## [{lab_slug}](/{LABS_DIR}/{lab_slug})\n")
        for solution in solution_list:
            user = solution['github_username']
            link = solution['solution_link']
            md_content.append(f"- [@{user}](https://github.com/{user}): [Solution Link]({link})")
        md_content.append("") # Add a blank line for spacing

    # Write to the Markdown file
    try:
        with open(SOLUTIONS_MD_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
        print(f"Successfully generated {SOLUTIONS_MD_FILE}.")
    except IOError as e:
        print(f"Error writing to {SOLUTIONS_MD_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()