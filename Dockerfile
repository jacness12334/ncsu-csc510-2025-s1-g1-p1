# Dockerfile - Minimum structure for Python application deployment.
# Used for build and runtime environments, checked by Hadolint.
# NOTE: NOT USED FOR RELEASING AS THIS WAS DISALLOWED BY OUR PROJECT MANAGEMENT. THIS IS ONLY FOR GITHUB ACTIONS USE ONLY.

# Use a lean, official Python image for the final stage
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the setup file (or requirements.txt if you use one)
COPY setup.cfg .

# Install the dependencies required for the application.
# Hadolint will warn if you don't pin versions (DL3008), but we ignore that in .hadolint.yaml for flexibility.
RUN pip install .

# Copy the application source code
# Assuming the main code is in the 'proj1/' directory as per repository context
COPY proj1/ proj1/

# Expose the port your service runs on (e.g., if you have a web API)
# EXPOSE 8080

# Define the command to run the application (assuming a main module in proj1)
CMD ["python", "proj1/main.py"]
