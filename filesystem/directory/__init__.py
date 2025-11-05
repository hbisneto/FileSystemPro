# -*- coding: utf-8 -*-
#
# filesystem/directory/__init__.py
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
# Directory

---

## Overview
This module provides comprehensive utilities for directory management, including creation, deletion, enumeration, path manipulation, timestamp handling (creation, access, write times in local/UTC formats), symbolic links, temporary directories, and size calculations. It supports recursive operations, pattern matching via glob, and cross-platform compatibility. Functions return iterators/lists for enumeration and metadata via `wrapper.get_object` where applicable. Global `current_directory` tracks the working directory, updated by `set_current_directory`.

## Features
- **Path Operations:** Combine/join paths (with absolute checks), get parent/name, resolve links.
- **Creation & Deletion:** Create dirs (with subdirs), temp subdirs, symbolic links; delete (recursive).
- **Enumeration:** List files/directories/entries with patterns ("TopDirectoryOnly" or "AllDirectories").
- **Existence & Size:** Check existence, compute recursive total size (bytes or formatted units).
- **Timestamps:** Get/set creation/access/write times (local/UTC, as datetime or str; Unix approximations).
- **Movement & Rename:** Move dirs/files (with root/content options, overwrite), rename dirs.
- **Tree Visualization:** Generate a tree-like string representation, ignoring common dev dirs (e.g., .git).
- **Current Dir Management:** Get/set working directory with global tracking.

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import directory
```

### Examples:

- Create a directory with subdirs and get metadata:

```python
result = directory.create("/path/to/new_directory")
print(result['abspath'])  # Full path
print(result['size'])     # "0.0 bytes" for empty dir
```

- Enumerate files recursively with pattern:

```python
files = directory.get_files("/path/to/directory", "*.txt", "AllDirectories")
for file_path in files:
    print(file_path)
```

- Get directory size formatted:

```python
size = directory.get_size("/path/to/directory", show_unit=True)
print(size)  # e.g., "2.5 GB"
```

- Move directory contents (not root) with overwrite:

```python
result = directory.move("/source/dir", "/dest/dir", move_root=False, overwrite=True)
print(result['size'])  # Size of destination
```

- Generate directory tree:

```python
lines = directory.get_tree("/path/to/project")
for line in lines:
    print(line)
    # Outputs tree like: 
    ├── file.txt
    └── subdir
        └── nested.py
```

- Set and get current directory:

```python
directory.set_current_directory("/path/to/work")
print(directory.get_current_directory())  # /path/to/work
```

- Get last write time and set it:

```python
write_time = directory.get_last_write_time("/path/to/directory")
print(write_time)  # datetime object
directory.set_last_write_time("/path/to/directory", "2023-01-01 12:00:00")
```
"""

import datetime
import glob
import os
import shutil
import tempfile
from filesystem import wrapper as wra

current_directory = os.getcwd()
"""
Global variable tracking the current working directory (updated by set_current_directory).
"""

def combine(*args, paths=[]):
    """
    # directory.combine(*args, paths=[])

    ---

    ### Overview
    Combines a list of paths or arguments into a single path. If the first argument or the first element in the paths list is not an absolute path, it raises a ValueError.
    If both `*args` and `paths` are provided, `paths` has priority and `*args` is ignored.

    ### Parameters:
    *args (str): The paths to combine. The first argument must be an absolute path.
    paths (list): A list of paths to combine. The first element in the list must be an absolute path. Defaults to an empty list.

    ### Returns:
    str: The combined path.

    ### Raises:
    - ValueError: If the first path is not absolute.

    ### Examples:
    - Combines all paths in the list, starting with an absolute path.
    ```python
    combine(paths=["/home/user/directory", "subdirectory", "file.txt"])
    ```
    - Combines all arguments, starting with an absolute path.
    ```python
    combine("/home/user/directory", "subdirectory", "file.txt")
    ```
    """
    if paths:
        path_list = paths
    else:
        path_list = list(args)
    if not path_list:
        return ""
    first = path_list[0]
    if not os.path.isabs(first):
        raise ValueError(
            f'Invalid argument: The path "{first}" is not an absolute path.\n'
            f'- The first path must be absolute.\n'
            f'For example, "/home/user/directory" is valid.'
        )
    rel_paths = []
    for p in path_list[1:]:
        if os.path.isabs(p):
            rel_paths = [p]
        else:
            rel_paths.append(p)
    return os.path.join(first, *rel_paths).rstrip(os.sep)

def create(path, create_subdirs=True):
    """
    # directory.create(path, create_subdirs=True)

    ---

    ### Overview
    Creates a directory at the specified path. If `create_subdirs` is True, all intermediate-level 
    directories needed to contain the leaf directory will be created (ignores if exists). 
    If False, raises if intermediates missing or leaf exists. Returns details via `wrapper.get_object`.

    ### Parameters:
    path (str): The directory path to create.
    create_subdirs (bool): A flag that indicates whether to create intermediate subdirectories. 
    Defaults to True.

    ### Returns:
    dict: Details of the created directory (from `wrapper.get_object`; includes "abspath", "size" as str, times as str, etc.).

    ### Raises:
    - FileExistsError: If the leaf directory already exists when `create_subdirs` is False.
    - PermissionError: If the permission is denied.
    - FileNotFoundError: If intermediates missing and `create_subdirs` is False.

    ### Examples:
    - Creates all intermediate subdirectories if they don't exist and returns their details.
    ```python
    create("/path/to/directory")
    ```
    - Creates only the leaf directory, raises an error if any intermediate directory doesn't exist, 
    and returns the details of the created directory.
    ```python
    create("/path/to/directory", False)
    ```
    """
    if not os.path.isdir(path):
        if create_subdirs:
            os.makedirs(path, exist_ok=True)
        else:
            os.mkdir(path)
    return wra.get_object(path)

def create_symbolic_link(path_target, path_link):
    """
    # directory.create_symbolic_link(path_target, path_link)

    ---

    ### Overview
    Creates a directory symbolic link at `path_link` pointing to `path_target`.

    ### Parameters:
    path_target (str): The target directory the symbolic link points to.
    path_link (str): The path where the symbolic link will be created.

    ### Returns:
    dict: A dictionary containing details about the created symbolic link (from `wrapper.get_object`; "is_link": True).

    ### Raises:
    - FileExistsError: If the link already exists.
    - FileNotFoundError: If the target path does not exist.
    - ValueError: If target is not a directory.
    - OSError: If the operation is not supported or permission is denied.
    - PermissionError: If permission is denied when accessing the target or creating the link.

    ### Examples:
    - Creates a symbolic link to a directory.
    ```python
    create_symbolic_link("/path/to/target", "/path/to/link")
    ```
    """
    if not os.path.exists(path_target):
        raise FileNotFoundError(f"The target path '{path_target}' does not exist.")
    if not os.path.isdir(path_target):
        raise ValueError(f"Target '{path_target}' must be a directory.")
    os.symlink(path_target, path_link)
    return wra.get_object(path_link)

def create_temp_subdirectory(prefix=""):
    """
    # directory.create_temp_subdirectory(prefix="")

    ---

    ### Overview
    Creates a uniquely named, empty directory in the system's temporary directory with an optional prefix.

    ### Parameters:
    prefix (str, optional): A prefix for the temporary directory name. Defaults to an empty string.

    ### Returns:
    str: The path of the created temporary directory.

    ### Examples:
    - Creates a temporary directory.

    ```python
    create_temp_subdirectory()
    ```
    - Creates a temporary directory with a prefix.

    ```python
    create_temp_subdirectory("myapp_")
    ```
    """
    return tempfile.mkdtemp(prefix=prefix)

def delete(path, recursive=False):
    """
    # directory.delete(path, recursive=False)

    ---

    ### Overview
    Deletes a directory at the specified path. If `recursive` is True, the directory and all its contents will be removed.

    ### Parameters:
    path (str): The directory path to delete.
    recursive (bool): A flag that indicates whether to delete the directory even if it is not empty. Defaults to False.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - OSError: If the directory is not empty and `recursive` is False, or permission denied.

    ### Examples:
    - Deletes an empty directory.
    ```python
    delete("/path/to/directory")
    ```
    - Deletes a directory and all its contents.
    ```python
    delete("/path/to/directory", True)
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f'The directory "{path}" does not exist.')
    if os.listdir(path) and not recursive:
        raise OSError(f'The directory "{path}" is not empty. Use recursive=True.')
    shutil.rmtree(path)

def enumerate_directories(path, search_pattern="*", search_option="TopDirectoryOnly"):
    """
    # directory.enumerate_directories(path, search_pattern="*", search_option="TopDirectoryOnly")

    ---

    ### Overview
    Returns an iterator of directory full names that match a search pattern in a specified path, with optional recursion.

    ### Parameters:
    path (str): The directory path to enumerate.
    search_pattern (str, optional): The search pattern (e.g., "*.txt"). Defaults to "*".
    search_option (str, optional): "TopDirectoryOnly" or "AllDirectories" to control recursion. Defaults to "TopDirectoryOnly".

    ### Returns:
    iterator: An iterator of directory full paths.

    ### Raises:
    - FileNotFoundError: If the path does not exist or is not a directory.
    - PermissionError: If permission is denied.

    ### Examples:
    - Enumerates all directories in a path.
    ```python
    for dir_path in enumerate_directories("/path/to/directory"):
        print(dir_path)
    ```
    - Enumerates directories matching a pattern recursively.
    ```python
    for dir_path in enumerate_directories("/path/to/directory", "*.test", "AllDirectories"):
        print(dir_path)
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The path '{path}' must be a directory.")
    if search_option == "AllDirectories":
        for root, dirs, _ in os.walk(path):
            for d in dirs:
                if glob.fnmatch.fnmatch(d, search_pattern):
                    yield os.path.join(root, d)
    else:
        for entry in os.scandir(path):
            if entry.is_dir() and glob.fnmatch.fnmatch(entry.name, search_pattern):
                yield entry.path

def enumerate_files(path, search_pattern="*", search_option="TopDirectoryOnly"):
    """
    # directory.enumerate_files(path, search_pattern="*", search_option="TopDirectoryOnly")

    ---

    ### Overview
    Returns an iterator of file full names that match a search pattern in a specified path, with optional recursion.

    ### Parameters:
    path (str): The directory path to enumerate.
    search_pattern (str, optional): The search pattern (e.g., "*.txt"). Defaults to "*".
    search_option (str, optional): "TopDirectoryOnly" or "AllDirectories" to control recursion. Defaults to "TopDirectoryOnly".

    ### Returns:
    iterator: An iterator of file full paths.

    ### Raises:
    - FileNotFoundError: If the path does not exist or is not a directory.
    - PermissionError: If permission is denied.

    ### Examples:
    - Enumerates all files in a path.
    ```python
    for file_path in enumerate_files("/path/to/directory"):
        print(file_path)
    ```
    - Enumerates files matching a pattern recursively.
    ```python
    for file_path in enumerate_files("/path/to/directory", "*.txt", "AllDirectories"):
        print(file_path)
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The path '{path}' must be a directory.")
    if search_option == "AllDirectories":
        for root, _, files in os.walk(path):
            for f in files:
                if glob.fnmatch.fnmatch(f, search_pattern):
                    yield os.path.join(root, f)
    else:
        for entry in os.scandir(path):
            if entry.is_file() and glob.fnmatch.fnmatch(entry.name, search_pattern):
                yield entry.path

def exists(path):
    """
    # directory.exists(path)

    ---

    ### Overview
    Checks if a directory exists at the specified path.

    ### Parameters:
    path (str): The directory path to check.

    ### Returns:
    bool: True if the directory exists, False otherwise.

    ### Examples:
    - Checks if a directory exists.

    ```python
    exists("/path/to/directory")
    ```
    """
    return os.path.isdir(path)

def get_creation_time(path):
    """
    # directory.get_creation_time(path)

    ---

    ### Overview
    Gets the creation date and time of a directory. Note: On Unix, this returns the change time (not true creation time).

    ### Parameters:
    path (str): The directory path.

    ### Returns:
    datetime: The creation date and time of the directory.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets the creation time of a directory.
    ```python
    get_creation_time("/path/to/directory")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.fromtimestamp(os.path.getctime(path))

def get_creation_time_utc(path):
    """
    # directory.get_creation_time_utc(path)

    ---

    ### Overview
    Gets the creation date and time, in Coordinated Universal Time (UTC) format, of a directory. Note: On Unix, this returns the change time (not true creation time).

    ### Parameters:
    path (str): The directory path.

    ### Returns:
    datetime: The creation date and time in UTC.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets the UTC creation time of a directory.
    ```python
    get_creation_time_utc("/path/to/directory")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.utcfromtimestamp(os.path.getctime(path))

def get_current_directory():
    """
    # directory.get_current_directory()

    ---

    ### Overview
    Retrieves the current working directory (reflects the last `set_current_directory` call).

    ### Parameters:
    None.

    ### Returns:
    str: The path of the current working directory.

    ### Raises:
    None.

    ### Examples:
    ```python
    from filesystem import directory as dir
    dir.set_current_directory("/path/to/directory")
    print(dir.get_current_directory())  # Outputs: /path/to/directory
    ```
    """
    global current_directory
    return current_directory

def get_directories(path, search_pattern="*", search_option="TopDirectoryOnly"):
    """
    # directory.get_directories(path, search_pattern="*", search_option="TopDirectoryOnly")

    ---

    ### Overview
    Returns the names of subdirectories that match the specified search pattern and search option in the specified directory.

    ### Parameters:
    path (str): The directory path to search.
    search_pattern (str, optional): The search pattern (e.g., "*.test"). Defaults to "*".
    search_option (str, optional): "TopDirectoryOnly" or "AllDirectories" to control recursion. Defaults to "TopDirectoryOnly".

    ### Returns:
    list: A list of directory full paths.

    ### Raises:
    - FileNotFoundError: If the path does not exist or is not a directory.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets all subdirectories in a path.
    ```python
    get_directories("/path/to/directory")
    ```
    - Gets subdirectories matching a pattern recursively.
    ```python
    get_directories("/path/to/directory", "*.test", "AllDirectories")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The path '{path}' must be a directory.")
    result = []
    if search_option == "AllDirectories":
        for root, dirs, _ in os.walk(path):
            for d in dirs:
                if glob.fnmatch.fnmatch(d, search_pattern):
                    result.append(os.path.join(root, d))
    else:
        for entry in os.scandir(path):
            if entry.is_dir() and glob.fnmatch.fnmatch(entry.name, search_pattern):
                result.append(entry.path)
    return result

def get_files(path, search_pattern="*", search_option="TopDirectoryOnly"):
    """
    # directory.get_files(path, search_pattern="*", search_option="TopDirectoryOnly")

    ---

    ### Overview
    Returns the names of files that match the specified search pattern and search option in the specified directory.

    ### Parameters:
    path (str): The directory path to search.
    search_pattern (str, optional): The search pattern (e.g., "*.txt"). Defaults to "*".
    search_option (str, optional): "TopDirectoryOnly" or "AllDirectories" to control recursion. Defaults to "TopDirectoryOnly".

    ### Returns:
    list: A list of file full paths.

    ### Raises:
    - FileNotFoundError: If the path does not exist or is not a directory.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets all files in a path.
    ```python
    get_files("/path/to/directory")
    ```
    - Gets files matching a pattern recursively.
    ```python
    get_files("/path/to/directory", "*.txt", "AllDirectories")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The path '{path}' must be a directory.")
    result = []
    if search_option == "AllDirectories":
        for root, _, files in os.walk(path):
            for f in files:
                if glob.fnmatch.fnmatch(f, search_pattern):
                    result.append(os.path.join(root, f))
    else:
        for entry in os.scandir(path):
            if entry.is_file() and glob.fnmatch.fnmatch(entry.name, search_pattern):
                result.append(entry.path)
    return result

def get_filesystem_entries(path, search_pattern="*", search_option="TopDirectoryOnly"):
    """
    # directory.get_filesystem_entries(path, search_pattern="*", search_option="TopDirectoryOnly")

    ---

    ### Overview
    Returns an array of file and directory names that match a search pattern and search option in a specified path.

    ### Parameters:
    path (str): The directory path to search.
    search_pattern (str, optional): The search pattern (e.g., "*.txt"). Defaults to "*".
    search_option (str, optional): "TopDirectoryOnly" or "AllDirectories" to control recursion. Defaults to "TopDirectoryOnly".

    ### Returns:
    list: A list of file and directory full paths.

    ### Raises:
    - FileNotFoundError: If the path does not exist or is not a directory.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets all entries in a path.
    ```python
    get_filesystem_entries("/path/to/directory")
    ```
    - Gets entries matching a pattern recursively.
    ```python
    get_filesystem_entries("/path/to/directory", "*.txt", "AllDirectories")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The path '{path}' must be a directory.")
    result = []
    if search_option == "AllDirectories":
        for root, dirs, files in os.walk(path):
            for d in dirs:
                if glob.fnmatch.fnmatch(d, search_pattern):
                    result.append(os.path.join(root, d))
            for f in files:
                if glob.fnmatch.fnmatch(f, search_pattern):
                    result.append(os.path.join(root, f))
    else:
        for entry in os.scandir(path):
            if glob.fnmatch.fnmatch(entry.name, search_pattern):
                result.append(entry.path)
    return result

def get_last_access_time(path):
    """
    # directory.get_last_access_time(path)

    ---

    ### Overview
    Returns the date and time the specified directory was last accessed.

    ### Parameters:
    path (str): The directory path.

    ### Returns:
    datetime: The last access date and time of the directory.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets the last access time of a directory.
    ```python
    get_last_access_time("/path/to/directory")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.fromtimestamp(os.path.getatime(path))

def get_last_access_time_utc(path):
    """
    # directory.get_last_access_time_utc(path)

    ---

    ### Overview
    Returns the date and time, in Coordinated Universal Time (UTC) format, that the specified directory was last accessed.

    ### Parameters:
    path (str): The directory path.

    ### Returns:
    datetime: The last access date and time in UTC.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets the UTC last access time of a directory.
    ```python
    get_last_access_time_utc("/path/to/directory")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.utcfromtimestamp(os.path.getatime(path))

def get_last_write_time(path):
    """
    # directory.get_last_write_time(path)

    ---

    ### Overview
    Returns the date and time the specified directory was last written to.

    ### Parameters:
    path (str): The directory path.

    ### Returns:
    datetime: The last write date and time of the directory.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets the last write time of a directory.
    ```python
    get_last_write_time("/path/to/directory")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.fromtimestamp(os.path.getmtime(path))

def get_last_write_time_utc(path):
    """
    # directory.get_last_write_time_utc(path)

    ---

    ### Overview
    Returns the date and time, in Coordinated Universal Time (UTC) format, that the specified directory was last written to.

    ### Parameters:
    path (str): The directory path.

    ### Returns:
    datetime: The last write date and time in UTC.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Gets the UTC last write time of a directory.
    ```python
    get_last_write_time_utc("/path/to/directory")
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.utcfromtimestamp(os.path.getmtime(path))

def get_name(path):
    """
    # directory.get_name(path)

    ---

    ### Overview
    Retrieves the name of the directory of the specified path. 
    If the path has an extension, it is assumed to be a file, and the parent directory name is returned. 
    If the path does not have an extension, it is assumed to be a directory, 
    and the directory name is returned. Works even if path does not exist (assumes dir if not file).

    ### Parameters:
    path (str): The directory or file path from which to retrieve the name.

    ### Returns:
    str: The name of the parent directory or the file.

    ### Examples:
    - Retrieves the parent directory name when the path is a file.
    ```python
    get_name("/path/to/directory/file.txt")
    ```
    - Retrieves the directory name when the path is a directory.
    ```python
    get_name("/path/to/directory")
    ```
    """
    if os.path.isfile(path):
        return get_parent_name(path)
    else:
        normalized = os.path.normpath(path.rstrip('/'))
        return os.path.basename(normalized)

def get_parent(path):
    """
    # directory.get_parent(path)
    
    ---

    ### Overview
    Retrieves the parent directory from the specified path.

    ### Parameters:
    path (str): The directory path from which to retrieve the parent directory.

    ### Returns:
    str: The parent directory of the specified path.

    ### Examples:
    - Retrieves the parent directory when the path ends with a slash.
    ```python
    get_parent("/path/to/directory/")
    ```
    - Retrieves the parent directory when the path does not end with a slash.
    ```python
    get_parent("/path/to/directory")
    ```
    """
    return os.path.dirname(path)

def get_parent_name(path):
    """
    # directory.get_parent_name(path)

    ---

    ### Overview
    Retrieves the parent directory name from the specified path.

    ### Parameters:
    path (str): The directory path from which to retrieve the parent directory name.

    ### Returns:
    str: The name of the parent directory.

    ### Examples:
    - Retrieves the parent directory name when the path ends with a slash.
    ```python
    get_parent_name("/path/to/directory/")
    ```
    - Retrieves the parent directory name when the path does not end with a slash.
    ```python
    get_parent_name("/path/to/directory")
    ```
    """
    normalized = os.path.normpath(path.rstrip('/'))
    return os.path.basename(os.path.dirname(normalized))

def get_size(directory_path, show_unit=False):
    """
    # directory.get_size(directory_path, show_unit=False)

    ---

    ### Overview
    Calculates the total size of all files in the specified directory (recursive). Returns raw bytes as int if `show_unit=False`, or a formatted string with unit (bytes to YB) otherwise.

    ### Parameters:
    - directory_path (str): The path of the directory to calculate the size of.
    - show_unit (bool, optional): If True, format as "X.X unit" (e.g., "2.0 KB"). Defaults to False (returns int bytes).

    ### Returns:
    - int: Total size in bytes (if `show_unit=False`).
    - str: Formatted size (e.g., "2.0 KB") if `show_unit=True`.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied (e.g., during walk).

    ### Examples:
    - Calculate raw bytes:
    ```python
    get_size("/path/to/directory")  # Returns: 2048 (int)
    ```
    - Calculate formatted size:
    ```python
    get_size("/path/to/directory", True)  # Returns: "2.0 KB" (str)
    ```
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")

    total_size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, dirnames, filenames in os.walk(directory_path)
        for filename in filenames
    )

    if not show_unit:
        return total_size

    size = total_size
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if size < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0

def get_tree(directory, indent="", prefix="├── "):
    """
    # directory.get_tree(directory, indent="", prefix="├── ")

    ---

    ### Overview
    Generates a visual representation of the directory structure rooted at the given `directory` path. 
    The structure is returned as a list of strings, each representing a line of the tree-like layout, 
    mimicking the output of the Unix `tree` command.

    Common development directories such as `.git`, `__pycache__`, `node_modules`, and `.venv` are 
    automatically ignored.

    ### Parameters:
    directory (str): The root directory path whose contents will be represented.
    indent (str): A string used for indenting subdirectory levels. Typically managed internally during recursion.
    prefix (str): The prefix to use before the current item. Defaults to `"├── "`.

    ### Returns:
    list[str]: A list of strings representing the visual structure of the directory tree.

    ### Raises:
    - PermissionError: If access to a directory is denied.

    ### Examples:
    - Displays the structure of a directory and its subdirectories.

    ```python
    lines = get_tree("/path/to/project")
    for line in lines:
        print(line)
    ```
    """
    
    tree_lines = []
    ignore_list = {'.git', '__pycache__', 'node_modules', '.venv'}
    
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        tree_lines.append(f"{indent}{prefix}[Permissão negada: {directory}]")
        return tree_lines
    
    items = [item for item in items if item not in ignore_list]
    
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = index == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        tree_lines.append(f"{indent}{current_prefix}{item}")
        
        if os.path.isdir(path):
            next_indent = indent + ("    " if is_last else "│   ")
            tree_lines.extend(get_tree(path, next_indent))
    return tree_lines

def join(path1='', path2='', path3='', path4='', paths=[]):
    """
    # directory.join(path1='', path2='', path3='', path4='', paths=[])

    ---

    ### Overview
    Joins multiple directory paths into a single path string. Treats all segments as strings (no reset on absolute paths). 
    Avoids double separators between segments and removes any trailing separator. Filters out empty paths for clean concatenation. 
    If `paths` is provided, it extends the individual paths (`path1` to `path4`).

    ### Parameters:
    path1, path2, path3, path4 (str): Individual directory paths to join. Defaults to empty strings (ignored if empty).
    paths (list, optional): A list of additional directory paths to append after the individual ones. Defaults to an empty list.

    ### Returns:
    str: The joined directory path.

    ### Examples:
    - Joins multiple directory paths.
    ```python
    join("/path/to", "directory", paths=["subdirectory", "file.txt"])
    ```
    - Joins multiple directory paths without additional paths.
    ```python
    join("/path/to", "directory")
    ```
    - Handles absolute paths without reset:
    ```python
    join("rel", "/abs")  # Returns: "rel/abs"
    ```
    - Filters empties:
    ```python
    join("", "a", "", paths=["b"])  # Returns: "a/b"
    ```
    """
    if paths:
        path_list = [p for p in [path1, path2, path3, path4] if p] + paths
    else:
        path_list = [p for p in [path1, path2, path3, path4] if p]
    if not path_list:
        return ""
    result = path_list[0]
    for p in path_list[1:]:
        if not result.endswith(os.sep):
            result += os.sep
        result += p.lstrip(os.sep)
    return result.rstrip(os.sep)

def move(source, destination, move_root=True, overwrite=False):
    """
    # directory.move(source, destination, move_root=True, overwrite=False)

    ---

    ### Overview
    Moves file or directory from source to destination.
    - For files: moves directly (ignores move_root).
    - For directories:
        - move_root=True: moves the directory itself (rename/move).
        - move_root=False: moves only its contents (into destination; merges if destination is existing dir).
    Creates parent directories if needed. By default, raises if destination conflicts (file/dir with same name).

    ### Parameters:
    source (str): The source path (file or directory).
    destination (str): The target path.
    move_root (bool, optional): For directories, move the root dir? Defaults to True.
    overwrite (bool, optional): Overwrite existing files/dirs at destination? Defaults to False (raises FileExistsError on conflict).

    ### Returns:
    dict: Details of the destination (from `wrapper.get_object`).

    ### Raises:
    - FileNotFoundError: If source does not exist.
    - ValueError: If source is not file/dir as expected.
    - FileExistsError: If destination conflicts and overwrite=False.
    - PermissionError: If permission denied.
    - OSError: If move fails (e.g., cross-device, other errors).

    ### Examples:
    - Move a file (raises if dest exists): 
    
    ```python
    move("/path/file.txt", "/new/file.txt")
    ```
    - Force overwrite: 
    ```python
    move("/path/file.txt", "/new/file.txt", overwrite=True)
    ```
    - Move entire dir:
    ```python
    move("/path/source_dir", "/new/target_dir")
    ```
    - Move contents:
    ```python
    move("/path/source_dir", "/new/target_dir", move_root=False)
    ```
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"The source path '{source}' does not exist.")
    
    def check_conflict(dest_path):
        """
        Helper to check/raise on conflict:
        Raises FileExistsError if dest_path exists and overwrite is False.
        """
        if overwrite:
            return
        if os.path.exists(dest_path):
            raise FileExistsError(f"Destination '{dest_path}' already exists. Set overwrite=True to force.")

    if os.path.isfile(source):
        check_conflict(destination)
        parent_dest = os.path.dirname(destination)
        if parent_dest and not os.path.exists(parent_dest):
            os.makedirs(parent_dest, exist_ok=True)
        shutil.move(source, destination)
        return wra.get_object(destination)

    if not os.path.isdir(source):
        raise ValueError(f"Source '{source}' must be a directory for directory move logic.")

    parent_dest = os.path.dirname(destination)
    if parent_dest and not os.path.exists(parent_dest):
        os.makedirs(parent_dest, exist_ok=True)

    if move_root:
        check_conflict(destination)
        shutil.move(source, destination)
    else:
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
        elif not os.path.isdir(destination):
            check_conflict(destination)
            raise OSError(f"Destination '{destination}' exists but is not a directory.")
        
        for root, dirs, files in os.walk(source):
            rel_root = os.path.relpath(root, source)
            dest_root = os.path.join(destination, rel_root) if rel_root != '.' else destination
            os.makedirs(dest_root, exist_ok=True)
            for d in dirs:
                item_dest = os.path.join(dest_root, d)
                check_conflict(item_dest)
                shutil.move(os.path.join(root, d), item_dest)
            for f in files:
                item_dest = os.path.join(dest_root, f)
                check_conflict(item_dest)
                shutil.move(os.path.join(root, f), item_dest)

        # Remove original folder after moving only contents
        shutil.rmtree(source, ignore_errors=True)
    return wra.get_object(destination)
   
def rename(old_path, new_path):
    """
    # directory.rename(old_path, new_path)

    ---

    ### Overview
    Renames a directory from the old directory path to the new directory path. If the old directory path does not exist or is not a directory, the function returns False.

    ### Parameters:
    old_path (str): The old directory path to rename.
    new_path (str): The new directory path.

    ### Returns:
    bool: True if the directory was successfully renamed, False otherwise.

    ### Raises:
    - FileExistsError: If new_path already exists.

    ### Examples:
    - Renames a directory.
    ```python
    rename("/path/to/old_directory", "/path/to/new_directory")
    ```
    """
    if not os.path.isdir(old_path):
        return False
    if os.path.exists(new_path):
        raise FileExistsError(f"Destination '{new_path}' already exists.")
    try:
        os.rename(old_path, new_path)
        return True
    except OSError:
        return False

def resolve_link_target(path, return_final_target=False):
    """
    # directory.resolve_link_target(path, return_final_target=False)

    ---

    ### Overview
    Gets the target of the specified directory link.

    ### Parameters:
    path (str): The path of the symbolic link.
    return_final_target (bool, optional): If True, resolves to the final target of nested links. Defaults to False.

    ### Returns:
    str: The path of the link target.

    ### Raises:
    - ValueError: If the path is not a symbolic link.
    - OSError: If the operation is not supported.

    ### Examples:
    - Resolves a symbolic link.
    ```python
    resolve_link_target("/path/to/link")
    ```
    """
    if not os.path.islink(path):
        raise ValueError(f"The path '{path}' is not a symbolic link.")
    target = os.path.realpath(path) if return_final_target else os.readlink(path)
    if not os.path.isdir(target):
        raise ValueError(f"Link target '{target}' must be a directory.")
    return target

def set_creation_time(path, creation_time):
    """
    # directory.set_creation_time(path, creation_time)

    ---

    ### Overview
    Sets the creation date and time for the specified directory. Approximates via modification time (Unix limitation: true creation time not settable).

    ### Parameters:
    path (str): The directory path.
    creation_time (datetime or str): The creation date and time to set. Str parsed as "%Y-%m-%d %H:%M:%S" or "%Y-%m-%d %H:%M:%S.%f".

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - ValueError: If str parse fails.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the creation time of a directory.
    ```python
    set_creation_time("/path/to/directory", datetime.datetime(2023, 1, 1))
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if isinstance(creation_time, str):
        try:
            creation_time = datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                creation_time = datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Invalid datetime string format: '{creation_time}'. Use '%Y-%m-%d %H:%M:%S' or with '.%f'.")
    ts = creation_time.timestamp()
    os.utime(path, (os.path.getatime(path), ts))

def set_creation_time_utc(path, creation_time_utc):
    """
    # directory.set_creation_time_utc(path, creation_time_utc)

    ---

    ### Overview
    Sets the creation date and time, in Coordinated Universal Time (UTC) format, for the specified directory. Approximates via modification time (Unix limitation: true creation time not settable). Uses timestamp directly for absolute UTC.

    ### Parameters:
    path (str): The directory path.
    creation_time_utc (datetime or str): The UTC creation date and time to set. Str parsed as above.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - ValueError: If str parse fails.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the UTC creation time of a directory.
    ```python
    set_creation_time_utc("/path/to/directory", datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc))
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if isinstance(creation_time_utc, str):
        try:
            creation_time_utc = datetime.datetime.strptime(creation_time_utc, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                creation_time_utc = datetime.datetime.strptime(creation_time_utc, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Invalid datetime string format: '{creation_time_utc}'. Use '%Y-%m-%d %H:%M:%S' or with '.%f'.")
    ts = creation_time_utc.timestamp()
    os.utime(path, (os.path.getatime(path), ts))

def set_current_directory(path):
    """
    # directory.set_current_directory(path)

    ---

    ### Overview
    Sets the application's current working directory to the specified directory and updates the global `current_directory` variable.

    ### Parameters:
    path (str): The directory path to set as the current working directory.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the current working directory.
    ```python
    set_current_directory("/path/to/directory")
    ```
    """
    global current_directory
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    os.chdir(path)
    current_directory = os.getcwd()

def set_last_access_time(path, last_access_time):
    """
    # directory.set_last_access_time(path, last_access_time)

    ---

    ### Overview
    Sets the date and time the specified directory was last accessed. Approximates via utime (sets access time).

    ### Parameters:
    path (str): The directory path.
    last_access_time (datetime or str): The last access date and time to set. Str parsed as above.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - ValueError: If str parse fails.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the last access time of a directory.
    ```python
    set_last_access_time("/path/to/directory", datetime.datetime(2023, 1, 1))
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if isinstance(last_access_time, str):
        try:
            last_access_time = datetime.datetime.strptime(last_access_time, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                last_access_time = datetime.datetime.strptime(last_access_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Invalid datetime string format: '{last_access_time}'. Use '%Y-%m-%d %H:%M:%S' or with '.%f'.")
    ts = last_access_time.timestamp()
    os.utime(path, (ts, os.path.getmtime(path)))

def set_last_access_time_utc(path, last_access_time_utc):
    """
    # directory.set_last_access_time_utc(path, last_access_time_utc)

    ---

    ### Overview
    Sets the date and time, in Coordinated Universal Time (UTC) format, that the specified directory was last accessed. Uses timestamp directly for absolute UTC.

    ### Parameters:
    path (str): The directory path.
    last_access_time_utc (datetime or str): The UTC last access date and time to set. Str parsed as above.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - ValueError: If str parse fails.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the UTC last access time of a directory.
    ```python
    set_last_access_time_utc("/path/to/directory", datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc))
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if isinstance(last_access_time_utc, str):
        try:
            last_access_time_utc = datetime.datetime.strptime(last_access_time_utc, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                last_access_time_utc = datetime.datetime.strptime(last_access_time_utc, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Invalid datetime string format: '{last_access_time_utc}'. Use '%Y-%m-%d %H:%M:%S' or with '.%f'.")
    ts = last_access_time_utc.timestamp()
    os.utime(path, (ts, os.path.getmtime(path)))

def set_last_write_time(path, last_write_time):
    """
    # directory.set_last_write_time(path, last_write_time)

    ---

    ### Overview
    Sets the date and time a directory was last written to. Approximates via utime (sets modification time).

    ### Parameters:
    path (str): The directory path.
    last_write_time (datetime or str): The last write date and time to set. Str parsed as above.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - ValueError: If str parse fails.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the last write time of a directory.
    ```python
    set_last_write_time("/path/to/directory", datetime.datetime(2023, 1, 1))
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if isinstance(last_write_time, str):
        try:
            last_write_time = datetime.datetime.strptime(last_write_time, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                last_write_time = datetime.datetime.strptime(last_write_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Invalid datetime string format: '{last_write_time}'. Use '%Y-%m-%d %H:%M:%S' or with '.%f'.")
    ts = last_write_time.timestamp()
    os.utime(path, (os.path.getatime(path), ts))

def set_last_write_time_utc(path, last_write_time_utc):
    """
    # directory.set_last_write_time_utc(path, last_write_time_utc)

    ---

    ### Overview
    Sets the date and time, in Coordinated Universal Time (UTC) format, that a directory was last written to. Uses timestamp directly for absolute UTC.

    ### Parameters:
    path (str): The directory path.
    last_write_time_utc (datetime or str): The UTC last write date and time to set. Str parsed as above.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - ValueError: If str parse fails.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the UTC last write time of a directory.
    ```python
    set_last_write_time_utc("/path/to/directory", datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc))
    ```
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if isinstance(last_write_time_utc, str):
        try:
            last_write_time_utc = datetime.datetime.strptime(last_write_time_utc, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                last_write_time_utc = datetime.datetime.strptime(last_write_time_utc, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Invalid datetime string format: '{last_write_time_utc}'. Use '%Y-%m-%d %H:%M:%S' or with '.%f'.")
    ts = last_write_time_utc.timestamp()
    os.utime(path, (os.path.getatime(path), ts))