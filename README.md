# 🛠️ Real-World Software Engineering Labs

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status"/>
  <img src="https://img.shields.io/badge/Contributions-Welcome-blue" alt="Contributions Welcome"/>
  <img src="https://img.shields.io/github/forks/OmarEssameldinMousa/Real-World-Software-Engineering-Labs?style=social" alt="GitHub forks"/>
  <img src="https://img.shields.io/github/stars/OmarEssameldinMousa/Real-World-Software-Engineering-Labs?style=social" alt="GitHub stars"/>
</p>

This repository offers a collection of hands-on labs designed to simulate real-world production issues. Sharpen your skills in debugging, refactoring, pipeline optimization, and performance tuning with challenges that mirror what you'd encounter in a professional software engineering environment.

Each lab is a self-contained environment, providing:

*   **A Detailed README:** A comprehensive description of the challenge, the scenario, and your objectives.
*   **A Containerized Application/Pipeline:** A reproducible environment using Docker to ensure consistency.
*   **A Validation Script:** A tool to verify if your solution successfully resolves the issue.
*   **A Solutions Folder:** A community-driven collection of different approaches to solving the lab.

---

## 🚀 How to Engage

There are two primary ways to interact with this repository: as a **Solver** or as a **Contributor**.

### 🔹 As a Solver

1. **Choose a Lab:** Browse the **Labs Index** section and pick a challenge that matches your interests or skill goals.
2. **Fork the Repository:** Click the "Fork" button at the top right of this page to create your own copy of the repository. This allows you to work independently and submit your changes.
3. **Set Up the Lab:** Clone your fork locally, navigate to the chosen lab's directory under `labs/<lab-name>/`, and follow the setup instructions in the lab's `README.md`. Use the provided scripts to start the environment and validate your work.
4. **Implement Your Fix:** Solve the challenge by making the necessary code changes, debugging, or optimizing as described in the lab instructions. Test your solution using the validation script provided.
5. **Submit Your Solution:** Add a JSON object describing your solution to the central `solutions/solutions.json` file. Include details such as your GitHub username, a brief summary of your approach, and a link to your solution write-up if available.
6. **Open a Pull Request:** Push your changes to your fork and open a Pull Request to the main repository. Your solution will be automatically validated, and upon approval, it will be added to our main [**Community Solutions**](SOLUTIONS.md) page.

For detailed, step-by-step instructions, please refer to our [**CONTRIBUTING.md**](CONTRIBUTING.md).

### 🔹 As a Contributor

1. **Create a New Lab:** Copy the `labs/_template-lab/` directory to `labs/<your-lab-name>/` to start a new lab.
2. **Develop the Challenge:** Write a clear problem description, set up the containerized application or pipeline, and provide a validation script to check solutions.
3. **Add Metadata:** Complete the `lab.yaml` file with all relevant details about your lab, such as category, level, and grading metrics.
4. **Open a Pull Request:** Submit your new lab via a Pull Request. Our continuous integration pipeline will automatically validate your lab, and once merged, it will appear in the **Labs Index** for others to solve.

For more information on contributing new labs, see the [**CONTRIBUTING.md**](CONTRIBUTING.md) guide.

---

## 🔬 Lab Categories & Levels

To help you find the right challenge, labs are categorized by software engineering majors, subcategories, and seniority levels.

<div style="display: flex; flex-wrap: wrap; gap: 2rem; align-items: flex-start;">

<div>

### 🧑‍💻 Lab Categories

| Category                        |
|----------------------------------|
| AI & Machine Learning           |
| Data Engineering                |
| Backend Engineering             |
| Frontend Engineering            |
| DevOps & Infrastructure         |
| Security Engineering            |
| Mobile Development              |
| Testing & QA                    |
| Performance Engineering         |
| Site Reliability Engineering    |
| Full Stack Engineering          |
| Cloud Engineering               |
| Embedded Systems                |
| Developer Productivity          |
| Observability & Monitoring      |

</div>

<div>

### 🏅 Seniority Levels

| Level        |
|--------------|
| <span style="color:#2ecc40;">Entry Level</span>  |
| <span style="color:#3498db;">Junior</span>       |
| <span style="color:#f1c40f;">Mid Senior</span>   |
| <span style="color:#e67e22;">Senior</span>       |
| <span style="color:#e74c3c;">Lead</span>         |

</div>

<div>

### 🧩 Lab Subcategories

| Subcategory         |
|---------------------|
| Debugging           |
| Refactoring         |
| Performance Tuning  |
| Pipelines           |
| Validation          |
| Monitoring          |
| Security Fixes      |
| Infrastructure      |
| Automation          |
| Testing             |
| Code Review         |
| CI/CD               |
| Scalability         |
| Reliability         |
| Documentation       |

</div>

<div>

### 🎯 Grading Metrics

| Metric         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| Custom         | The lab includes a unique, lab-specific grading or validation approach.     |
| Self Grading   | Participants validate their own solutions using provided scripts.          |
| Performance    | Solutions are evaluated based on measurable performance improvements.       |
| Timed          | Completion time is a factor in the evaluation.                            |

</div>
</div>

---

## 📑 Labs Index

<!-- LABS_TABLE_START -->
| Lab Category | Subcategory | Seniority Level | Lab Name | Description | Grading | Contributor | # Solvers |
|---|---|---|---|---|---|---|---|
| Data Engineering | Performance Tuning | <span style="color:#f1c40f;">Mid Senior</span> | [Streaming Delayed Join](labs/streaming-delayed-join) | Fix a streaming pipeline where a costly join introduces a 1-hour processing delay. Target: < 5 min latency. | timed | [@OmarEssameldinMousa](https://github.com/OmarEssameldinMousa) | 1 |
<!-- LABS_TABLE_END -->

---

## 🧭 Getting Started

To get started with a lab, navigate to its directory and use the provided scripts:

```bash
# Navigate to the lab's directory
cd labs/<lab-name>

# Start the lab environment
./scripts/run.sh

# Validate the lab (for authors and CI)
./scripts/validate.sh

# If available, run the local solution validator
./scripts/solution-validator.sh# Real-World-Software-Engineering-Labs
```# Real-World-Software-Engineering-Labs
# Real-World-Software-Engineering-Labs
