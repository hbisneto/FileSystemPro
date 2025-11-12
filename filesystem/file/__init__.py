"""
# File

---

## Overview
The File module is a comprehensive utility toolset that forms part of the FileSystemPro library. 
It provides a suite of functions designed to handle various file operations such as integrity checks,
file creation, deletion, enumeration, and file splitting and reassembling.

## Features
- `Checksum Calculation:` Utilizes SHA-256 hashing to calculate file checksums for integrity verification.
- `Integrity Check:` Compares checksums of two files to verify their integrity.
- `File Creation:` Supports creating both text and binary files with specified data.
- `File Deletion:` Safely deletes files by checking for their existence before removal.
- `File Enumeration:` Enumerates all files in a given directory, providing detailed file information.
- `File Existence Check:` Determines if a file exists at a given path.
- `File Listing:` Lists all files in a specified directory.
- `File Renaming:` Renames files within a directory after checking for their existence.
- `File Reassembling:` Reassembles split files back into a single file.
- `File Splitting:` Splits a file into smaller parts based on a specified chunk size.

## Detailed Functionality
The module's functions are designed to be robust and easy to use, 
providing a high level of abstraction from the underlying file system operations.

### Checksum Calculation and Integrity Check
The `calculate_checksum` function reads a file in binary mode and calculates its SHA-256 hash, 
returning the hexadecimal digest. The `check_integrity` function uses this to compare the checksums of 
two files, which is essential for verifying that files have not been tampered with or corrupted.

### File Creation, Deletion, and Enumeration
File creation is handled by two functions: `create` for text files, 
which uses codecs to handle different encodings, and `create_binary_file` for binary files. 
The `delete` function removes a file after confirming its existence, 
while `enumerate_files` provides a comprehensive list of all files in a directory, including their metadata.

### File Existence, Listing, and Renaming
The `exists` function checks if a file is present at a specified path. 
The `list` function returns a list of all files in a directory. 
The `rename` function allows for renaming a file if it exists.

### File Reassembling and Splitting
The `reassemble_file` function is used to combine parts of a 
previously split file back into its original form. 
Conversely, the `split_file` function divides a file into smaller parts, 
each with a size defined by the `chunk_size` parameter.

## Usage
To use the functions provided by this module, 
import the module and call the desired function with the appropriate parameters:

```python
from filesystem import file as fsfile
```
"""

import codecs
import hashlib
import os
import shutil
import filesystem as fs
from filesystem import directory as dir
from filesystem import wrapper as wra

def append_text(file, text, encoding="utf-8"):
    """
    # file.append_text(file, text, encoding="utf-8")

    ---

    ### Overview
    Appends the specified text to a file at the given path using the specified encoding. If the file does not exist, it is created. The text is appended to the end of the file without adding a newline character.

    ### Parameters:
    - file (str): The path to the file where the text will be appended.
    - text (str): The text to append to the file.
    - encoding (str, optional): The encoding to use for writing the text. Defaults to "utf-8".

    ### Returns:
    None

    ### Raises:
    - IOError: If an I/O error occurs during file writing.
    - PermissionError: If permission is denied when accessing the file.
    - UnicodeEncodeError: If the text cannot be encoded with the specified encoding.

    ### Examples:
    - Append text to a file with default UTF-8 encoding:

    ```python
    fsfile.append_text("example.txt", "This is a sample text.")
    ```

    - Append text to a file with a different encoding:

    ```python
    fsfile.append_text("example.txt", "This is a sample text.", encoding="utf-16")
    ```
    """
    with open(file, 'a', encoding=encoding) as file:
        file.write(f'{text}')

def calculate_checksum(file):
    """
    # file.calculate_checksum(file)

    ---

    ### Overview
    Calculates the SHA-256 checksum of a file. This function reads the file in binary mode and updates the hash in chunks to efficiently handle large files.

    ### Parameters:
    file (str): The path to the file for which the checksum is to be calculated.

    ### Returns:
    str: The calculated hexadecimal SHA-256 checksum of the file.

    ### Raises:
    - FileNotFoundError: If the file does not exist at the specified path.
    - IOError: If there is an error reading the file.

    ### Examples:
    - Calculate and return the checksum of a file:

    ```python
    checksum = calculate_checksum("/path/to/file")
    print(checksum)
    ```
    """
    sha256_hash = hashlib.sha256()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_integrity(file, reference_file):
    """
    # file.check_integrity(file, reference_file)

    ---
    
    ### Overview
    Compares the SHA-256 checksums of two files to verify their integrity. This function is useful for ensuring that a file has not been altered or corrupted by comparing it to a reference file.

    ### Parameters:
    file (str): The path to the file whose integrity is being checked.
    reference_file (str): The path to the reference file against which the checksum comparison is made.

    ### Returns:
    bool: Returns True if the checksums match, indicating the files are identical in content; False otherwise.

    ### Raises:
    - FileNotFoundError: If either the `file` or `reference_file` does not exist at the specified paths.
    - IOError: If there is an error reading either file during the checksum calculation.

    ### Examples:
    - Check the integrity of a file against a reference file and print the result:

    ```python
    integrity = check_integrity("/path/to/file", "/path/to/reference_file")
    print("Files are identical:", integrity)
    ```
    """
    file_to_check = calculate_checksum(file)
    reference_check = calculate_checksum(reference_file)

    return file_to_check == reference_check

def copy(source, destination, overwrite=False):
    """
    # file.copy(source, destination, overwrite=False)

    ---

    ### Overview
    Copies a file or a list of files from the source to the destination. This function handles both single file copying and multiple file copying while providing options for overwriting existing files and performing various validation checks.
    
    **For lists, copies each file individually to the destination directory; partial failures do not stop the process.**

    ### Parameters:
    - source (str or list): The path to the source file or a list of source files to be copied.
    - destination (str): The path to the destination directory where the file(s) should be copied.
    - overwrite (bool, optional): If set to True, existing files at the destination will be overwritten. Defaults to False.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the source file or any of the listed source files do not exist.
    - FileExistsError: If the file already exists in the destination and `overwrite` is set to False.
    - PermissionError: If the destination path is not writable.
    - Exception: For any unexpected errors that occur during the copying process.

    ### Examples:
    - Copying a single file without overwriting:

    ```python
    copy("path/to/source/file.txt", "path/to/destination/")
    ```

    - Copying multiple files with the option to overwrite existing files:

    ```python
    copy(["path/to/source/file1.txt", "path/to/source/file2.txt"], "path/to/destination/", overwrite=True)
    ```
    """
    try:
        if isinstance(source, str):
            if not os.path.exists(source): 
                raise FileNotFoundError(f'Source file "{source}" does not exist.')
            
            if not os.access(os.path.dirname(destination), os.W_OK): 
                raise PermissionError(f'Destination path "{os.path.dirname(destination)}" is not writable.') 

            if not overwrite:
                destination_files = get_files(destination, False)
                if get_filename(source) in destination_files:
                    raise FileExistsError(f'The file "{source}" already exists in "{destination}"')
            shutil.copy2(source, destination)
            
        if isinstance(source, list):
            for item in source:
                if not os.path.exists(item): 
                    raise FileNotFoundError(f'Source file "{item}" does not exist.')
        
                if not os.access(os.path.dirname(destination), os.W_OK): 
                    raise PermissionError(f'Destination path "{os.path.dirname(destination)}" is not writable.') 

                if not overwrite:
                    destination_files = get_files(destination, False)
                    if get_filename(item) in destination_files:
                        raise FileExistsError(f'The file "{item}" already exists in "{destination}"')
                shutil.copy2(item, destination)
    
    except FileNotFoundError as fnf_error: 
        raise fnf_error

    except FileExistsError as fe_error:
        raise fe_error
    
    except PermissionError as perm_error:  
        raise perm_error
    
    except Exception as e: 
        raise Exception(f'An unexpected error occurred: {e}')

def create(file, data, overwrite=False, encoding="utf-8"):
    """
    # file.create(file, data, overwrite=False, encoding="utf-8")

    ---

    ### Overview
    Creates or modifies a file at the specified path by writing the provided data. If `overwrite` is `True`, the file is overwritten; otherwise, the data is appended to the end of the file. Returns a dictionary with the file's metadata after the operation.

    ### Parameters:
    - file (str): The path to the file to create or modify.
    - data (str): The data to write into the file.
    - overwrite (bool, optional): If `True`, overwrites the file; if `False`, appends to it. Defaults to `False`.
    - encoding (str, optional): The encoding to use for writing the data. Defaults to "utf-8".

    ### Returns:
    dict: A dictionary containing metadata of the created or modified file, as returned by `wra.get_object`.

    ### Raises:
    - IOError: If an I/O error occurs during file writing.
    - PermissionError: If permission is denied when accessing the file.
    - UnicodeEncodeError: If the data cannot be encoded with the specified encoding.

    ### Examples:
    - Create a new file or append to an existing one:

    ```python
    file_details = fsfile.create("example.txt", "Hello, World!")
    print(file_details)
    ```

    - Overwrite a file with a different encoding:

    ```python
    file_details = fsfile.create("example.txt", "Hello, World!", overwrite=True, encoding="utf-16")
    print(file_details)
    ```
    """
    if overwrite==True:
        with codecs.open(f'{file}', "w", encoding=encoding) as custom_file:
            custom_file.write(data)
    else:
        with codecs.open(f'{file}', "a", encoding=encoding) as custom_file:
            custom_file.write(data)

    return wra.get_object(f'{file}')

def create_binary_file(filename, data, buffer_size=4096):
    """
    # file.create_binary_file(filename, data, buffer_size=4096)

    ---

    ### Overview
    Creates or overwrites a binary file at the specified path and writes the provided data. If the data is a string, it is encoded to bytes using UTF-8 before writing. The file is always overwritten if it exists, and the buffer size can be adjusted for performance optimization.

    ### Parameters:
    - filename (str): The path to the binary file to create or overwrite.
    - data (str or bytes): The data to write into the file. Strings are encoded to bytes using UTF-8.
    - buffer_size (int, optional): The buffer size for writing the file, in bytes. Defaults to 4096.

    ### Returns:
    None

    ### Raises:
    - IOError: If an I/O error occurs during file writing.
    - PermissionError: If permission is denied when accessing the file.
    - UnicodeEncodeError: If a string input cannot be encoded to bytes.

    ### Examples:
    - Create a binary file with string data:

    ```python
    fsfile.create_binary_file("example.bin", "Hello, World!")
    ```

    - Create a binary file with byte data and custom buffer size:

    ```python
    fsfile.create_binary_file("example.bin", b"Hello, World!", buffer_size=8192)
    ```
    """
    if type(data) != bytes:
        b_data = bytes(data.encode())
        with open(filename, 'wb', buffering=buffer_size) as binary_file:
            binary_file.write(b_data)
    else:
        with open(filename, 'wb', buffering=buffer_size) as binary_file:
            binary_file.write(data)

def delete(file):
    """
    # file.delete(file)

    ---
    
    ### Overview
    Deletes a file at the specified path if it exists.

    ### Parameters:
    - file (str): The file path to delete.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Deletes a file if it exists.

    ```python
    delete("/path/to/file")
    ```
    """
    if not exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    os.remove(file)

def enumerate_files(file):
    """
    # file.enumerate_files(file)

    ---
    
    ### Overview
    Enumerates all files in a given directory and its subdirectories. 
    For each file and directory, it retrieves various attributes using the `wra.get_object` function.

    ### Parameters:
    file (str): The directory path to enumerate files from.

    ### Returns:
    A list of dictionaries, where each dictionary contains various attributes of a file or directory. 
    These attributes include the time of last modification, creation time, last access time, name, size, 
    absolute path, parent directory, whether it's a directory or file or link, whether it exists, 
    and its extension (if it's a file).

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
    file = os.path.expanduser(file)
    for root, dirs, files in os.walk(file):
        results.append(wra.get_object(root))
        results.extend([wra.get_object(dir.join(root,x)) for x in files])
    return results

def exists(file):
    """
    # file.exists(file)

    ---
    
    ### Overview
    Checks if a file exists at the specified path.

    ### Parameters:
    file (str): The file path to check.

    ### Returns:
    bool: True if the file exists, False otherwise.

    ### Raises:
    - PermissionError: If the permission is denied.

    ### Examples:
    - Checks if a file exists at a specific path.

    ```python
    exists("/path/to/file")
    ```
    """
    is_file = os.path.isfile(file)
    if is_file:
        return True
    return False

def find_duplicates(path):
    """
    # file.find_duplicates(path)
    
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
            checksum = calculate_checksum(file_path)
            if checksum in checksums:
                original_files.append(checksums[checksum])
                duplicate_files.append(file_path)
            else:
                checksums[checksum] = file_path
    return original_files, duplicate_files

def get_extension(file, lower=True):
    """
    # file.get_extension(file, lower=True)

    ---
    
    ### Overview
    Extracts the file extension from the given file path and returns it in lowercase or uppercase based on the `lower` parameter.

    ### Parameters:
    file (str): The path of the file from which to extract the extension.
    lower (bool, optional): If True, returns the extension in lowercase. If False, returns it in uppercase. Default is True.

    ### Returns:
    str: The file extension in lowercase or uppercase.

    ### Examples:
    - Extracts the file extension in lowercase.

    ```python
    get_extension("/path/to/file.txt")
    # Output: '.txt'
    ```

    - Extracts the file extension in uppercase.

    ```python
    get_extension("/path/to/file.txt", lower=False)
    # Output: '.TXT'
    ```
    """

    _, file_extension = os.path.splitext(file)
    if lower == True:
        return file_extension.lower()
    return file_extension.upper()

def get_filename(file):
    """
    # file.get_filename(path)

    ---

    ### Overview
    Extracts the filename from the given filepath and returns it.

    ### Parameters:
    path (str): The path of the file from which to extract the filename.

    ### Returns:
    str: The filename extracted from the path.

    ### Examples:
    - Extracts the filename from a given file path.

    ```python
    get_filename("/path/to/your/file/name.txt")
    ```
    """
    return os.path.basename(file)

def get_files(path, fullpath=True, extension=None):
    """
    # file.get_files(path, fullpath=True, extension=None)

    ---

    ### Overview
    Retrieves a list of files from the specified directory. Optionally, it can return the full path of each file and filter files by their extension.

    ### Parameters:
    - path (str): The directory path to search for files.
    - fullpath (bool, optional): If True, returns the full path of each file. Defaults to True.
    - extension (str, optional): If specified, only files with this extension will be included. Defaults to None.

    ### Returns:
    - list: A list of file names or full paths, depending on the `fullpath` parameter.

    ### Raises:
    - FileNotFoundError: If the specified directory does not exist.
    - PermissionError: If the permission is denied to access the directory.

    ### Examples:
    - Retrieve all files in a directory:

    ```python
    get_files("/path/to/directory")
    ```

    - Retrieve all `.txt` files in a directory with full paths:

    ```python
    get_files("/path/to/directory", fullpath=True, extension=".txt")
    ```
    """
    
    file_list = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if extension is None or file.endswith(extension):
                if fullpath == True:
                    file_list.append(f'{path}{fs.OS_SEPARATOR}{file}')
                else:
                    file_list.append(file)
    return file_list

def get_size(file, show_unit=False):
    """
    # file.get_size(file, show_unit=False)

    ---

    ### Overview
    Calculates the size of a file at the specified path.
    Returns raw bytes (int) or a formatted string in bytes/KB/MB/GB/TB/PB/EB/ZB/YB (up to ~1 YB), depending on the `show_unit` parameter.

    ### Parameters:
    - file (str): The path of the file to calculate the size of.
    - show_unit (bool, optional): If True, returns a formatted string with units (e.g., '1.0 KB'); if False, returns raw bytes as int. Defaults to False.

    ### Returns:
    - int or str: Raw bytes as int if `show_unit=False`; formatted string with unit if `True` (e.g., '1.0 KB').

    ### Raises:
    - FileNotFoundError: If the file does not exist or is not a file.
    - OSError (including PermissionError): If access is denied or another OS error occurs during size retrieval.

    ### Examples:
    - Calculate the raw size (int) of a file:

    ```python
    size = fsfile.get_size("/path/to/file")
    print(size)  # e.g., 1024
    """ 

    if not os.path.isfile(file): 
        raise FileNotFoundError(f"The file '{file}' was not found.")

    size = os.path.getsize(file) 
    if not show_unit:
        return size
    
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if size < 1024.0: 
            return f"{size:3.1f} {unit}"
        size /= 1024.0

def move(source, destination, new_filename=None, replace_existing=False):
    """
    # file.move(source, destination, new_filename=None, replace_existing=False)

    ---
    
    ### Overview
    The move function moves a file from a source location to a destination location. 
    If the destination file already exists, 
    you can choose whether to replace it or keep the existing file. 

    ### Parameters
    - source (str): The path to the source file.
    - destination (str): The path to the destination directory.
    - new_filename (Optional[str]): The new filename to use in the destination directory. If not provided, the original filename from the source path is used.
    - replace_existing (Optional[bool]): If `True`, replace the existing file in the destination. If `False`, raise an error if the destination file already exists. Defaults to False.

    ### Returns
    None

    ### Raises
    - FileNotFoundError: If the source file does not exist.
    - PermissionError: If permission is denied during the move operation.

    ### Examples
    - Move a file:

    ```python
    move("/path/to/source/file.txt", "/path/to/destination/")
    ```

    - Move a file with a different filename in the destination:

    ```python
    move("/path/to/source/file.txt", "/path/to/destination/", new_filename="new_file.txt")
    ```

    - Replace an existing file in the destination:

    ```python
    move("/path/to/source/file.txt", "/path/to/destination/", replace_existing=True)
    ```
    """
    if new_filename:
        destination_file = os.path.join(destination, new_filename)
    else:
        destination_file = os.path.join(destination, os.path.basename(source))

    try:
        if exists(destination_file):
            if replace_existing:
                shutil.move(source, destination_file)
            else:
                raise FileExistsError(f"[FileSystemPro.move.FileExistsError]: Destination file '{destination_file}' already exists. Use 'replace_existing=True' to replace it.")
        else:
            shutil.move(source, destination_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"[FileSystemPro.move.FileNotFoundError]: {e}")

def rename(old_name, new_name):
    """
    # file.rename(old_name, new_name)

    ---
    
    ### Overview
    Renames a file in a given directory from `old_name` to `new_name`.
    Returns True if the file was successfully renamed, False otherwise.

    ### Parameters:
    old_name (str): The current name of the file.
    new_name (str): The new name for the file.

    ### Returns:
    bool: True if the file was successfully renamed, False otherwise.

    ### Raises:
    - PermissionError: If the permission is denied.

    ### Examples:
    - Renames a file in a specific directory.

    ```python
    rename("/path/to/file/old_name.txt", "/path/to/file/new_name.txt")
    ```
    """
    if exists(old_name):
        os.rename(old_name, new_name)
        return True
    return False

def reassemble_file(large_file, new_file):
    """
    # file.reassemble_file(large_file, new_file)

    ---
    
    ### Overview
    Reassembles a file that was previously split into parts. 
    The function checks for the existence of the split parts and reads each part, writing it to a new file. 
    After all parts have been written to the new file, the function deletes the parts.
    
    **Ignores missing sequential parts and processes only existing ones. If no parts exist, no action is taken.**

    ### Parameters:
    large_file (str): The name of the original large file that was split.
    new_file (str): The name for the new file that will be created from the parts.

    ### Returns:
    None

    ### Raises:
    - IOError: If an error occurs reading or writing parts.
    - PermissionError: If permission is denied during operations.

    ### Examples:
    - Reassembles a file that was split into parts.

    ```python
    reassemble_file("large_file", "new_file")
    ```
    """
    parts = []
    i = 0
    while os.path.exists(f'{large_file}.fsp{str(i)}'):
        parts.append(f'{large_file}.fsp{str(i)}')
        i += 1

    if len(parts) != 0:
        with open(new_file, 'wb') as output_file:
            for part in parts:
                with open(part, 'rb') as part_file:
                    output_file.write(part_file.read())
            
        for part in parts:
            delete(part)

def split_file(file, chunk_size = 1048576):
    """
    # file.split_file(file, chunk_size=1048576)

    ---

    ### Overview
    Splits a file into smaller chunks of a specified size, preserving the original file. Each chunk is saved as a separate file named `{file}.fsp{index}`, where `index` is a zero-based integer (e.g., `file.fsp0`, `file.fsp1`). The chunk size is specified in bytes, defaulting to 1 MB.

    ### Parameters:
    - file (str): The path to the file to split.
    - chunk_size (int, optional): The size of each chunk in bytes. Defaults to 1048576 (1 MB).

    ### Returns:
    bool: `True` if the file was successfully split, `False` if the file does not exist.

    ### Raises:
    - IOError: If an I/O error occurs during file reading or writing.
    - PermissionError: If permission is denied when accessing the file or creating chunks.

    ### Examples:
    - Split a file into 1 MB chunks:

    ```python
    success = fsfile.split_file("large_file.bin")
    print("Split successful:", success)
    ```

    - Split a file into 500 KB chunks:

    ```python
    success = fsfile.split_file("large_file.bin", chunk_size=512000)
    print("Split successful:", success)
    ```
    """
    if exists(file) == False:
        return False

    with open(file, 'rb') as f:
        chunk = f.read(chunk_size)
        i = 0
        while chunk:
            with open(f'{file}.fsp{str(i)}', 'wb') as chunk_file:
                chunk_file.write(chunk)
            i += 1
            chunk = f.read(chunk_size)
    return True
