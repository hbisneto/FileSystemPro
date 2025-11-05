# -*- coding: utf-8 -*-
#
# filesystem/wrapper/__init__.py
# FileSystemPro
#
# Created by Heitor Bisneto on 12/11/2025.
# Copyright © 2023–2025 hbisneto. All rights reserved.
#
# This file is part of FileSystemPro.
# FileSystemPro is free software: you can redistribute it and/or modify
# it under the terms of the MIT License. See LICENSE for more details.
#

"""
# Wrapper

---

## Overview
This module provides utility functions for retrieving structured metadata about files or directories at a given path, including absolute paths, timestamps (formatted as "YYYY/MM/DD HH:MM:SS:ff"), existence/type checks (file/dir/link), names/extensions, and sizes (formatted with units like bytes/KB/MB). It also includes a simple check for file extensions. All operations use standard library functions for cross-platform compatibility, with recursive size calculation for directories. Errors like non-existence or permissions are raised where applicable.

## Features
- **Metadata Retrieval:** Get a comprehensive dict with abspath, access/creation/modification dates (formatted strings), dirname, existence, is_dir/is_file/is_link, extension, name (with/without ext), and size (formatted string with units).
- **Extension Check:** Quickly verify if a path string has a file extension (works even for non-existent paths).
- **Timestamp Formatting:** Internal helpers format dates consistently; supports both files and directories.
- **Size Calculation:** For files: raw bytes formatted; for dirs: recursive total of all contained files.

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import wrapper
```

### Examples:

- Get full metadata for a file:

```python
details = wrapper.get_object("/path/to/file.txt")
print(details['name'])        # e.g., "file.txt"
print(details['size'])        # e.g., "1.2 KB"
print(details['modified'])    # e.g., "2023/11/04 12:34:56:123456"
print(details['is_file'])     # True
```

- Get metadata for a directory (recursive size):

```python
dir_details = wrapper.get_object("/path/to/directory")
print(dir_details['size'])    # e.g., "10.5 MB" (total of all files)
print(dir_details['is_dir'])  # True
```

- Check if a path has an extension:

```python
has_ext = wrapper.has_extension("/path/to/file.txt")  # True
no_ext = wrapper.has_extension("/path/to/file")       # False
print(has_ext, no_ext)
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
