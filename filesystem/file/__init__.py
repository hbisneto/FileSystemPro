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

def append_text(file, text):
    """
    # file.append_text(file, text)

    ---
    
    ### Overview
    Appends UTF-8 encoded text to an existing file, or creates a new file if it does not exist.

    ### Parameters:
    - file_path (str): The path to the file.
    - text (str): The text to append to the file.

    ### Returns:
    None

    ### Raises:
    - IOError: If an I/O error occurs

    ### Examples:
    - Appends text to a file, creating the file if it does not exist.

    ```python
    append_text('example.txt', 'This is a sample text.')
    ```
    """
    with open(file, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

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
        # Read and update hash in chunks of 4K
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

def create(file, data, encoding="utf-8"):
    """
    # file.create(file, data, encoding="utf-8")

    ---
    
    ### Overview
    Creates a file at the specified path and writes data into it. If the file already exists, 
    its contents are overwritten. The function then returns the details of the created file.

    ### Parameters:
    file (str): The file path to create.
    data (str): The data to write into the file.
    encoding (str): The encoding to use when opening the file. Defaults to "utf-8".

    ### Returns:
    dict: A dictionary containing the details of the created file.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If the permission is denied.
    - UnicodeEncodeError: If the data cannot be encoded with the specified encoding.

    ### Examples:
    - Creates a file and writes data into it, then returns the file details.

    ```python
    create("/path/to/file", "Hello, World!")
    ```
    - Creates a file with a different encoding, writes data into it, then returns the file details.

    ```python
    create("/path/to/file", "Hello, World!", "utf-16")
    ```
    """
    try:
        with codecs.open(f'{file}', "w", encoding=encoding) as custom_file:
            custom_file.write(data)
    except:
        pass
    return wra.get_object(f'{file}')

def create_binary_file(filename, data):
    """
    # file.create_binary_file(filename, data)

    ---
    
    ### Overview
    Creates a binary file at the specified filename and writes data into it. If the data is not of bytes type,
    it is first encoded to bytes.

    ### Parameters:
    - filename (str): The filename of the binary file to create.
    - data (str or bytes): The data to write into the file. If it is a string, it will be encoded to bytes.

    ### Returns:
    None

    ### Raises:
    - FileExistsError: If the file already exists.
    - PermissionError: If the permission is denied.
    - UnicodeEncodeError: If the data cannot be encoded to bytes.

    ### Examples:
    - Creates a binary file and writes string data into it, which is first encoded to bytes.

    ```python
    create_binary_file("/path/to/file", "Hello, World!")
    ```
    - Creates a binary file and writes byte data into it.

    ```python
    create_binary_file("/path/to/file", b"Hello, World!")
    ```
    """
    if type(data) != bytes:
        b_data = bytes(data.encode())
        with open(filename, 'wb') as binary_file:
            binary_file.write(b_data)
    else:
        with open(filename, 'wb') as binary_file:
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
    if exists(file):
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
    - FileNotFoundError: If the file does not exist.
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

def get_extension(file_path, lower=True):
    """
    # file.get_extension(file_path, lower=True)

    ---
    
    ### Overview
    Extracts the file extension from the given file path and returns it in lowercase or uppercase based on the `lower` parameter.

    ### Parameters:
    file_path (str): The path of the file from which to extract the extension.
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

    _, file_extension = os.path.splitext(file_path)
    if lower == True:
        return file_extension.lower()
    return file_extension.upper()

def get_files(path, fullpath=False, extension=None):
    """
    # file.get_files(path, fullpath=False, extension=None)

    ---

    ### Overview
    Retrieves a list of files from the specified directory. Optionally, it can return the full path of each file and filter files by their extension.

    ### Parameters:
    - path (str): The directory path to search for files.
    - fullpath (bool, optional): If True, returns the full path of each file. Defaults to False.
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
    - UnicodeEncodeError: If the data cannot be encoded with the specified encoding.

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

    ### Parameters:
    old_name (str): The current name of the file.
    new_name (str): The new name for the file.

    ### Returns:
    bool: True if the file was successfully renamed, False otherwise.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
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

    ### Parameters:
    large_file (str): The name of the original large file that was split.
    new_file (str): The name for the new file that will be created from the parts.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If any of the parts do not exist.
    - PermissionError: If the permission is denied.

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
    # file.split_file(file, chunk_size = 1048576)

    ---
    
    ### Overview
    Splits a large file into smaller chunks. The function reads the file in chunks of a specified size and writes each chunk to a new file. The new files are named by appending `.fsp` and an index number to the original filename.

    ### Parameters:
    file (str): The name of the file to split.
    chunk_size (int): The size of each chunk. Defaults to 1048576 bytes (1 MB).

    ### Returns:
    True if the file was successfully split, False if the file does not exist.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If the permission is denied.

    ### Examples:
    - Splits a file into 1 MB chunks.

    ```python
    split_file("large_file")
    ```
    - Splits a file into chunks of a specified size.

    ```python
    split_file("large_file", 512000)  # splits into 500 KB chunks
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

