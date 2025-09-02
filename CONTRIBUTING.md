# 🤝 Contributing to Real-World SE Labs

Thank you for your interest in contributing! This repository is built on automation, so following these guidelines precisely is essential for your pull request to be validated and merged.

We welcome two types of contributions: **Lab Authors** who create new challenges, and **Solvers** who submit their solutions.

---

## 1. Lab Authors: How to Add a New Lab

As a lab author, you are creating a new, self-contained challenge for the community. To ensure your submission is valid, you must adhere to the following rules.

### Pull Request Rules for Lab Authors

*   **One Lab Per Pull Request:** Your PR must only contain changes within a single new lab directory (e.g., `labs/your-new-lab/`).
*   **Trigger Path:** Your changes must be within the `labs/` directory to trigger the correct CI workflow.

### Required Files & Structure

Create a new directory at `labs/<your-lab-slug>/` that contains **all** of the following:

> 💡 **Quick Start:**  
> You can use the provided starter script [`tools/init_lab.sh`](tools/init_lab.sh) to scaffold a new lab directory with the correct structure and metadata.  
>  
> ```bash
> ./tools/init_lab.sh "Your Lab Name"
> ```
>  
> This will create a new lab folder under `labs/` with all required files, and update `lab.yaml` for you.

| Path                            | Description                                                                     | Required? |
| ------------------------------- | ------------------------------------------------------------------------------- | :-------: |
| `lab.yaml`                      | Metadata for the README index. See example below.                               |    ✅     |
| `README.md`                     | Detailed description, goals, and instructions for your lab.                     |    ✅     |
| `docker-compose.yml`            | The Docker Compose file to set up the lab environment.                          |    ✅     |
| `app/`                          | A directory containing your application's source code.                          |    ✅     |
| `app/Dockerfile`                | The Dockerfile for your application.                                            |    ✅     |
| `scripts/`                      | A directory for helper scripts.                                                 |    ✅     |
| `scripts/run.sh`                | A script to start the lab for the user.                                         |    ✅     |
| `scripts/validate.sh`           | A **non-interactive** script for the CI to perform a quick sanity check.        |    ✅     |
| `scripts/solution-validator.sh` | A script for solvers to check their work locally.                               | (Optional) |

#### Example `lab.yaml`
```yaml
name: "Streaming Delayed Join"
category: "Data Engineering"
subcategory: "Performance Tuning"
grading: "Performance" # Note: 'grading' not 'Grading'
seniority: "Mid Senior"
description: "Fix a streaming pipeline where a costly join introduces a 1-hour delay."
contributor:
  github_user: "YourGitHubUsername" # Note: Just the username
```

### The CI Validation Process for Labs

When you open a pull request to add a lab, our CI pipeline will automatically:
1.  **Validate Structure:** Check that your lab directory contains all required files.
2.  **Execute Validation Script:** Run your lab's `scripts/validate.sh` to ensure it's functional.
3.  **Update README:** If all checks pass, your PR can be merged. The automation will then add your lab to the index in the main `README.md`.

---

## 2. Solvers: How to Submit a Solution

Submitting a solution involves adding a single JSON object to a central file. The CI is strict to prevent syntax errors.

### Pull Request Rules for Solvers

*   **Modify ONLY `solutions/solutions.json`:** Your PR must only contain changes to this single file. Any other changes will trigger the wrong workflow and be rejected.
*   **Add Exactly One JSON Object:** Your change should be the addition of one object to the list in `solutions.json`.

### Steps to Submit a Solution

1.  **Fork the repository.**
2.  **Create a public write-up** of your solution (e.g., a blog post, a Gist, or a public GitHub repository).
3.  **Find the lab's slug.** This is the name of the lab's directory (e.g., `streaming-delayed-join`).
4.  **Edit `solutions/solutions.json`** and add a new JSON object to the list. **Place a comma** after the preceding object if necessary.

    **Strict Format:**
    ```json
    {
      "github_username": "your-github-username",
      "lab_slug": "the-lab-slug-you-solved",
      "solution_link": "https://link-to-your-writeup-or-repo"
    }
    ```
    *Example: Adding a new solution*
    ```diff
      },
    + {
    +   "github_username": "johndoe",
    +   "lab_slug": "streaming-delayed-join",
    +   "solution_link": "https://github.com/johndoe/my-solution"
    + }
    ]
    ```
5.  **Open a Pull Request** containing only that single-file change.

### The CI Validation Process for Solutions

When you open a PR to add a solution, the CI pipeline will:
1.  **Validate JSON:** Check that `solutions.json` is still a valid JSON file and that your entry has the correct fields (`github_username`, `lab_slug`, `solution_link`).
2.  **Render Markdown:** If valid, the automation will regenerate the main `SOLUTIONS.md` file to include your link.
3.  **Update Solver Count:** The automation will also update the **# Solvers** count for that lab in the main `README.md`.

If all checks pass, your PR can be merged.