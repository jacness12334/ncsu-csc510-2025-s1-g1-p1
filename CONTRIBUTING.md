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

### 🎯 Future Feature Suggestions (High Priority)

Based on core team feedback, these are high-impact features we would like to implement to enhance user experience and operational efficiency:

Predictive Ordering (Machine Learning Integration): Develop an ML model (using Python and Flask) that can analyze movie genre, run time, and showtime to suggest specific snack combinations to the user before they even start browsing. This feature will improve conversion rates and streamline the user's ordering process by anticipating their preferences.

Inventory Waste Prevention Forecasting: Build a dedicated backend module to forecast concession demand based on historical sales data, weather, and current show schedules. This forecasting model will allow theaters to optimize inventory procurement, significantly reducing food waste and lowering operational costs.

Food Bank Surplus Integration: Create a simple administrative dashboard and API endpoint that allows theater staff to log end-of-night surplus concession inventory that is still safe for donation. This system would integrate with local food bank partners via email or API, facilitating timely pickups and minimizing waste impact.

In-Seat Feedback & Rating System: Implement a client-side rating mechanism in the React frontend that allows customers to quickly provide feedback on food quality or delivery experience post-purchase. This data should be captured and stored in the SQL database to provide theater management with continuous, actionable quality control metrics.

Real-time Order Status Tracker: Enhance the user interface with a real-time order status bar (e.g., "Confirmed" -> "Preparing" -> "Delivering" -> "Delivered") powered by a persistent connection (e.g., WebSockets or long polling) handled by the Flask backend. This dramatically improves customer experience by reducing anxiety and providing transparency after the order is placed.

### 💡 Tips for Extending Movie Munchers Robustly

1. Extending the SQL Database Schema

When adding a new table (e.g., promotions) or a column to an existing table, first design the migration script carefully. Never directly modify the production database structure; define the schema changes in an Alembic or equivalent migration file to ensure atomic, reversible updates. Before running the migration, always check that the Flask-SQLAlchemy models reflect the new schema fields and that default values or NOT NULL constraints are handled gracefully.

2. Adding New Flask API Endpoints

To introduce a new endpoint (e.g., /api/order-history), ensure it is protected by appropriate authentication and authorization checks immediately upon entry, especially if it handles user-specific data. Structure the view function to strictly separate the business logic (which should reside in service modules) from the HTTP request/response handling. Always use Flask's built-in JSON utilities to serialize responses, and validate incoming data using a library like Marshmallow to prevent unexpected data types or security vulnerabilities.

3. Creating New React Components

When developing a new component (e.g., a SeatPicker component), prioritize component reusability and separation of concerns by keeping local state to a minimum. Use props to pass data and callbacks from its parent component, following a one-way data flow to maintain predictability. Ensure the component is fully responsive by utilizing Tailwind's utility classes and breakpoints, making it look great on both mobile ordering screens and desktop views.

4. Implementing Complex State Logic in React

For managing application-wide state (like the shopping cart or user session), avoid prop-drilling by leveraging a centralized solution like React Context or a dedicated state management library like Redux/Zustand. When updating complex objects in state (like adding items to the cart array), always use the immutable update pattern by creating a new array or object instead of directly mutating the existing state object. This prevents hard-to-debug side effects and ensures components re-render correctly.

5. Managing Environment Variables

If adding new external services (like a payment gateway key or a new email provider URL), never hardcode sensitive credentials directly into the codebase, even in development files. Use environment variables defined in a .env file for local development and ensure your CI/CD pipeline securely injects them into the Flask backend and the Next.js frontend build process. Access keys on the client-side (frontend) should only be for non-sensitive public IDs; true secrets must remain server-side.
