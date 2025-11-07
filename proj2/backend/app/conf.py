# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MovieMunchers'
copyright = '2025, Jacob Phillips, Aadya Maurya, Janelle Correia, Galav Sharma, Aarya Rajoju'
author = 'Jacob Phillips, Aadya Maurya, Janelle Correia, Galav Sharma, Aarya Rajoju'
release = 'v1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # MAKE SURE THIS IS PRESENT AND CORRECTLY SPELLED
    'sphinx.ext.autodoc',     

    # The rest of your extensions are also necessary:
    'sphinx.ext.napoleon',    
    'sphinx_autodoc_typehints'
]

templates_path = ['_templates']
exclude_patterns = []


# In conf.py
# Add external libraries that may fail to import during doc generation
autodoc_mock_imports = [
    "flask",
    "flask_sqlalchemy",
    "flasgger",
    # **CRITICAL FIX:** Mocking the base library
    "sqlalchemy",
    "sqlalchemy.orm", 
    # Add 'app' as it's an internal package dependency 
    # which you don't need to actually run during doc generation
    "app"
    # Add any other third-party libraries your services rely on
]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

import os
import sys
import pathlib

# ----------------------------------------------------------------------
# FIX: Explicitly add the project root (the directory CONTAINING 'backend')
# to the Python path. This allows the system to recognize 'backend' as a package.
# ----------------------------------------------------------------------

# The path to the 'source' directory:
source_dir = pathlib.Path(__file__).parent.resolve() 

# The path to the directory two levels up (the project root, containing 'backend'):
project_root = source_dir.parent.parent.resolve() 

print(f"\n--- DEBUG: sys.path insert path is: {project_root} ---")
import glob
print(f"--- DEBUG: Files in the insert path: {glob.glob(str(project_root) + '/*')} ---")

# The path to the 'source' directory:
source_dir = pathlib.Path(__file__).parent.resolve() 
# The path to the directory two levels up (the project root, containing 'backend'):
project_root = source_dir.parent.parent.resolve() 

# Correct path insertion (remove the os.path.abspath('../') line)
sys.path.insert(0, str(project_root)) 

# You may also need to insert the backend directory for internal imports
sys.path.insert(0, str(project_root / 'backend'))