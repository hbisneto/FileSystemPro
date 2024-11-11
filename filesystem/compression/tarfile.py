"""
# TarFile

---

## Overview
This module provides functions to create, extract, and read tar archives. It is designed to handle both single files and directories, making it versatile for various file compression and extraction needs.

## Features
- **Create Tar Archives:** Compress single files or directories into a tar archive.
- **Extract Tar Archives:** Extract all or specific files from a tar archive.
- **Read Tar Archives:** List the contents of a tar archive.


## Usage
To use these functions, simply import the module and call the desired function with appropriate parameters:

```python
import os
import tarfile

# Example: Creating a tar archive
create_tar('/path/to/file_or_directory', '/path/to/destination.tar')

# Example: Extracting from a tar archive
extract('/path/to/archive.tar', '/path/to/destination')

# Example: Reading a tar archive
contents = read_tar_archive('/path/to/archive.tar')
print(contents)
```
"""

import os
import tarfile

def create_tar(fullpath_files, destination):
    """
    # compression.create_tar(fullpath_files, destination)

    ---

    ### Overview
    The `create_tar` function compresses files or directories into a TAR file.

    ### Parameters:
    - **fullpath_files (str or list)**: The path(s) to the file(s) or directory(ies) to be compressed. It can be a single string or a list of strings.
    - **destination (str)**: The path where the resulting TAR file will be saved.

    ### Function Details:
    1. **add_to_tar(tarf, path, base_path)**: A helper function that adds files to the TAR archive.
    - If `path` is a file, it writes the file to the TAR archive.
    - If `path` is a directory, it recursively adds all files in the directory to the TAR archive.

    2. **Main Function Logic**:
    - If `fullpath_files` is a string, it compresses the single file or directory specified by the string.
    - If `fullpath_files` is a list, it compresses each file or directory in the list.

    ### Returns:
    - A message indicating whether a single file/directory or a list of files/directories was compressed.

    ### Examples:
    - Compressing a single file or directory:
        ```python
        create_tar("/path/to/file_or_directory", "/path/to/destination.tar")
        ```

    - Compressing multiple files or directories:
        ```python
        create_tar(["/path/to/file1", "/path/to/directory2"], "/path/to/destination.tar")
        ```
    """
    def add_to_tar(tarf, path, base_path):
        if os.path.isfile(path):
            tarf.add(path, os.path.relpath(path, base_path))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    tarf.add(file_path, os.path.relpath(file_path, base_path))

    if isinstance(fullpath_files, str):
        with tarfile.open(destination, 'w') as tarf:
            add_to_tar(tarf, fullpath_files, os.path.dirname(fullpath_files))
        return "ONLY ONE FILE OR DIRECTORY WAS COMPRESSED"
    
    if isinstance(fullpath_files, list):
        with tarfile.open(destination, 'w') as tarf:
            for item in fullpath_files:
                add_to_tar(tarf, item, os.path.dirname(item))
        return "A LIST OF FILE OR DIRECTORY WAS COMPRESSED"

def extract(tar_filename, destination, extraction_list=[]):
    """
    # compression.extract(tar_filename, destination, extraction_list=[])

    ---

    ### Overview
    The `extract` function is designed to extract files from a tar archive. It can extract all files or a specified list of files from the archive.

    ### Parameters:
    - **tar_filename (str)**: The path to the tar file that needs to be extracted.
    - **destination (str)**: The directory where the extracted files will be saved.
    - **extraction_list (list, optional)**: A list of specific files or directories to extract from the tar file. If this list is empty, all files will be extracted.

    ### Function Details:
    1. **Opening the Tar File**:
        - The function attempts to open the tar file specified by `tar_filename` in read mode (`"r:*"`).

    2. **Extracting Files**:
        - If `extraction_list` is empty, the function extracts all files to the `destination` directory.
        - If `extraction_list` contains specific items, the function checks if each item exists in the tar file:
            - If the item exists, it extracts the item to the `destination`.
            - If the item does not exist, it checks for any files in the tar archive that start with the item's name and extracts those.

    3. **Error Handling**:
        - If the tar file is not found, the function returns a message indicating the file was not found.
        - If a specified item in `extraction_list` is not found, the function returns `False`.
        - For any other exceptions, the function returns a message with the error details.

    ### Returns:
    - **True**: If the extraction is successful.
    - **"[FileSystem Pro]: File Not Found"**: If the tar file is not found.
    - **False**: If a specified item in `extraction_list` is not found.
    - **Error Message**: If any other error occurs during extraction.

    ### Examples:
    - Extracting all files from a tar archive:
        ```python
        extract("archive.tar.gz", "/path/to/destination")
        ```

    - Extracting specific files from a tar archive:
        ```python
        extract("archive.tar.gz", "/path/to/destination", ["file1.txt", "dir2/"])
        ```
    """
    try:
        with tarfile.open(tar_filename, "r:*") as tar_file:
            if len(extraction_list) == 0:
                tar_file.extractall(destination)
                return True

            for item in extraction_list:
                if item in tar_file.getnames():
                    tar_file.extract(item, destination)
                else:
                    for i in tar_file.getnames():
                        if i.startswith(item):
                            tar_file.extract(i, destination)
            return True

    except FileNotFoundError:
        return "[FileSystem Pro]: File Not Found"
    except KeyError:
        return False
    except Exception as e:
        return f"[FileSystem Pro]: An error occurred.\nError: {e}"

def read_tar_archive(tar_filename):
    """
    # compression.read_tar_archive(tar_filename)

    ---

    ### Overview
    The `read_tar_archive` function reads the contents of a TAR archive file and returns a list of the names of the files contained within it.

    ### Parameters:
    - **tar_filename (str)**: The path to the TAR archive file to be read.

    ### Function Details:
    1. **Opening the TAR file**:
        - The function attempts to open the specified TAR file in read mode using `tarfile.open(tar_filename, "r")`.
        - If the file is successfully opened, it retrieves the names of all the files in the archive using `tar_file.getnames()` and returns this list.

    2. **Error Handling**:
        - If the specified TAR file is not found, the function catches the `FileNotFoundError` and returns the message `"[FileSystem Pro]: File Not Found"`.
        - If any other exception occurs, it catches the exception and returns a message indicating an error occurred, along with the error message.

    ### Returns:
    - A list of file names contained in the TAR archive if successful.
    - A string message indicating an error if the file is not found or another exception occurs.

    ### Examples:
    - Reading the contents of a TAR archive:
        ```python
        tar_contents = read_tar_archive("/path/to/archive.tar")
        print(tar_contents)
        ```

    This function is useful for quickly listing the contents of a TAR archive without extracting the files.
    """
    try:
        with tarfile.open(tar_filename, "r") as tar_file:
            tar_contents_list = tar_file.getnames()
            return tar_contents_list
    except FileNotFoundError:
        return "[FileSystem Pro]: File Not Found"
    except Exception as e:
        return f"[FileSystem Pro]: An error occurred. Error: {e}"
