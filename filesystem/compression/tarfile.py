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
    Creates a tar archive at the specified destination path, compressing one or multiple files or directories provided in `fullpath_files`.

    ### Parameters:
    - **fullpath_files (str or list)**: The full path of a single file/directory or a list of files/directories to compress.
    - **destination (str)**: The destination path where the tar archive will be created.

    ### Returns:
    - **str**: A message indicating whether a single file/directory or a list of files/directories was compressed.

    ### Raises:
    - **FileNotFoundError**: If any of the specified files or directories do not exist.
    - **PermissionError**: If permission is denied for accessing the files or writing to the destination.
    - **ValueError**: If `fullpath_files` is neither a string nor a list.

    ### Examples:
    - Compresses a single file or directory into a tar archive.

    ```python
    create_tar("/path/to/file_or_directory", "/path/to/destination.tar")
    ```

    - Compresses multiple files or directories into a tar archive.

    ```python
    files_to_compress = ["/path/to/file1", "/path/to/file2", "/path/to/dir"]
    create_tar(files_to_compress, "/path/to/destination.tar")
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
    Extracts files from a tar archive to the specified destination directory. You can extract the entire archive or specify a list of files to extract.

    ### Parameters:
    - **tar_filename (str)**: The path of the tar archive to extract files from.
    - **destination (str)**: The directory where the files will be extracted.
    - **extraction_list (list, optional)**: A list of files or directories to extract. If empty, extracts all files. Defaults to an empty list.

    ### Returns:
    - **bool**: Returns `True` if extraction is successful, or `False` if a `KeyError` occurs.

    ### Raises:
    - **FileNotFoundError**: If the tar archive does not exist.
    - **KeyError**: If the specified file or directory is not found in the tar archive.
    - **Exception**: For any other errors that occur during the extraction process.

    ### Examples:
    - Extracts all files from a tar archive to the specified destination directory.

    ```python
    extract("/path/to/archive.tar", "/destination/directory")
    ```

    - Extracts specific files from a tar archive.

    ```python
    extract("/path/to/archive.tar", "/destination/directory", extraction_list=["file1.txt", "file2.txt"])
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
    Reads the contents of a tar archive and returns a list of the files within it.

    ### Parameters:
    - **tar_filename (str)**: The path of the tar archive to read.

    ### Returns:
    - **list**: A list of filenames contained in the tar archive.

    ### Raises:
    - **FileNotFoundError**: If the tar archive does not exist.
    - **Exception**: For any other errors that occur during the process.

    ### Examples:
    - Reads the contents of a tar archive.

    ```python
    read_tar_archive("/path/to/archive.tar")
    ```
    """
    try:
        with tarfile.open(tar_filename, "r") as tar_file:
            tar_contents_list = tar_file.getnames()
            return tar_contents_list
    except FileNotFoundError:
        return "[FileSystem Pro]: File Not Found"
    except Exception as e:
        return f"[FileSystem Pro]: An error occurred. Error: {e}"
