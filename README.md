# LexisUni-process

## Introduction

This script is designed to streamline the workflow for handling bulk downloads from LexisNexis Uni. When downloading large datasets, it's common to have multiple .zip files containing nested folders and metadata files.

This tool automates three tedious tasks:
- Extracting all files from multiple zip archives.
- Flattening the directory structure so all documents are stored directly in one aggregate folder
- Cleaning the dataset by automatically excluding or removing _doclist.PDF files, which are typically index files rather than primary source documents.

## How to use
### 1. Setup Your Folder
Ensure all your LexisNexis .zip files are in the same directory.
- Place the `unzip.py` script into this folder.
- The folder structure should look like this:
/your-project-folder
├── 1.zip
├── 2.zip
├── ...
└── unzip.py

### 2. Run the Script
- Open your Terminal (or Command Prompt).
- Navigate to your project folder:
```cd /path/to/your-project-folder```
- Execute the script using Python 3:
- python3 unzip.py

### 3. Output
The script will create a new folder. All primary documents will be moved there, and any internal sub-folders or _doclist files will be removed or ignored.
