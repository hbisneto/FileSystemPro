"""
# Compression

---

## Overview
The Compression module is a component of the FileSystemPro library that provides functions for creating, extracting, and reading compressed archive files in tar and zip formats. 
It leverages Python's built-in `tarfile` and `zipfile` modules to handle compression and extraction efficiently, supporting single files, directories, or lists thereof.

## Features
- **Archive Creation:** Compresses single files/directories or lists into tar (.tar, .tar.gz, .tar.bz2) or zip (.zip) archives, preserving internal structure.
- **Archive Extraction:** Extracts all contents or specific files/directories from tar or zip archives to a destination directory.
- **Archive Reading:** Lists the contents of tar or zip archives, with optional filtering of system files (e.g., .DS_Store).
- **Error Handling:** Raises descriptive exceptions for common issues like missing files or permissions, ensuring robust operations.
- **Flexibility:** Supports compressed variants (e.g., gzip for tar) and partial extractions for targeted workflows.

## Detailed Functionality
The module's functions are grouped by archive type (tar and zip) for clarity, providing a unified interface while respecting format-specific behaviors.

### Tar Functions
- **`create_tar(fullpath_files, destination, compression='none')`**: Compresses files/directories into a tar archive, with optional gzip/bzip2 compression.
- **`extract_tar(tar_filename, destination, extraction_list=[])`**: Extracts from a tar archive (auto-detects compression like .tar.gz).
- **`read_tar(tar_filename)`**: Returns a list of files in the tar archive.

### Zip Functions
- **`create_zip(fullpath_files, destination)`**: Compresses files/directories into a zip archive (uses deflate by default).
- **`extract_zip(zip_path, destination, extraction_list=None)`**: Extracts from a zip archive, supporting None (all), list, or single file.
- **`read_zip(zip_filename, show_compression_system_files=True)`**: Returns a list of files, optionally excluding system artifacts.

## Usage
To use the functions provided by this module, 
import the module and call the desired function with the appropriate parameters:

```python
from filesystem import compression as comp
```
"""

import os
import tarfile as __tarfile__
import zipfile as __zipfile__
from filesystem import wrapper as wra

def create_tar(fullpath_files, destination, compression='none'):
    """
    # compression.create_tar(fullpath_files, destination, compression='none')

    ---

    ### Overview
    Creates a tar archive at the specified destination path, compressing one or multiple files or directories provided in `fullpath_files`.
    Preserves structure within each item, but roots list items separately (no common base for multi-local paths).
    Supports compression types: 'none' (plain .tar), 'gz' (.tar.gz), 'bz2' (.tar.bz2).

    ### Parameters:
    - **fullpath_files (str or list)**: The full path of a single file/directory or a list of files/directories to compress.
    - **destination (str)**: The destination path where the tar archive will be created (extension auto-appended if needed, e.g., .tar.gz).
    - **compression (str, optional)**: Compression type. Options: 'none' (default), 'gz', 'bz2'. Defaults to 'none'.

    ### Returns:
    - **dict**: Metadata of the created tar archive (from `wrapper.get_object`).

    ### Raises:
    - **FileNotFoundError**: If any of the specified files or directories do not exist.
    - **PermissionError**: If permission is denied for accessing the files or writing to the destination.
    - **ValueError**: If `fullpath_files` is neither a string nor a list, or invalid compression.

    ### Examples:
    - Creates a plain .tar.
    ```python
    result = create_tar("/path/to/file", "/path/to/archive.tar")
    print(result['size'])  # E.g., "1.2 MB"
    ```

    - Creates a .tar.gz (gzip-compressed).
    ```python
    result = create_tar("/path/to/file", "/path/to/archive.tar.gz", compression='gz')
    print(result['size'])  # Smaller due to compression
    ```

    - Compresses multiple files as .tar.bz2.
    ```python
    files_to_compress = ["/path/to/file1", "/path/to/file2"]
    result = create_tar(files_to_compress, "/path/to/archive.tar.bz2", compression='bz2')
    ```
    """
    mode_map = {'none': 'w', 'gz': 'w:gz', 'bz2': 'w:bz2'}
    if compression not in mode_map:
        raise ValueError(f"Invalid compression: '{compression}'. Options: 'none', 'gz', 'bz2'.")
    mode = mode_map[compression]

    if not destination.lower().endswith(('.tar', '.tar.gz', '.tar.bz2')):
        ext = '.tar' if compression == 'none' else f'.tar.{compression}'
        destination += ext

    def add_to_tar(tarf, path, base_path):
        """
        # compression.add_to_tar(tarf, path, base_path)

        ---

        ### Overview
        Helper function to add a file or directory (and its contents) to an open tar archive. 
        Uses relative paths from `base_path` to preserve structure. Only adds files (ignores empty directories).

        ### Parameters:
        - **tarf (tarfile.TarFile)**: An open tarfile object in write mode.
        - **path (str)**: The full path to the file or directory to add.
        - **base_path (str)**: The base path for computing relative paths in the archive.

        ### Returns:
        None

        ### Raises:
        - **FileNotFoundError**: If `path` does not exist.
        - **PermissionError**: If permission is denied accessing `path` or its contents.

        ### Examples:
        - Adding a single file:
        ```python
        with tarfile.open('archive.tar', 'w') as tarf:
            add_to_tar(tarf, '/path/to/file.txt', '/path/to')
        # Adds as 'file.txt' in archive
        ```

        - Adding a directory (adds all files recursively):
        ```python
        with tarfile.open('archive.tar', 'w') as tarf:
            add_to_tar(tarf, '/path/to/dir', '/path/to')
        # Adds files as 'dir/subfile.txt', etc.
        ```
        """
        if os.path.isfile(path):
            tarf.add(path, os.path.relpath(path, base_path))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    tarf.add(file_path, os.path.relpath(file_path, base_path))

    if isinstance(fullpath_files, str):
        if not os.path.exists(fullpath_files):
            raise FileNotFoundError(f"The file or directory '{fullpath_files}' does not exist.")
        with __tarfile__.open(destination, mode) as tarf:
            add_to_tar(tarf, fullpath_files, os.path.dirname(fullpath_files))
    
    elif isinstance(fullpath_files, list):
        for item in fullpath_files:
            if not os.path.exists(item):
                raise FileNotFoundError(f"The file or directory '{item}' does not exist.")
        with __tarfile__.open(destination, mode) as tarf:
            for item in fullpath_files:
                add_to_tar(tarf, item, os.path.dirname(item))
    else:
        raise ValueError("fullpath_files must be a string or a list.")

    return wra.get_object(destination)

def extract_tar(tar_filename, destination, extraction_list=[]):
    """
    # compression.extract_tar(tar_filename, destination, extraction_list=[])

    ---

    ### Overview
    Extracts files from a tar archive to the specified destination directory. You can extract the entire archive or specify a list of files to extract.
    Uses 'r:*' mode to auto-detect compression.
    Supports auto-detection of compressed formats like .tar.gz, .tar.bz2.

    ### Parameters:
    - **tar_filename (str)**: The path of the tar archive to extract files from.
    - **destination (str)**: The directory where the files will be extracted.
    - **extraction_list (list, optional)**: A list of files or directories to extract. If empty, extracts all files. Defaults to an empty list.

    ### Returns:
    - **dict**: Metadata of the destination directory after extraction (from `wrapper.get_object`).

    ### Raises:
    - **FileNotFoundError**: If the tar archive does not exist.
    - **KeyError**: If a specified file or directory is not found in the tar archive.
    - **PermissionError**: If permission is denied.
    - **Exception**: For any other errors during extraction.

    ### Examples:
    - Extracts all files from a tar archive to the specified destination directory.
    ```python
    result = extract_tar("/path/to/archive.tar", "/destination/directory")
    print(result['size'])  # Size of extracted dir
    ```

    - Extracts specific files from a tar archive.
    ```python
    extract_tar("/path/to/archive.tar", "/destination/directory", extraction_list=["file1.txt", "file2.txt"])
    ```
    """
    try:
        with __tarfile__.open(tar_filename, "r:*") as tar_file:
            if len(extraction_list) == 0:
                tar_file.extractall(destination)
            else:
                for item in extraction_list:
                    if item in tar_file.getnames():
                        tar_file.extract(item, destination)
                    else:
                        raise KeyError(f"The file or directory '{item}' is not found in the tar archive.")
    except FileNotFoundError:
        raise
    except KeyError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        raise Exception(f"An error occurred during extraction: {e}")

    return wra.get_object(destination)

def read_tar(tar_filename):
    """
    # compression.read_tar(tar_filename)

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
    contents = read_tar("/path/to/archive.tar")
    print(contents)  # ['file1.txt', 'dir/file2.txt']
    ```
    """
    try:
        with __tarfile__.open(tar_filename, "r") as tar_file:
            return tar_file.getnames()
    except FileNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"An error occurred while reading the tar archive: {e}")

def create_zip(fullpath_files, destination):
    """
    # compression.create_zip(fullpath_files, destination)

    ---

    ### Overview
    Creates a zip archive at the specified destination path, compressing one or multiple files or directories provided in `fullpath_files`.
    Preserves structure within each item, but roots list items separately (no common base for multi-local paths).

    ### Parameters:
    - **fullpath_files (str or list)**: The full path of a single file/directory or a list of files/directories to compress.
    - **destination (str)**: The destination path where the zip archive will be created.

    ### Returns:
    - **dict**: Metadata of the created zip archive (from `wrapper.get_object`).

    ### Raises:
    - **FileNotFoundError**: If any of the specified files or directories do not exist.
    - **PermissionError**: If the permission is denied for accessing the files or writing to the destination.
    - **ValueError**: If `fullpath_files` is neither a string nor a list.

    ### Examples:
    - Compresses a single file or directory into a zip archive.
    ```python
    result = create_zip("/path/to/file_or_directory", "/path/to/destination.zip")
    print(result['size'])  # E.g., "1.2 MB"
    ```

    - Compresses multiple files or directories into a zip archive.
    ```python
    files_to_compress = ["/path/to/file1", "/path/to/file2", "/path/to/dir"]
    result = create_zip(files_to_compress, "/path/to/destination.zip")
    print(result['abspath'])  # Full path to archive
    ```
    """
    def add_to_zip(zipf, path, base_path):
        """
        # compression.add_to_zip(zipf, path, base_path)

        ---

        ### Overview
        Helper function to add a file or directory (and its contents) to an open zip archive. 
        Uses relative paths from `base_path` to preserve structure. Only adds files (ignores empty directories).

        ### Parameters:
        - **zipf (zipfile.ZipFile)**: An open zipfile object in write mode.
        - **path (str)**: The full path to the file or directory to add.
        - **base_path (str)**: The base path for computing relative paths in the archive.

        ### Returns:
        None

        ### Raises:
        - **FileNotFoundError**: If `path` does not exist.
        - **PermissionError**: If permission is denied accessing `path` or its contents.

        ### Examples:
        - Adding a single file:
        ```python
        with zipfile.ZipFile('archive.zip', 'w') as zipf:
            add_to_zip(zipf, '/path/to/file.txt', '/path/to')
        # Adds as 'file.txt' in archive
        ```

        - Adding a directory (adds all files recursively):
        ```python
        with zipfile.ZipFile('archive.zip', 'w') as zipf:
            add_to_zip(zipf, '/path/to/dir', '/path/to')
        # Adds files as 'dir/subfile.txt', etc.
        ```
        """
        if os.path.isfile(path):
            zipf.write(path, os.path.relpath(path, base_path))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, base_path))

    if isinstance(fullpath_files, str):
        if not os.path.exists(fullpath_files):
            raise FileNotFoundError(f"The file or directory '{fullpath_files}' does not exist.")
        with __zipfile__.ZipFile(destination, 'w') as zipf:
            add_to_zip(zipf, fullpath_files, os.path.dirname(fullpath_files))
    
    elif isinstance(fullpath_files, list):
        for item in fullpath_files:
            if not os.path.exists(item):
                raise FileNotFoundError(f"The file or directory '{item}' does not exist.")
        with __zipfile__.ZipFile(destination, 'w') as zipf:
            for item in fullpath_files:
                add_to_zip(zipf, item, os.path.dirname(item))
    else:
        raise ValueError("fullpath_files must be a string or a list.")

    return wra.get_object(destination)

def extract_zip(zip_path, destination, extraction_list=None):
    """
    # compression.extract_zip(zip_path, destination, extraction_list=None)

    ---

    ### Overview
    Extracts files from a zip archive to the specified destination directory. You can extract the entire archive or specify a list of files to extract.

    ### Parameters:
    - **zip_path (str)**: The path of the zip archive from which to extract files.
    - **destination (str)**: The directory where the files will be extracted.
    - **extraction_list (None or list or str, optional)**: If `None`, extracts all files. If a list, extracts only the files specified in the list. If a string, extracts the file specified. Defaults to `None`.

    ### Returns:
    - **dict**: Metadata of the destination directory after extraction (from `wrapper.get_object`).

    ### Raises:
    - **FileNotFoundError**: If the zip archive does not exist.
    - **KeyError**: If a specified file is not found in the zip archive.
    - **PermissionError**: If permission is denied for reading the zip archive or writing to the destination.
    - **ValueError**: If `extraction_list` is not `None`, a list, or a string.
    - **RuntimeError**: For other zip-related errors.

    ### Examples:
    - Extracts all files from a zip archive to the specified destination directory.
    ```python
    result = extract_zip("/path/to/archive.zip", "/destination/directory")
    print(result['size'])  # Size of extracted dir
    ```

    - Extracts specific files from a zip archive.
    ```python
    extract_zip("/path/to/archive.zip", "/destination/directory", extraction_list=["file1.txt", "file2.txt"])
    ```

    - Extracts a single file from a zip archive.
    ```python
    extract_zip("/path/to/archive.zip", "/destination/directory", extraction_list="file1.txt")
    ```
    """
    os.makedirs(destination, exist_ok=True)
    try:
        with __zipfile__.ZipFile(zip_path, 'r') as zip_ref:
            if extraction_list is None:
                zip_ref.extractall(destination)
            elif isinstance(extraction_list, list):
                for item in extraction_list:
                    zip_ref.extract(item, destination)
            elif isinstance(extraction_list, str):
                zip_ref.extract(extraction_list, destination)
            else:
                raise ValueError("The parameter 'extraction_list' must be None, a list, or a string.")
    except KeyError as e:
        raise KeyError(f"File not found in zip: {e}")
    except RuntimeError as e:
        raise RuntimeError(f"Zip extraction error: {e}")
    except FileNotFoundError:
        raise
    except PermissionError:
        raise

    return wra.get_object(destination)

def read_zip(zip_filename, show_compression_system_files=True):
    """
    # compression.read_zip(zip_filename, show_compression_system_files=True)

    ---

    ### Overview
    Reads the contents of a zip archive and returns a list of the files within it. You can choose to include or exclude compression system files (e.g., `__MACOSX/`, `.DS_Store`, `Thumbs.db`).

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
    contents = read_zip("/path/to/archive.zip")
    print(contents)  # ['file1.txt', 'dir/file2.txt']
    ```

    - Reads the contents of a zip archive and excludes compression system files.
    ```python
    read_zip("/path/to/archive.zip", show_compression_system_files=False)
    ```
    """
    try:
        with __zipfile__.ZipFile(zip_filename, "r") as zip_file:
            all_contents_list = zip_file.namelist()
            zip_contents_list = []
            system_files = ['__MACOSX/', '.DS_Store', 'Thumbs.db']
            for i in all_contents_list:
                if show_compression_system_files or not any(sys in i for sys in system_files):
                    zip_contents_list.append(i)
            return zip_contents_list
    except FileNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"An error occurred while reading the zip archive: {e}")