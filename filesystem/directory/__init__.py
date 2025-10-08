"""
# Directory

---

## Overview
The Directory module is a component of the FileSystemPro library that provides a collection of functions
for handling directory-related operations. It simplifies tasks such as path manipulation, 
directory creation and deletion, file and directory enumeration, and management of directory metadata.

## Features
- **Directory Creation:** Creates new directories, with an option to create necessary subdirectories.
- **Directory Deletion:** Deletes directories, with an option for recursive deletion.
- **Directory Existence Check:** Checks whether a directory exists at a specified path.
- **Directory Information:** Retrieves parent directories and root information.
- **Directory Listing:** Lists all subdirectories within a given directory.
- **Directory Renaming:** Renames a directory if it exists.
- **File and Directory Enumeration:** Retrieves lists or iterators of files and directories, with support for search patterns and recursion.
- **Metadata Management:** Gets and sets creation, access, and modification times of directories.
- **Path Combination:** Dynamically combines multiple paths into a single path string.
- **Parent Directory Information:** Retrieves the name or path of a file's parent directory.
- **Symbolic Links:** Creates and resolves symbolic links.

## Usage
To use the functions provided by this module, 
import the module and call the desired function with the appropriate parameters:

```python
from filesystem import directory as dir
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
Creates a string that represents the path to the current directory. (Where the directory is working)
"""

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

def create_symbolic_link(path_target, path_link):
    """
    # directory.create_symbolic_link(path_link, path_target)

    ---

    ### Overview
    Creates a directory symbolic link identified by path that points to path_to_target.

    ### Parameters:
    path_target (str): The target directory the symbolic link points to.
    path_link (str): The path where the symbolic link will be created.

    ### Returns:
    dict: A dictionary containing details about the created symbolic link

    ### Raises:
    - FileExistsError: If the link already exists.
    - FileNotFoundError: If the target path does not exist.
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
    - FileNotFoundError: If the path does not exist.
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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
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
    - FileNotFoundError: If the path does not exist.
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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
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
    Gets the creation date and time of a directory.

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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.fromtimestamp(os.path.getctime(path))

def get_creation_time_utc(path):
    """
    # directory.get_creation_time_utc(path)

    ---

    ### Overview
    Gets the creation date and time, in Coordinated Universal Time (UTC) format, of a directory.

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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    return datetime.datetime.utcfromtimestamp(os.path.getctime(path))

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
    - FileNotFoundError: If the path does not exist.
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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
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
    - FileNotFoundError: If the path does not exist.
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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
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
    - FileNotFoundError: If the path does not exist.
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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
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
    if not os.path.exists(path):
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
    if not os.path.exists(path):
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
    if not os.path.exists(path):
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
    if not os.path.exists(path):
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
    # directory.get_size(directory_path)

    ---

    ### Overview
    Calculates the total size of all files in the specified directory. The size is returned in bytes, KB, MB, GB, or TB, depending on the total size.

    ### Parameters:
    - directory_path (str): The path of the directory to calculate the size of.

    ### Returns:
    - str: A string representing the total size of the directory, formatted as a float followed by the unit of measurement.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Calculate the total size of all files in a directory:

    ```python
    get_size("/path/to/directory")

    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")

    total_size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, dirnames, filenames in os.walk(directory_path)
        for filename in filenames
    )

    if not show_unit:
        return  total_size

    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if total_size < 1024.0:
            return f"{total_size:3.1f} {unit}"
        total_size /= 1024.0

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
    if not exists(source):
        raise FileNotFoundError(f"The source path '{source}' does not exist.")
    
    if exists(destination):
        if move_root:
            shutil.move(source, destination)
        else:
            for root, dirs, files in os.walk(source):
                for d in dirs:
                    shutil.move(os.path.join(root, d), os.path.join(destination, os.path.relpath(os.path.join(root, d), source)))
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(destination, os.path.relpath(os.path.join(root, f), source)))
    else:
        if move_root:
            create(destination)
            shutil.move(source, destination)
        else:
            create(destination)
            for root, dirs, files in os.walk(source):
                for d in dirs:
                    shutil.move(os.path.join(root, d), os.path.join(destination, os.path.relpath(os.path.join(root, d), source)))
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(destination, os.path.relpath(os.path.join(root, f), source)))
   
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
    - FileNotFoundError: If the path does not exist or is not a symbolic link.
    - OSError: If the operation is not supported.

    ### Examples:
    - Resolves a symbolic link.

    ```python
    resolve_link_target("/path/to/link")
    ```
    """
    if not os.path.islink(path):
        raise FileNotFoundError(f"The path '{path}' is not a symbolic link.")
    if return_final_target:
        return os.path.realpath(path)
    return os.readlink(path)

def set_creation_time(path, creation_time):
    """
    # directory.set_creation_time(path, creation_time)

    ---

    ### Overview
    Sets the creation date and time for the specified directory.

    ### Parameters:
    path (str): The directory path.
    creation_time (datetime): The creation date and time to set.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the creation time of a directory.

    ```python
    set_creation_time("/path/to/directory", datetime.datetime(2023, 1, 1))
    ```
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    # Note: Setting creation time is not directly supported in Python's standard library.
    # This is a limitation, as os.utime only sets access and modification times.
    # For Unix, we can approximate by setting modification time as a fallback.
    if not type(creation_time) == datetime.datetime:
        creation_time = datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S")
    os.utime(path, (os.path.getatime(path), creation_time.timestamp()))

def set_creation_time_utc(path, creation_time_utc):
    """
    # directory.set_creation_time_utc(path, creation_time_utc)

    ---

    ### Overview
    Sets the creation date and time, in Coordinated Universal Time (UTC) format, for the specified directory.

    ### Parameters:
    path (str): The directory path.
    creation_time_utc (datetime): The UTC creation date and time to set.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the UTC creation time of a directory.

    ```python
    set_creation_time_utc("/path/to/directory", datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc))
    ```
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if not type(creation_time_utc) == datetime.datetime:
        creation_time_utc = datetime.datetime.strptime(creation_time_utc, "%Y-%m-%d %H:%M:%S")
    # Convert UTC datetime to local timestamp
    local_time = creation_time_utc.timestamp() - datetime.datetime.now().astimezone().utcoffset().total_seconds()
    os.utime(path, (os.path.getatime(path), local_time))

def set_current_directory(path):
    """
    # directory.set_current_directory(path)

    ---

    ### Overview
    Sets the application's current working directory to the specified directory.

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
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    os.chdir(path)
    current_directory = os.getcwd()

def set_last_access_time(path, last_access_time):
    """
    # directory.set_last_access_time(path, last_access_time)

    ---

    ### Overview
    Sets the date and time the specified directory was last accessed.

    ### Parameters:
    path (str): The directory path.
    last_access_time (datetime): The last access date and time to set.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the last access time of a directory.

    ```python
    set_last_access_time("/path/to/directory", datetime.datetime(2023, 1, 1))
    ```
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if not type(last_access_time) == datetime.datetime:
        last_access_time = datetime.datetime.strptime(last_access_time, "%Y-%m-%d %H:%M:%S")
    os.utime(path, (last_access_time.timestamp(), os.path.getmtime(path)))

def set_last_access_time_utc(path, last_access_time_utc):
    """
    # directory.set_last_access_time_utc(path, last_access_time_utc)

    ---

    ### Overview
    Sets the date and time, in Coordinated Universal Time (UTC) format, that the specified directory was last accessed.

    ### Parameters:
    path (str): The directory path.
    last_access_time_utc (datetime): The UTC last access date and time to set.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the UTC last access time of a directory.

    ```python
    set_last_access_time_utc("/path/to/directory", datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc))
    ```
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if not type(last_access_time_utc) == datetime.datetime:
        last_access_time_utc = datetime.datetime.strptime(last_access_time_utc, "%Y-%m-%d %H:%M:%S")
    local_time = last_access_time_utc.timestamp() - datetime.datetime.now().astimezone().utcoffset().total_seconds()
    os.utime(path, (local_time, os.path.getmtime(path)))

def set_last_write_time(path, last_write_time):
    """
    # directory.set_last_write_time(path, last_write_time)

    ---

    ### Overview
    Sets the date and time a directory was last written to.

    ### Parameters:
    path (str): The directory path.
    last_write_time (datetime): The last write date and time to set.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the last write time of a directory.

    ```python
    set_last_write_time("/path/to/directory", datetime.datetime(2023, 1, 1))
    ```
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if not type(last_write_time) == datetime.datetime:
        last_write_time = datetime.datetime.strptime(last_write_time, "%Y-%m-%d %H:%M:%S")
    os.utime(path, (os.path.getatime(path), last_write_time.timestamp()))

def set_last_write_time_utc(path, last_write_time_utc):
    """
    # directory.set_last_write_time_utc(path, last_write_time_utc)

    ---

    ### Overview
    Sets the date and time, in Coordinated Universal Time (UTC) format, that a directory was last written to.

    ### Parameters:
    path (str): The directory path.
    last_write_time_utc (datetime): The UTC last write date and time to set.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If permission is denied.

    ### Examples:
    - Sets the UTC last write time of a directory.

    ```python
    set_last_write_time_utc("/path/to/directory", datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc))
    ```
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if not type(last_write_time_utc) == datetime.datetime:
        last_write_time_utc = datetime.datetime.strptime(last_write_time_utc, "%Y-%m-%d %H:%M:%S")
    local_time = last_write_time_utc.timestamp() - datetime.datetime.now().astimezone().utcoffset().total_seconds()
    os.utime(path, (os.path.getatime(path), local_time))