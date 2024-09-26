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

    ### Parameters:
    *args (str): The paths to combine. The first argument must be an absolute path.
    paths (list): A list of paths to combine. The first element in the list must be an absolute path. Defaults to an empty list.

    ### Returns:
    str: The combined path.

    ### Raises:
    - ValueError: If the first argument or the first element in the paths list is not an absolute path.

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
        result = paths[0]
        if not os.path.isabs(result):
            raise ValueError(
f'''Invalid argument: The path "{result}" is not an absolute path.
- The first argument inside paths list must to be an absolute path.

For example, "/home/user/directory" is a valid absolute path. Please provide a valid absolute path.

'''
)
        for path in paths:
            if os.path.isabs(path):
                result = path
            else:
                result = join(result, path)
        return result

    result = args[0]
    if not os.path.isabs(result):
        raise ValueError(
f'''Invalid argument: The path "{result}" is not an absolute path.
- The first argument must to be an absolute path.

For example, "/home/user/directory" is a valid absolute path. Please provide a valid absolute path.

'''
)
    for path in args[1:]:
        if path == '':
            continue
        if os.path.isabs(path):
            result = path
        else:
            if not result.endswith(os.sep):
                result += os.sep
            result += path
    return result

def create(path, create_subdirs=True):
    """
    # directory.create(path, create_subdirs=True)

    ---

    ### Overview
    Creates a directory at the specified path. If `create_subdirs` is True, all intermediate-level 
    directories needed to contain the leaf directory will be created. After the directory is created, 
    it returns the details of the created directory.

    ### Parameters:
    path (str): The directory path to create.
    create_subdirs (bool): A flag that indicates whether to create intermediate subdirectories. 
    Defaults to True.

    ### Returns:
    dict: A dictionary containing the details of the created directory.

    ### Raises:
    - FileExistsError: If the directory already exists when `create_subdirs` is False.
    - PermissionError: If the permission is denied.
    - FileNotFoundError: If the path does not exist.

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
    - Exception: If the directory does not exist or if the directory is not empty and `recursive` is False.

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
    if not exists(path):
        raise Exception(f'\n\n>> The directory "{path}" does not exist.')

    if not os.listdir(path) or recursive:
        shutil.rmtree(path)
    else:
        raise Exception(f'\n\n>> The directory "{path}" is not empty.\n>> Use delete(path, True) to remove anyway.')

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
    if os.path.isdir(path):
        return True
    return False

def get_directories(path, fullpath=False):
    """
    # directory.get_directories(path, fullpath=False)

    ---
    
    ### Overview
    Retrieves a list of directories within the specified path.

    ### Parameters:
    path (str): The directory path to search within.
    fullpath (bool, optional): If True, returns the full path of each directory. Defaults to False.

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
    and the directory name is returned.

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
    if wra.has_extension(path):
        return f'{get_parent_name(path)}'
    else:
        return os.path.basename(os.path.dirname(path + '/'))

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
    if path.endswith('/'):
        path = path[:-1]
        return os.path.basename(path)
    return os.path.basename(os.path.dirname(path))

def join(path1='', path2='', path3='', path4='', paths=[]):
    """
    # directory.join(path1='', path2='', path3='', path4='', paths=[])

    ---

    ### Overview
    Joins multiple directory paths into a single path. The function ensures that each directory path ends with a separator before joining. If a directory path does not end with a separator, one is added.

    ### Parameters:
    path1, path2, path3, path4 (str): The directory paths to join. Defaults to an empty string.
    paths (list): A list of additional directory paths to join. Defaults to an empty list.

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
    """
    key_dir = ""
    if not path1.endswith(os.sep):
        if path1 != "":
            path1 = path1 + os.sep
    key_dir += path1
    if not path2.endswith(os.sep):
        if path2 != "":
            path2 = path2 + os.sep
    key_dir += path2
    if not path3.endswith(os.sep):
        if path3 != "":
            path3 = path3 + os.sep
    key_dir += path3
    if not path4.endswith(os.sep):
        if path4 != "":
            path4 = path4 + os.sep
    key_dir += path4

    if paths:
        for item in paths:
            if not item.endswith(os.sep):
                item = item + os.sep
            key_dir += item
    return key_dir[:-1]

def move(source, destination, move_root=True):
    """
    # directory.move(source, destination, move_root=True)

    ---

    ### Overview
    The move function is designed to move files or directories from a source location to a destination.
    It provides flexibility by allowing you to specify whether intermediate-level subdirectories should be created during the move operation.

    ### Parameters:
    source (str): The path to the file or directory you want to move.
    destination (str): The target location where the source should be moved.
    move_root (bool, optional): A flag indicating whether to move the entire directory (including its root)
    or just its contents. Defaults to True.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the source path does not exist.
    - PermissionError: If permission is denied during the move operation.

    ### Examples:
    - Move the entire directory (including intermediate subdirectories):

    ```python
    move("/path/to/source", "/path/to/destination")
    ```
    - Move only the leaf directory (raise an error if intermediate directories don't exist):

    ```python
    move("/path/to/source", "/path/to/destination", move_root=False)
    ```
    """
    if exists(destination):
        if move_root:
            shutil.move(source, destination)
        else:
            entries = os.listdir(source)
            for root, dirs, files in os.walk(source):
                for d in dirs:
                    shutil.move(os.path.join(root, d), os.path.join(destination, d))
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(destination, f))
    else:
        if move_root:
            create(destination)
            shutil.move(source, destination)
        else:
            entries = os.listdir(source)
            for root, dirs, files in os.walk(source):
                for d in dirs:
                    shutil.move(os.path.join(root, d), os.path.join(destination, d))
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(destination, f))
   
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

    ### Examples:
    - Renames a directory.

    ```python
    rename("/path/to/old_directory", "/path/to/new_directory")
    ```
    """
    if os.path.isdir(old_path):
        os.rename(old_path, new_path)
        return True
    return False
