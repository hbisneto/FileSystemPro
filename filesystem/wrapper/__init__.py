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

import codecs
import datetime
import glob
import os
import shutil
from filesystem import file as fsfile
from filesystem import directory as dir
import zipfile

### wrapper.combine() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def combine(*args, paths=[]):
    """
    # wrapper.combine(*args, paths=[])
    - #### Under support
        - Consider using `directory.combine(*args, paths=[])`

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

### wrapper.create_directory() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def create_directory(path, create_subdirs=True):
    """
    # wrapper.create(path, create_subdirs = True)
    - #### Under support
        - Consider using `directory.create(path, create_subdirs = True)`
    ---

    ### Overview
    Creates a directory at the specified path. If `create_subdirs` is True, all intermediate-level 
    directories needed to contain the leaf directory will be created. This function is useful for 
    setting up directory structures in a file system.

    ### Parameters:
    - path (str): The directory path to create.
    - create_subdirs (bool): A flag that indicates whether to create intermediate subdirectories. 
      Defaults to True.

    ### Returns:
    None

    ### Raises:
    - PermissionError: If the permission is denied.

    ### Examples:
    - Creates all intermediate subdirectories if they don't exist.

    ```python
    create("/path/to/directory")
    ```
    - Creates only the leaf directory, raises an error if any intermediate directory doesn't exist.

    ```python
    create("/path/to/directory", False)
    ```
    """
    if create_subdirs:
        os.makedirs(path, exist_ok=True)
    else:
        os.mkdir(path)
    return get_object(path)

### wrapper.create_file() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def create_file(file_name, path, text, encoding="utf-8-sig"):
    """
    # create_file(file_name, path, text, encoding="utf-8-sig")
    - #### Under support
        - Consider using `file.create(file, data, encoding="utf-8-sig")`
    ---

    ### Overview
    Creates a file with a specified name, path, and text content. 
    The file is created with a specified encoding, defaulting to "utf-8-sig".

    ### Parameters:
    file_name (str): The name of the file to create.
    path (str): The directory path where the file will be created.
    text (str): The text content to write into the file.
    encoding (str): The encoding to use when creating the file. Defaults to "utf-8-sig".

    ### Returns:
    A dictionary containing various attributes of the created file. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension.

    ### Raises:
    - FileExistsError: If the file already exists.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Creates a file with specified text content.

    ```python
    create_file("example.txt", "/path/to/directory", "Hello, World!")
    ```
    """
    try:
        with codecs.open(f'{path}/{file_name}', "w", encoding=encoding) as custom_file:
            custom_file.write(text)
    except:
        pass
    return get_object(f'{path}/{file_name}')

### wrapper.delete() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def delete(path, recursive=False):
    """
    # wrapper.delete(path, recursive = False)
    - #### Under support
        - Consider using `directory.delete(path, recursive=False)`

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
    if not os.path.exists(path):
        raise Exception(f'\n\n>> The directory "{path}" does not exist.')

    if not os.listdir(path) or recursive:
        shutil.rmtree(path)
    else:
        raise Exception(f'\n\n>> The directory "{path}" is not empty.\n>> Use delete(path, True) to remove anyway.')

### wrapper.enumerate_files() kept to cover version support. Remove on (MAJOR UPDATE ONLY)   
def enumerate_files(path):
    """
    # wrapper.enumerate_files(file)
    - #### Under support
        - Consider using `file.enumerate_files(path)`
    ---
    
    ### Overview
    Enumerates all files in a given directory and its subdirectories. For each file and directory, it retrieves various attributes using the `wra.get_object` function.

    ### Parameters:
    file (str): The directory path to enumerate files from.

    ### Returns:
    A list of dictionaries, where each dictionary contains various attributes of a file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Enumerates all files in the home directory and its subdirectories.

    ```python
    enumerate_files("~/")
    ```
    """
    results = []
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        results.append(get_object(root))
        results.extend([get_object(join(root,x)) for x in files])
    return results

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

### wrapper.get_files() kept to cover version support. Remove on (MAJOR UPDATE ONLY)   
def get_files(path):
    """
    # wrapper.get_files(path)
    - #### Under support
        - Consider using `file.get_files(path)`

    ---
    ### Overview
    Returns a list of dictionaries, each representing the properties of a file or directory at the specified path.

    ### Parameters:
    path (str): The path to get files from. This can be a directory or a file.

    ### Returns:
    A list of dictionaries. Each dictionary represents the properties of a file or directory and is obtained by calling the `get_object` function.

    ### Raises:
    - FileNotFoundError: If the path does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Get properties for all files in a directory.

    ```python
    get_files("/path/to/directory")
    ```
    - Get properties for a single file.

    ```python
    get_files("/path/to/file.txt")
    ```
    """
    result = []
    path = os.path.expanduser(path)
    for x in glob.glob(path):
        result.append(get_object(x))
    return result

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

### wrapper.join() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def join(path1='', path2='', path3='', path4='', paths=[]):
    """
    # wrapper.join(path1='', path2='', path3='', path4='', paths=[])
    - #### Under support
        - Consider using `directory.join(path1='', path2='', path3='', path4='', paths=[])`
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

### wrapper.list_directories() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def list_directories(path):
    """
    # wrapper.list_directories(path)
    - #### Under support
        - Consider using `directory.get_directories(path)`

    ---

    ### Overview
    Lists all directories in the specified path.

    ### Parameters:
    path (str): The directory path to list.

    ### Returns:
    list: A list of directory names in the specified path.

    ### Examples:
    - Lists all directories in a specific path.

    ```python
    get_directories("/path/to/directory")
    ```
    """
    directory_list = []
    for dir in os.listdir(path):
        if os.path.isdir(join(path, dir)):
            directory_list.append(dir)
    
    return directory_list

### wrapper.list_files() kept to cover version support. Remove on (MAJOR UPDATE ONLY)
def list_files(path):
    """
    # wrapper.list_files(path)
    - #### Under support
        - Consider using `file.get_files(path)`

    ---
    
    ### Overview
    Retrieves all files in a given directory.

    ### Parameters:
    path (str): The directory path to retrieve files from.

    ### Returns:
    A list of strings, where each string is the name of a file in the directory.

    ### Raises:
    - FileNotFoundError: If the directory does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Retrieves all files in a specific directory.

    ```python
    get_files("/path/to/directory")
    ```
    """
    file_list = []
    for file in os.listdir(path):
        if os.path.isfile(join(path, file)):
            file_list.append(file)
    return file_list

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

def read_zip_file_contents(zip_filename):
    """
    # wrapper.read_zip_file_contents(zip_filename)

    ---
    
    ### Overview
    Reads the contents of a ZIP file and returns a list of the names of the files contained within it.

    ### Parameters:
    zip_filename (str): The path to the ZIP file to read.

    ### Returns:
    list: A list of filenames contained in the ZIP file.

    ### Raises:
    - FileNotFoundError: If the ZIP file does not exist.
    - Exception: For any other errors that occur while reading the ZIP file.

    ### Examples:
    - Reads the contents of a ZIP file and returns the list of filenames.

    ```python
    read_zip_file_contents("/path/to/zipfile.zip")
    ```
    """
    try:
        with zipfile.ZipFile(zip_filename, "r") as zip_file:
            zip_contents_list = zip_file.namelist()
            return zip_contents_list
    except FileNotFoundError:
        return "[FileSystem Pro]: File Not Found"
    except Exception as e:
        return f"[FileSystem Pro]: An error occurred. Error: {e}"
