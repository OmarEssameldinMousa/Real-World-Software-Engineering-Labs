# tools/update-readme.py
import os
import re
import yaml
import sys
import json
from collections import Counter

# --- Configuration ---
LABS_DIR = 'labs'
README_FILE = 'README.md'
SOLUTIONS_FILE = 'solutions.json'
TABLE_START_MARKER = '<!-- LABS_TABLE_START -->'
TABLE_END_MARKER = '<!-- LABS_TABLE_END -->'
TEMPLATE_LAB_DIR = '_template-lab'

# --- Helper Functions ---
def get_seniority_span(level):
    colors = {
        "Entry Level": "#2ecc40", "Junior": "#3498db", "Mid Senior": "#f1c40f",
        "Senior": "#e67e22", "Lead": "#e74c3c",
    }
    color = colors.get(level, "#ffffff")
    return f'<span style="color:{color};">{level}</span>'

def get_all_solver_counts():
    """Counts all solvers for all labs from the central JSON file."""
    try:
        with open(SOLUTIONS_FILE, 'r', encoding='utf-8') as f:
            solutions = json.load(f)
        
        lab_slugs = [s['lab_slug'] for s in solutions if 'lab_slug' in s]
        return Counter(lab_slugs)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, assume no solvers yet.
        return Counter()

# --- Main Logic ---
def main():
    print("--- Starting README update process ---")
    
    solver_counts = get_all_solver_counts()
    labs_data = []

    for item in os.listdir(LABS_DIR):
        lab_path = os.path.join(LABS_DIR, item)
        if not os.path.isdir(lab_path) or item == TEMPLATE_LAB_DIR:
            continue
            
        yaml_path = os.path.join(lab_path, 'lab.yaml')
        if os.path.exists(yaml_path):
            print(f"Processing lab: {item}")
            try:
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    lab_meta = yaml.safe_load(f)
                
                lab_slug = os.path.basename(lab_path)
                labs_data.append({
                    'category': lab_meta.get('category', 'N/A'),
                    'subcategory': lab_meta.get('subcategory', 'N/A'),
                    'seniority': lab_meta.get('seniority', 'N/A'),
                    'name': lab_meta.get('name', 'N/A'),
                    'slug': lab_slug,
                    'description': lab_meta.get('description', 'No description.'),
                    'contributor_gh': lab_meta.get('contributor', {}).get('github_user', 'anonymous'),
                    'solver_count': solver_counts.get(lab_slug, 0),
                    'grading': lab_meta.get('grading', 'N/A')
                })
            except Exception as e:
                print(f"Error processing {lab_path}: {e}", file=sys.stderr)

    labs_data.sort(key=lambda x: (x['category'], x['name']))
    
    table_header = "| Lab Category | Subcategory | Seniority Level | Lab Name | Description | Grading | Contributor | # Solvers |\n"
    table_separator = "|---|---|---|---|---|---|---|---|\n"
    
    table_rows = []
    for lab in labs_data:
        seniority_html = get_seniority_span(lab['seniority'])
        lab_link = f"[{lab['name']}]({LABS_DIR}/{lab['slug']})"
        contributor_link = f"[@{lab['contributor_gh']}](https://github.com/{lab['contributor_gh']})"
        row = f"| {lab['category']} | {lab['subcategory']} | {seniority_html} | {lab_link} | {lab['description']} | {lab['grading']} | {contributor_link} | {lab['solver_count']} |"
        table_rows.append(row)
        
    new_table_content = table_header + table_separator + "\n".join(table_rows)

    try:
        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        pattern = re.compile(f"({re.escape(TABLE_START_MARKER)}).*?({re.escape(TABLE_END_MARKER)})", re.DOTALL)
        if not pattern.search(readme_content):
             print(f"Error: Could not find table markers in {README_FILE}.", file=sys.stderr)
             sys.exit(1)
        new_readme_content = pattern.sub(f"\\1\n{new_table_content}\n\\2", readme_content)

        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_readme_content)
        print("README.md has been updated successfully.")
    except FileNotFoundError:
        print(f"Error: {README_FILE} not found.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()