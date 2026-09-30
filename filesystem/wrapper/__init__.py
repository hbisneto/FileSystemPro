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
import hashlib
import mimetypes
import os
import stat
from filesystem import file as fsfile
from filesystem import directory as dir
from typing import(
    Dict, 
    List, 
    Optional, 
    Union, 
    Any
)
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional Unix-only modules
try:
    import pwd
    import grp
    _HAS_PWD_GRP = True
except ImportError:
    _HAS_PWD_GRP = False

# ===========================================================================
# Internal helpers
# ===========================================================================

def _human_age(seconds: float) -> str:
    """Convert seconds into a human-readable age string."""
    if seconds < 0:
        return "in the future"
    intervals = (
        ('year', 31536000),
        ('month', 2592000),
        ('week', 604800),
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
        ('second', 1),
    )
    for name, count in intervals:
        value = int(seconds // count)
        if value >= 1:
            return f"{value} {name}{'s' if value != 1 else ''}"
    return "0 seconds"

def _require_exists(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path '{path}' does not exist.")

# def _format_size(size: int) -> str:
#     for unit in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
#         if size < 1024.0:
#             return f"{size:3.1f} {unit}"
#         size /= 1024.0
#     return f"{size:3.1f} YB"

# def _format_timestamp(ts: float) -> str:
#     dt = datetime.datetime.fromtimestamp(ts)
#     return dt.strftime("%Y/%m/%d %H:%M:%S:%f")

def compare(path_a: str, path_b: str) -> Dict[str, Any]:
    """
    Compares two filesystem objects and returns differences in size,
    timestamps and type. Useful for sync / audit.
    """
    _require_exists(path_a)
    _require_exists(path_b)

    raw_a = get_raw_object(path_a)
    raw_b = get_raw_object(path_b)

    differences = {}

    # Type
    if raw_a["is_file"] != raw_b["is_file"] or raw_a["is_dir"] != raw_b["is_dir"]:
        differences["type"] = {
            "a": "file" if raw_a["is_file"] else ("dir" if raw_a["is_dir"] else "other"),
            "b": "file" if raw_b["is_file"] else ("dir" if raw_b["is_dir"] else "other"),
        }

    # Size
    if raw_a["size"] != raw_b["size"]:
        differences["size"] = {
            "a": raw_a["size"],
            "b": raw_b["size"],
            "delta": raw_b["size"] - raw_a["size"],
        }

    # Timestamps
    for key in ("created", "modified", "access"):
        if abs(raw_a[key] - raw_b[key]) > 1e-6:  # ignore microsecond noise
            differences[key] = {
                "a": raw_a[key],
                "b": raw_b[key],
                "delta_seconds": raw_b[key] - raw_a[key],
            }

    return {
        "identical": len(differences) == 0,
        "differences": differences,
        "path_a": path_a,
        "path_b": path_b,
    }

def get_age(path: str, reference: str = "modified") -> Dict[str, Any]:
    """
    Returns how long ago the object was created or modified.

    Parameters:
        reference: "created" or "modified" (default).

    Returns a dict with:
        - seconds: float
        - human: str  (e.g. "3 days")
        - reference: the reference used
    """
    _require_exists(path)

    if reference == "created":
        ts = os.path.getctime(path)
    elif reference == "modified":
        ts = os.path.getmtime(path)
    else:
        raise ValueError("reference must be 'created' or 'modified'")

    now = datetime.datetime.now().timestamp()
    seconds = now - ts

    return {
        "seconds": seconds,
        "human": _human_age(seconds),
        "reference": reference,
    }

# TEST FUNCTION
def get_link_target(path: str) -> str:
    """
    Returns the target of a symbolic link (os.readlink).
    Raises ValueError if the path is not a symlink.
    """
    _require_exists(path)
    if not os.path.islink(path):
        raise ValueError(f"Path '{path}' is not a symbolic link.")
    return os.readlink(path)

def get_mime_type(path: str) -> Optional[str]:
    """
    Detects the MIME type of a file using the standard library mimetypes module.
    Returns None if the type cannot be determined.
    """
    _require_exists(path)
    if not os.path.isfile(path):
        return None

    mime, _ = mimetypes.guess_type(path)
    return mime

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

def get_objects(
    paths: Union[str, List[str]],
    parallel: bool = False,
    max_workers: int = 4,
    raw: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    Batch version of get_object / get_raw_object.

    Parameters:
        paths: single path or list of paths.
        parallel: use ThreadPoolExecutor when True.
        max_workers: number of threads (only when parallel=True).
        raw: if True, call get_raw_object instead of get_object.

    Returns a dict keyed by the original path.
    Paths that raise an exception are stored as {"error": str(exception)}.
    """
    if isinstance(paths, str):
        paths = [paths]

    getter = get_raw_object if raw else get_object
    results: Dict[str, Dict[str, Any]] = {}

    def _safe_get(p: str) -> tuple:
        try:
            return p, getter(p)
        except Exception as e:
            return p, {"error": str(e)}

    if parallel and len(paths) > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_safe_get, p): p for p in paths}
            for future in as_completed(futures):
                path, data = future.result()
                results[path] = data
    else:
        for p in paths:
            _, data = _safe_get(p)
            results[p] = data

    return results

def get_owner(path: str) -> Dict[str, Any]:
    """
    Returns ownership information.
    On Unix tries to resolve UID/GID to names via pwd/grp.
    On Windows only UID/GID (or equivalent) are available.
    """
    _require_exists(path)

    st = os.stat(path)
    uid = st.st_uid
    gid = st.st_gid

    user_name = None
    group_name = None

    if _HAS_PWD_GRP:
        try:
            user_name = pwd.getpwuid(uid).pw_name
        except KeyError:
            user_name = None
        try:
            group_name = grp.getgrgid(gid).gr_name
        except KeyError:
            group_name = None

    return {
        "uid": uid,
        "gid": gid,
        "user": user_name,
        "group": group_name,
    }

def get_raw_object(path: str) -> Dict[str, Any]:
    """
    Same as get_object, but returns raw values:
    - timestamps as float (Unix epoch)
    - size as int (bytes)
    """
    _require_exists(path)

    head, tail = os.path.split(path)
    is_file = os.path.isfile(path)
    is_dir = os.path.isdir(path)
    is_link = os.path.islink(path)

    if is_file:
        size_bytes = os.path.getsize(path)
    else:
        size_bytes = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, filenames in os.walk(path)
            for filename in filenames
        )

    if is_file:
        _, ext = os.path.splitext(tail)
        extension = ext.lstrip('.') if ext else ""
        name_without_extension = os.path.splitext(tail)[0]
    else:
        extension = ""
        name_without_extension = tail

    return {
        "abspath": os.path.abspath(path),
        "access": os.path.getatime(path),          # float
        "created": os.path.getctime(path),         # float
        "dirname": os.path.dirname(path),
        "exists": True,
        "is_dir": is_dir,
        "is_file": is_file,
        "is_link": is_link,
        "extension": extension,
        "modified": os.path.getmtime(path),        # float
        "name": tail,
        "name_without_extension": name_without_extension,
        "size": size_bytes,                        # int
    }

def get_permissions(path: str) -> Dict[str, Any]:
    """
    Returns permission information:
    - mode: integer mode from st_mode
    - octal: string like '0o755'
    - readable / writable / executable: booleans via os.access
    """
    _require_exists(path)

    st = os.stat(path)
    mode = st.st_mode

    return {
        "mode": mode,
        "octal": oct(stat.S_IMODE(mode)),          # e.g. '0o755'
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
        "executable": os.access(path, os.X_OK),
    }

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

def is_empty(path: str) -> bool:
    """
    Returns True if:
    - the path is a file with size 0, or
    - the path is a directory containing no entries.
    """
    _require_exists(path)

    if os.path.isfile(path):
        return os.path.getsize(path) == 0
    if os.path.isdir(path):
        return len(os.listdir(path)) == 0
    return False

# ===========================================================================
# Explicit exports
# ===========================================================================

__all__ = [
    "compare",
    "get_age",
    "get_link_target",
    "get_mime_type",
    "get_object",
    "get_objects",
    "get_owner",
    "get_raw_object",
    "get_permissions",
    "has_extension",
    "is_empty",
]