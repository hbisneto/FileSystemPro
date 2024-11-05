"""
# Wrapper

---

## Overview
Wrapper is an integral part of the FileSystemPro library, designed to provide detailed information about 
files and directories. 
It includes functions for retrieving metadata, checking file extensions, and creating zip archives.

## Features
- `Metadata Retrieval:` Gathers comprehensive metadata about a file or directory path.
- `Extension Check:` Determines whether a file has an extension.
- `Zip Archive Creation:` Packages a directory or file into a zip archive.

## Detailed Functionality
The module's functions are crafted to offer detailed insights into the file system and to perform common 
file operations with ease.

### Metadata Retrieval (`get_object`)
The `get_object` function is the centerpiece of this module. 
It returns a dictionary containing various properties of the given path, such as absolute path, 
access time, creation time, directory name, existence, file type, link status, extension, modification time, 
file name, size, and more.

### Extension Check (`has_extension`)
The `has_extension` function checks if a given file path has an extension, 
which is useful for file type validation or processing logic that depends on file types.

### Zip Archive Creation (`make_zip`)
The `make_zip` function creates a zip archive from the specified source directory or file and 
saves it to the given destination. 
It is a convenient way to compress and package files for storage or transfer.

## Usage
To use the functions provided by this module, 
import the module and call the desired function with the appropriate parameters:

```python
from filesystem import wrapper as wra
```

"""

import datetime
import os
import shutil
from filesystem import file as fsfile
from filesystem import directory as dir

### INSERT INTO FILE MODULE
def find_duplicates(path):
    """
    # wrapper.find_duplicates(path)
    
    ---

    ### Overview
    Finds duplicate files in a given directory and its subdirectories.
    A file is considered a duplicate if it has the same checksum as another file.

    ### Parameters:
    path (str): The directory path to search for duplicate files.

    ### Returns:
    A tuple of two lists:
    - The first list contains the paths of the original files.
    - The second list contains the paths of the duplicate files.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Finds duplicate files in a specific directory.

    ```python
    find_duplicates("/path/to/directory")
    ```
    """
    checksums = {}
    original_files = []
    duplicate_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = dir.join(root, file)
            checksum = fsfile.calculate_checksum(file_path)
            if checksum in checksums:
                original_files.append(checksums[checksum])
                duplicate_files.append(file_path)
            else:
                checksums[checksum] = file_path
    return original_files, duplicate_files

def get_object(path):
    """
    # wrapper.get_object(path)

    ---

    ### Overview
    Retrieves various details about the file or directory at the specified path. These details include 
    the absolute path, access date, creation date, directory name, existence, type (file, directory, 
    or link), extension, modification date, name, name without extension, and size.

    ### Parameters:
    path (str): The file or directory path to retrieve details of.

    ### Returns:
    dict: A dictionary with the following keys:
    - "abspath": The absolute path.
    - "access": The last access time, or -1 if an error occurs.
    - "created": The creation time, or -1 if an error occurs.
    - "dirname": The directory name.
    - "exists": A boolean indicating whether the path exists.
    - "is_dir": A boolean indicating whether the path is a directory.
    - "is_file": A boolean indicating whether the path is a file.
    - "is_link": A boolean indicating whether the path is a symbolic link.
    - "extension": The file extension, or an empty string if the path is not a file.
    - "ext": The file extension, or an empty string if the path is not a file. `Kept for version support.`
    - "modified": The last modification time, or -1 if an error occurs.
    - "name": The base name of the path.
    - "name_without_extension": The base name of the path without the extension.
    - "size": The size of the file, or -1 if an error occurs.

    ### Raises:
    - FileNotFoundError: If the file or directory does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Retrieves details of a file.

    ```python
    get_object("/path/to/file")
    ```
    - Retrieves details of a directory.

    ```python
    get_object("/path/to/directory")
    ```
    """
    def obj_creation_date(path):
        """
        ### Overview
        Retrieves the creation date of the file or directory at the specified path.

        ### Parameters:
        path (str): The file or directory path to retrieve the creation date of.

        ### Returns:
        str: A string representing the creation date of the file or directory, formatted as "YYYY/MM/DD HH:MM:SS:ff".

        ### Raises:
        - FileNotFoundError: If the file or directory does not exist.
        - PermissionError: If the permission is denied.

        ### Examples:
        - Retrieves the creation date of a file.

        ```python
        obj_creation_date("/path/to/file")
        ```
        - Retrieves the creation date of a directory.

        ```python
        obj_creation_date("/path/to/directory")
        ```
        """
        timestamp = os.path.getctime(path)
        creation_date = datetime.datetime.fromtimestamp(timestamp)
        formatted_date = creation_date.strftime("%Y/%m/%d %H:%M:%S:%f")
        return formatted_date
    
    def obj_modification_date(path):
        """
        ### Overview
        Retrieves the last modification date of the file or directory at the specified path.

        ### Parameters:
        path (str): The file or directory path to retrieve the modification date of.

        ### Returns:
        str: A string representing the last modification date of the file or directory, formatted as "YYYY/MM/DD HH:MM:SS:ff".

        ### Raises:
        - FileNotFoundError: If the file or directory does not exist.
        - PermissionError: If the permission is denied.

        ### Examples:
        - Retrieves the last modification date of a file.

        ```python
        obj_modification_date("/path/to/file")
        ```
        - Retrieves the last modification date of a directory.

        ```python
        obj_modification_date("/path/to/directory")
        ```
        """
        timestamp = os.path.getmtime(path)
        modification_date = datetime.datetime.fromtimestamp(timestamp)
        formatted_date = modification_date.strftime("%Y/%m/%d %H:%M:%S:%f")
        return formatted_date
    
    def obj_last_access_date(path):
        """
        ### Overview
        Retrieves the last access date of the file or directory at the specified path.

        ### Parameters:
        path (str): The file or directory path to retrieve the last access date of.

        ### Returns:
        str: A string representing the last access date of the file or directory, formatted as "YYYY/MM/DD HH:MM:SS:ff".

        ### Raises:
        - FileNotFoundError: If the file or directory does not exist.
        - PermissionError: If the permission is denied.

        ### Examples:
        - Retrieves the last access date of a file.

        ```python
        obj_last_access_date("/path/to/file")
        ```
        - Retrieves the last access date of a directory.

        ```python
        obj_last_access_date("/path/to/directory")
        ```
        """
        timestamp = os.path.getatime(path)
        access_date = datetime.datetime.fromtimestamp(timestamp)
        formatted_date = access_date.strftime("%Y/%m/%d %H:%M:%S:%f")
        return formatted_date
        
    head, tail = os.path.split(path)

    result = {}
    result["abspath"] = os.path.abspath(path)
    result["access"] = obj_last_access_date(path)
    result["created"] = obj_creation_date(path)
    result["dirname"] = os.path.dirname(path)
    result["exists"] = os.path.exists(path)
    result["is_dir"] = os.path.isdir(path)
    result["is_file"] = os.path.isfile(path)
    result["is_link"] = os.path.islink(path)
    result["extension"] = tail.split(".")[-1] if result["is_file"] else ""
    ### EXT kept to cover version support. Remove on (MAJOR UPDATE ONLY)
    result["ext"] = tail.split(".")[-1] if result["is_file"] else ""
    result["modified"] = obj_modification_date(path)
    result["name"] = tail
    result["name_without_extension"] = tail.split('.')[0]
    result["size"] = get_size(path)
    return result

### CREATE METHOD INSIDE FILE AND DIRECTORY
def get_size(file_path):
    """
    # wrapper.get_size(path)

    ---

    ### Overview
    Calculates the size of the file or directory at the specified path. If the path is a directory, 
    it calculates the total size of all files in the directory. The size is returned in bytes, KB, 
    MB, GB, or TB, depending on the size.

    ### Parameters:
    path (str): The file or directory path to calculate the size of.

    ### Returns:
    str: A string representing the size of the file or directory, formatted as a float followed by 
    the unit of measurement.

    ### Raises:
    - FileNotFoundError: If the file or directory does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Calculates the size of a file.

    ```python
    get_size("/path/to/file")
    ```
    - Calculates the total size of all files in a directory.

    ```python
    get_size("/path/to/directory")
    ```
    """
    if os.path.isfile(file_path):
        size = os.path.getsize(file_path)
    else:
        size = sum(
            os.path.getsize(os.path.join(dirpath, filename)) 
                for dirpath, dirnames, filenames in os.walk(file_path)
                    for filename in filenames
        )
    
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0

def has_extension(file_path):
    """
    # wrapper.has_extension(file_path)

    --- 

    ### Overview
    Checks if the given file path has an extension. This function can return True or False based on the string, even if the file or directory does not exist.

    ### Parameters:
    file_path (str): The file path to check for an extension.

    ### Returns:
    bool: True if the file path has an extension, False otherwise.

    ### Examples:
    - Checks if the file path has an extension.

    ```python
    has_extension("/path/to/file.txt")
    ```
    This will return True because the file has an extension (.txt).

    - Checks if the file path has an extension.

    ```python
    has_extension("/path/to/file")
    ```
    This will return False because the file does not have an extension.
    """
    return os.path.splitext(file_path)[1] != ''

def make_zip(source, destination):
    """
    # wrapper.make_zip(source, destination)

    ---

    ### Overview
    Creates a zip archive of the specified source directory or file and moves it to the specified destination.

    ### Parameters:
    source (str): The path of the directory or file to archive.

    destination (str): The path where the archive will be moved to.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the source file or directory does not exist.
    - PermissionError: If the permission is denied.
    - shutil.SameFileError: If source and destination are the same file.

    ### Examples:
    - Creates a zip archive of a directory and moves it to a destination.

    ```python
    make_zip("/path/to/directory", "/path/to/directory.zip")
    ```
    - Creates a zip archive of a file and moves it to a destination.

    ```python
    make_zip("/path/to/file.txt", "/path/to/file.zip")
    ```
    """
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format), destination)
