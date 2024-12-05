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
    Creates a zip archive at the specified destination path, compressing one or multiple files or directories provided in `fullpath_files`.

    ### Parameters:
    - **fullpath_files (str or list)**: The full path of a single file/directory or a list of files/directories to compress.
    - **destination (str)**: The destination path where the zip archive will be created.

    ### Returns:
    - **str**: A message indicating whether a single file/directory or a list of files/directories was compressed.

    ### Raises:
    - **FileNotFoundError**: If any of the specified files or directories do not exist.
    - **PermissionError**: If the permission is denied for accessing the files or writing to the destination.
    - **ValueError**: If `fullpath_files` is neither a string nor a list.

    ### Examples:
    - Compresses a single file or directory into a zip archive.

    ```python
    create_zip("/path/to/file_or_directory", "/path/to/destination.zip")
    ```

    - Compresses multiple files or directories into a zip archive.

    ```python
    files_to_compress = ["/path/to/file1", "/path/to/file2", "/path/to/dir"]
    create_zip(files_to_compress, "/path/to/destination.zip")
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
    Extracts files from a zip archive to the specified destination directory. You can extract the entire archive or specify a list of files to extract.

    ### Parameters:
    - **zip_path (str)**: The path of the zip archive from which to extract files.
    - **destination (str)**: The directory where the files will be extracted.
    - **extraction_list (None or list or str, optional)**: If `None`, extracts all files. If a list, extracts only the files specified in the list. If a string, extracts the file specified. Defaults to `None`.

    ### Returns:
    - **None**

    ### Raises:
    - **FileNotFoundError**: If the zip archive does not exist.
    - **PermissionError**: If permission is denied for reading the zip archive or writing to the destination.
    - **ValueError**: If `extraction_list` is not `None`, a list, or a string.

    ### Examples:
    - Extracts all files from a zip archive to the specified destination directory.

    ```python
    extract("/path/to/archive.zip", "/destination/directory")
    ```

    - Extracts specific files from a zip archive.

    ```python
    extract("/path/to/archive.zip", "/destination/directory", extraction_list=["file1.txt", "file2.txt"])
    ```

    - Extracts a single file from a zip archive.

    ```python
    extract("/path/to/archive.zip", "/destination/directory", extraction_list="file1.txt")
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
    Reads the contents of a zip archive and returns a list of the files within it. You can choose to include or exclude compression system files (e.g., `__MACOSX/`, `.DS_Store`).

    ### Parameters:
    - **zip_filename (str)**: The path of the zip archive to read.
    - **show_compression_system_files (bool, optional)**: If `True`, includes compression system files in the list. Defaults to `True`.

    ### Returns:
    - **list**: A list of filenames contained in the zip archive.

    ### Raises:
    - **FileNotFoundError**: If the zip archive does not exist.
    - **Exception**: For any other errors that occur during the process.

    ### Examples:
    - Reads the contents of a zip archive and includes compression system files.

    ```python
    read_zip_archive("/path/to/archive.zip")
    ```

    - Reads the contents of a zip archive and excludes compression system files.

    ```python
    read_zip_archive("/path/to/archive.zip", show_compression_system_files=False)
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
