"""
# ZipFile

---

## Overview
This module provides functions to create, extract, and read zip archives. It is designed to handle both single files and directories, making it versatile for various file compression and extraction needs.

## Features
- **Create Zip Archives:** Compress single files or directories into a zip archive.
- **Extract Zip Archives:** Extract all or specific files from a zip archive.
- **Read Zip Archives:** List the contents of a zip archive.

## Usage
To use these functions, simply import the module and call the desired function with appropriate parameters:

```python
import os
import zipfile

# Example: Creating a zip archive
create_zip('/path/to/file_or_directory', '/path/to/destination.zip')

# Example: Extracting from a zip archive
extract('/path/to/archive.zip', '/path/to/destination')

# Example: Reading a zip archive
contents = read_zip_archive('/path/to/archive.zip')
print(contents)
```
"""

import os
import zipfile
from filesystem import wrapper as wra

def create_zip(fullpath_files, destination):
    """
    # compression.zipfile.create_zip(fullpath_files, destination)

    ---
    
    ### Overview
    The `create_zip` function compresses files or directories into a ZIP file.

    ### Parameters:
    - **fullpath_files (str or list)**: The path(s) to the file(s) or directory(ies) to be compressed. It can be a single string or a list of strings.
    - **destination (str)**: The path where the resulting ZIP file will be saved.

    ### Function Details:
    1. **add_to_zip(zipf, path, base_path)**: A helper function that adds files to the ZIP archive.
    - If `path` is a file, it writes the file to the ZIP archive.
    - If `path` is a directory, it recursively adds all files in the directory to the ZIP archive.

    2. **Main Function Logic**:
    - If `fullpath_files` is a string, it compresses the single file or directory specified by the string.
    - If `fullpath_files` is a list, it compresses each file or directory in the list.

    ### Returns:
    - A message indicating whether a single file/directory or a list of files/directories was compressed.

    ### Examples:
    - Compressing a single file or directory:
        ```python
        create_zip("/path/to/file_or_directory", "/path/to/destination.zip")
        ```

    - Compressing multiple files or directories:
        ```python
        create_zip(["/path/to/file1", "/path/to/directory2"], "/path/to/destination.zip")
        ```
    """
    def add_to_zip(zipf, path, base_path):
        if os.path.isfile(path):
            zipf.write(path, os.path.relpath(path, base_path))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, base_path))

    if isinstance(fullpath_files, str):
        with zipfile.ZipFile(destination, 'w') as zipf:
            add_to_zip(zipf, fullpath_files, os.path.dirname(fullpath_files))
        return "ONLY ONE FILE OR DIRECTORY WAS COMPRESSED"
    
    if isinstance(fullpath_files, list):
        with zipfile.ZipFile(destination, 'w') as zipf:
            for item in fullpath_files:
                add_to_zip(zipf, item, os.path.dirname(item))
        return "A LIST OF FILE OR DIRECTORY WAS COMPRESSED"
    
def extract(zip_path, destination, extraction_list=None):
    """
    # compression.zipfile.extract(zip_path, destination, extraction_list=None)

    ---
    
    ### Overview
    Reads the contents of a ZIP file and extracts files based on the provided parameters.

    ### Parameters:
    - **zip_filename (str)**: The path to the ZIP file to read.
    - **extraction_list (None, list, or str)**: Specifies which files to extract. If `None`, all files are extracted. If a list, only the files in the list are extracted. If a string, only the specified file is extracted.
    - **destination (str)**: The directory to extract files to. Defaults to the current directory.
    - **show_compression_system_files (bool)**: If `True`, includes system files in the extraction. Defaults to `True`.

    ### Raises:
    - **FileNotFoundError**: If the ZIP file does not exist.
    - **ValueError**: If `extraction_list` is not `None`, a list, or a string.
    - **Exception**: For any other errors that occur while reading the ZIP file.

    ### Examples:
    - Extracts all contents of a ZIP file to the current directory:
        ```python
        read_zip_archive("/path/to/zipfile.zip")
        ```

    - Extracts specific files from a ZIP file to a specified directory:
        ```python
        read_zip_archive("/path/to/zipfile.zip", extraction_list=["file1.txt", "file2.txt"], destination="/path/to/destination")
        ```

    - Extracts a single file from a ZIP file:
        ```python
        read_zip_archive("/path/to/zipfile.zip", extraction_list="file1.txt", destination="/path/to/destination")
        ```
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if extraction_list is None:
            zip_ref.extractall(destination)
        elif isinstance(extraction_list, list):
            for item in extraction_list:
                zip_ref.extract(item, destination)
        elif isinstance(extraction_list, str):
            zip_ref.extract(extraction_list, destination)
        else:
            raise ValueError("The parameter 'extraction_list' must be None, a list, or a string.")

def read_zip_archive(zip_filename, show_compression_system_files=True):
    """
    # compression.zipfile.read_zip_archive(zip_filename, show_compression_system_files=True)

    ---
    
    ### Overview
    Reads the contents of a ZIP file and returns a list of the names of the files contained within it.

    ### Parameters:
    zip_filename (str): The path to the ZIP file to read.

    ### Returns:
    list: A list of filenames contained in the ZIP file.

    ### Raises:
    - FileNotFoundError: If the ZIP file does not exist.
    - Exception: For any other errors that occur while reading the ZIP file.

    ### Examples:
    - Reads the contents of a ZIP file and returns the list of filenames.

    ```python
    list_contents("/path/to/zipfile.zip")
    ```
    """
    try:
        with zipfile.ZipFile(zip_filename, "r") as zip_file:
            zip_contents_list = []
            all_contents_list = zip_file.namelist()
            for i in all_contents_list:
                if show_compression_system_files == True:
                    zip_contents_list.append(i)
                else:
                    if "__MACOSX/" not in i:
                        if ".DS_Store" not in i:
                            zip_contents_list.append(i)
            return zip_contents_list
    except FileNotFoundError:
        return "[FileSystem Pro]: File Not Found"
    except Exception as e:
        return f"[FileSystem Pro]: An error occurred. Error: {e}"
