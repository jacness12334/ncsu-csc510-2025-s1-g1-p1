# **🎬 Contributing to Movie Munchers**

Welcome to the Movie Munchers open-source project\! We're excited that you're interested in helping us build the ultimate in-seat food ordering application.  
This repository is located at: **https://github.com/jacness12334/ncsu-csc510-2025-s1-g1-p1**  
These guidelines outline the steps and principles for contributing to the codebase, documentation, and community.

## **🤝 Code of Conduct**

By participating in this project, you are expected to uphold our Code of Conduct (if you have one). We strive to maintain an open and welcoming environment.

## **🚀 Getting Started**

Movie Munchers is a full-stack web application. Before contributing code, please ensure you have a working development environment set up locally, including installing all necessary dependencies for both the frontend and backend.

### **Project Stack**

* **Frontend:** React, Node.js, npm (using Next.js for routing).  
* **Backend:** Flask, SQL.

## **💡 Types of Contributions**

We appreciate all forms of help, though we primarily anticipate **Code, Bug Reports,** or **Design Suggestions**.

### **🐛 Bug Reports**

1. **Search** the existing issues to ensure the bug hasn't already been reported.  
2. **Open a new Issue**, clearly titled (e.g., "Bug: Checkout total is calculated incorrectly").  
3. Include detailed steps to reproduce the issue, what you expected to happen, and what actually happened.

### **✨ Feature Requests & Design Suggestions**

1. **Search** existing feature requests.  
2. **Open a new Issue** with the label enhancement.  
3. Describe the feature's goal and how it would benefit users (the "why"). If it's a design suggestion, include clear descriptions of the proposed changes.

### **💻 Code Contributions (Bug Fixes and Features)**

For direct changes to the code, please follow the **Pull Request Workflow** below.

## **🛠️ Code Contribution Workflow**

### **1\. Create a Branch**

Create a new branch for your work based on the primary branch. Use descriptive names (e.g., bugfix/issue-101, feature/new-menu-filter).

### **2\. Commit Your Changes**

### **3\. Sign Off on Your Work (DCO Requirement)**

**This is Mandatory.** To ensure legal clarity and confirm that you retain the IP while granting the necessary license, we use the **Developer Certificate of Origin (DCO)**.  
You must certify that you wrote the code or have the right to contribute it under the MIT License. To do this, simply add a signed-off line to your commit messages using the **\-s flag**:  
git commit \-s \-m "feat: Added user profile editing screen and DCO"

This adds the line Signed-off-by: Your Name \<your-email@example.com\>.

### **4\. Create a Pull Request (PR)**

1. Push your branch to your fork.  
2. Open a Pull Request from your fork's branch to the upstream main branch of Movie Munchers.  
3. Ensure your PR description clearly explains the changes.

### **5\. Review and Merge**

**All contributions require review by at least one of the 5 Core Team members before merging.**

* A Core Team member will review your code and may request changes.  
* Once approved and all tests pass, a Core Team member will merge your contribution.

## **📐 Style and Standards**

We require consistent formatting across the codebase. Please ensure all code passes these checks before submitting a PR.

### **Backend (Python/Flask)**

* **Formatting:** We use the **Black** code formatter to ensure all Python code adheres to a consistent style, primarily following **PEP 8**.  
* **Linting:** We use **Flake8** to catch style errors and potential bugs.

### **Frontend (React/Next.js)**

* **Formatting:** We use **Prettier** for automated code formatting.  
* **Linting:** We use **ESLint** to enforce JavaScript/React best practices.

### **Testing**

* Any new feature or substantial bug fix must include relevant unit and/or integration tests.  
* All existing tests must pass before a PR can be merged.

## **⚖️ Legal & Governance**

### **Intellectual Property (IP) and Licensing**

* **License:** Movie Munchers is distributed under the **MIT License**.  
* **Contributor IP:** **Contributors retain the Intellectual Property (IP) rights** to their original code contributions. By submitting a contribution with a **DCO signature**, you are confirming that your work is licensed under the MIT License and that you are authorized to submit it.

### **Project Governance (The Core Team)**

Movie Munchers is maintained and governed by the original 5 developers, who collectively form the **Core Team**.

* **Decision Making:** Decisions are made by **consensus among the 5 Core Team members**. Any one of the five members has the authority to review and approve code.  
* **PR Approval:** Only a Core Team member has the authority to approve and merge Pull Requests into the main branch.
