"""
# Directory

---

## Overview
The Directory module is a component of the FileSystemPro library that provides a collection of functions
for handling directory-related operations. It simplifies tasks such as path manipulation, 
directory creation and deletion, and file retrieval within directories.

## Features
- `Path Combination:` Dynamically combines multiple paths into a single path string.
- `Directory Creation:` Creates new directories, with an option to create necessary subdirectories.
- `Directory Deletion:` Deletes directories, with an option for recursive deletion.
- `Directory Existence Check:` Checks whether a directory exists at a specified path.
- `File Retrieval:` Retrieves a list of files within a directory using glob patterns.
- `Parent Directory Information:` Retrieves the name or path of a file's parent directory.
- `Directory Listing:` Lists all subdirectories within a given directory.
- `Directory Renaming:` Renames a directory if it exists.

## Detailed Functionality
The module's functions are designed to be intuitive and provide a high level of abstraction from the
underlying file system operations.

### Path Combination (`combine`)
The `combine` function takes multiple path segments and intelligently combines them into a single path. 
It ensures that the resulting path is valid and absolute, 
raising an error if the initial segment is not an absolute path.

### Directory Creation and Deletion (`create`, `delete`)
The `create` function allows for the creation of directories, 
with the option to create all necessary subdirectories if they do not exist. 
The `delete` function removes directories, with the ability to recursively delete all contents if specified.

### Directory and File Information (`exists`, `get_files`, `get_parent_name`, `get_parent`, `get_name`)
The `exists` function checks for the existence of a directory. 
The `get_files` function uses glob patterns to retrieve files within a directory. 
The `get_parent_name`, `get_parent`, and `get_name` functions provide information 
about the parent directory of a given path.

### Directory Operations (`join`, `list`, `rename`)
The `join` function is a versatile path joiner that can handle multiple path segments. 
The `list` function returns a list of all subdirectories within a specified directory. 
The `rename` function allows for renaming a directory, 
ensuring that the operation only occurs if the directory exists.

## Usage
To use the functions provided by this module, 
import the module and call the desired function with the appropriate parameters:

```python
from filesystem import directory as dir
```
"""

import os
import shutil
import filesystem as fs
from filesystem import wrapper as wra

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

def get_directories(path, fullpath=True):
    """
    # directory.get_directories(path, fullpath=True)

    ---
    
    ### Overview
    Retrieves a list of directories within the specified path.

    ### Parameters:
    path (str): The directory path to search within.
    fullpath (bool, optional): If True, returns the full path of each directory. Defaults to True.

    ### Returns:
    list: A list of directory names or full paths, depending on the `fullpath` parameter.

    ### Raises:
    - FileNotFoundError: If the specified path does not exist.
    - PermissionError: If the permission is denied to access the path.

    ### Examples:
    - Retrieves directory names within a specified path.

    ```python
    get_directories("/path/to/directory")
    ```

    - Retrieves full paths of directories within a specified path.

    ```python
    get_directories("/path/to/directory", fullpath=True)
    ```
    """
    directory_list = []
    for dir in os.listdir(path):
        if os.path.isdir(join(path, dir)):
            if fullpath == True:
                directory_list.append(f'{path}{fs.OS_SEPARATOR}{dir}')
            else:
                directory_list.append(dir)
    return directory_list

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
