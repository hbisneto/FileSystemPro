"""
# Wrapper

---

## Overview
Wrapper is an integral part of the FileSystemPro library, designed to provide detailed information about 
files and directories. 
It includes functions for retrieving metadata and checking file extensions.

## Features
- `Metadata Retrieval:` Gathers comprehensive metadata about a file or directory path.
- `Extension Check:` Determines whether a file has an extension.

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

## Usage
To use the functions provided by this module, 
import the module and call the desired function with the appropriate parameters:

```python
from filesystem import wrapper as wra
```

"""

import datetime
import os
from filesystem import file as fsfile
from filesystem import directory as dir

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
        
    def obj_get_size(path):
        """
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
        if os.path.isfile(path):
            size = os.path.getsize(path)
        else:
            size = sum(
                os.path.getsize(os.path.join(dirpath, filename)) 
                    for dirpath, dirnames, filenames in os.walk(path)
                        for filename in filenames
            )
        
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:3.1f} {unit}"
            size /= 1024.0

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
    result["modified"] = obj_modification_date(path)
    result["name"] = tail
    result["name_without_extension"] = tail.split('.')[0]
    result["size"] = obj_get_size(path)
    return result

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
