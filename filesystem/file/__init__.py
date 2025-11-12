# -*- coding: utf-8 -*-
#
# filesystem/file/__init__.py
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
# File

---

## Overview
This module provides comprehensive file operations, including creation, reading, writing (text/binary), appending, copying/moving/renaming/deleting, integrity verification via SHA-256 checksums, timestamp management (creation/access/write in local/UTC), symbolic links, splitting/reassembling large files, and batch processing for duplicates/hashes/reports. It supports encoding options, overwrite controls, and returns metadata via `wrapper.get_object` where applicable. Cross-platform compatible with error handling for common issues like permissions and non-existence.

## Features
- **I/O Operations:** Create/append/read/write files (text/binary/lines), with encoding and buffer support.
- **Integrity Tools:** Calculate checksums, check against references, batch verify directories, find duplicates, generate/save/load hash reports.
- **Path & Metadata:** Get extension/filename/size (raw/formatted), enumerate files recursively, Unix mode.
- **Manipulation:** Copy/move/rename/delete, create symbolic links, split/reassemble files into chunks.
- **Timestamps:** Get/set creation/access/write times (local/UTC, as datetime/str; Unix approximations via utime).
- **Batch & Reporting:** Process multiple files/directories, log results, generate integrity reports.

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import file
```

### Examples:

- Append text to a file:

```python
file.append_text("example.txt", "Hello, World!")
# Appends without newline; creates if missing
```

- Calculate SHA-256 checksum:

```python
checksum = file.calculate_checksum("/path/to/file.txt")
print(f"Checksum: {checksum}")
```

- Copy multiple files with overwrite:

```python
files = ["/path/to/file1.txt", "/path/to/file2.txt"]
file.copy(files, "/destination/dir/", overwrite=True)
```

- Get formatted file size:

```python
size = file.get_size("/path/to/file.txt", show_unit=True)
print(size)  # e.g., "1.5 MB"
```

- Batch integrity check and report:

```python
results = file.batch_check_integrity("/path/to/directory", log_file="report.log")
report = file.generate_integrity_report(results, "summary.txt")
print(report)
```

- Split and reassemble a large file:

```python
file.split_file("large_file.bin", chunk_size=1024*1024)  # 1 MB chunks
file.reassemble_file("large_file", "reassembled.bin")  # Deletes chunks after
```

- Set last write time:

```python
from datetime import datetime
file.set_last_write_time("example.txt", datetime(2023, 1, 1))
```
"""

import codecs
import hashlib
import os
import shutil
import filesystem as fs
from filesystem import directory as dir
from filesystem import wrapper as wra
import datetime
import json
import logging

def append_all_bytes(file, data):
    """
    # file.append_all_bytes(file, data)

    ---

    ### Overview
    Appends the specified byte array to the end of the file at the given path. If the file does not exist, this method creates a new file.

    ### Parameters:
    - file (str): The path to the file.
    - data (bytes): The byte array to append to the file.

    ### Returns:
    None

    ### Raises:
    - IOError: If an I/O error occurs.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Append bytes to a file:

    ```python
    fsfile.append_all_bytes("example.bin", b"Hello, World!")
    ```
    """
    try:
        with open(file, 'ab') as f:
            f.write(data)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error appending bytes to {file}: {str(e)}")

def append_all_lines(file, lines, encoding="utf-8"):
    """
    # file.append_all_lines(file, lines, encoding="utf-8")

    ---

    ### Overview
    Appends lines to a file using the specified encoding, and then closes the file. If the file does not exist, this method creates a new file.

    ### Parameters:
    - file (str): The path to the file.
    - lines (list): The lines to append to the file.
    - encoding (str, optional): The encoding to use. Defaults to "utf-8".

    ### Returns:
    None

    ### Raises:
    - IOError: If an I/O error occurs.
    - PermissionError: If permission is denied when accessing the file.
    - UnicodeEncodeError: If the lines cannot be encoded with the specified encoding.

    ### Examples:
    - Append lines to a file:

    ```python
    fsfile.append_all_lines("example.txt", ["Line 1", "Line 2"])
    ```
    """
    try:
        with codecs.open(file, 'a', encoding=encoding) as f:
            for line in lines:
                f.write(f"{line}\n")
    except (IOError, PermissionError, UnicodeEncodeError) as e:
        raise IOError(f"Error appending lines to {file}: {str(e)}")

def append_all_text(file, content, encoding="utf-8"):
    """
    # file.append_all_text(file, content, encoding="utf-8")

    ---

    ### Overview
    Appends the specified string to the file using the specified encoding, creating the file if it does not exist.

    ### Parameters:
    - file (str): The path to the file.
    - content (str): The string to append to the file.
    - encoding (str, optional): The encoding to use. Defaults to "utf-8".

    ### Returns:
    None

    ### Raises:
    - IOError: If an I/O error occurs.
    - PermissionError: If permission is denied when accessing the file.
    - UnicodeEncodeError: If the content cannot be encoded with the specified encoding.

    ### Examples:
    - Append text to a file:

    ```python
    fsfile.append_all_text("example.txt", "Hello, World!")
    ```
    """
    try:
        with codecs.open(file, 'a', encoding=encoding) as f:
            f.write(content)
    except (IOError, PermissionError, UnicodeEncodeError) as e:
        raise IOError(f"Error appending text to {file}: {str(e)}")

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

def batch_check_integrity(paths, reference_hashes=None, log_file="integrity_report.log"):
    """
    # file.batch_check_integrity(paths, reference_hashes=None, log_file="integrity_report.log")

    ---

    ### Overview
    Performs batch integrity verification on multiple files or directories using SHA-256 checksums.
    Supports verification against reference hashes if provided, and logs results to a specified log file.

    ### Parameters:
    - paths (str or list): A single path or list of paths to files or directories to verify.
    - reference_hashes (dict, optional): A dictionary mapping file paths to their reference SHA-256 hashes. Defaults to None.
    - log_file (str, optional): Path to the log file for recording verification results. Defaults to "integrity_report.log".

    ### Returns:
    dict: A dictionary containing verification results with the following keys:    
    - timestamp: ISO format timestamp of when the verification was performed
    - total_files: Total number of files checked
    - successful: Number of files with verified integrity
    - failed: Number of files that failed verification or encountered errors
    - errors: List of error messages
    - file_details: Dictionary mapping file paths to their verification details

    ### Raises:
    - FileNotFoundError: If a specified file or directory does not exist.
    - PermissionError: If permission is denied when accessing a file or directory.
    - IOError: If there is an error reading a file during checksum calculation.

    ### Examples:
    - Verify integrity of files in a directory without reference hashes:

    ```python
    results = batch_check_integrity("/path/to/directory")
    ```

    - Verify integrity of multiple files against reference hashes:

    ```python
    ref_hashes = {"/path/to/file1.txt": "hash1", "/path/to/file2.txt": "hash2"}
    results = batch_check_integrity(["/path/to/file1.txt", "/path/to/file2.txt"], ref_hashes)
    ```
    """

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    results = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_files": 0,
        "successful": 0,
        "failed": 0,
        "errors": [],
        "file_details": {}
    }

    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        try:
            if dir.exists(path):
                files = get_files(path, fullpath=True)
            else:
                files = [path] if exists(path) else []
                if not files:
                    raise FileNotFoundError(f"Path '{path}' does not exist.")

            for file_path in files:
                results["total_files"] += 1
                try:
                    current_hash = calculate_checksum(file_path)
                    file_info = {
                        "size": get_size(file_path),
                        "last_modified": datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                        "current_hash": current_hash,
                        "status": "OK"
                    }

                    if reference_hashes and file_path in reference_hashes:
                        file_info["reference_hash"] = reference_hashes[file_path]
                        file_info["status"] = "OK" if current_hash == reference_hashes[file_path] else "CORRUPTED"

                    results["file_details"][file_path] = file_info
                    results["successful" if file_info["status"] == "OK" else "failed"] += 1
                    logging.info(f"Verified {file_path}: {file_info['status']}")

                except (IOError, PermissionError) as e:
                    error_msg = f"Error processing {file_path}: {str(e)}"
                    results["errors"].append(error_msg)
                    results["failed"] += 1
                    logging.error(error_msg)

        except FileNotFoundError as e:
            error_msg = str(e)
            results["errors"].append(error_msg)
            results["failed"] += 1
            logging.error(error_msg)
        except PermissionError as e:
            error_msg = f"Permission denied for {path}: {str(e)}"
            results["errors"].append(error_msg)
            results["failed"] += 1
            logging.error(error_msg)

    return results

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

def create_symbolic_link(file_target, file_link):
    """
    # file.create_symbolic_link(file_target, file_link)

    ---

    ### Overview
    Creates a file symbolic link identified by file_link that points to file_target.

    ### Parameters:
    - file_target (str): The path to the target file or directory.
    - file_link (str): The path to the symbolic link.

    ### Returns:
    A dictionary with information about the created symbolic link.

    ### Raises:
    - FileNotFoundError: If the target path does not exist.
    - OSError: If an error occurs while creating the symbolic link.
    - PermissionError: If permission is denied.

    ### Examples:
    - Create a symbolic link:

    ```python
    fsfile.create_symbolic_link("target.txt", "link.txt")
    ```
    """
    try:
        if not os.path.exists(file_target):
            raise FileNotFoundError(f"Target path '{file_target}' does not exist.")
        os.symlink(file_target, file_link)
        return wra.get_object(file_link)
    except (OSError, PermissionError) as e:
        raise OSError(f"Error creating symbolic link {file_link} to {file_target}: {str(e)}")

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

def generate_integrity_report(results, output_file=None):
    """
    # file.generate_integrity_report(results, output_file=None)

    ---

    ### Overview
    Generates a detailed report of batch integrity verification results, optionally saving it to a file.

    ### Parameters:
    - results (dict): The results dictionary returned by `batch_check_integrity`.
    - output_file (str, optional): Path to save the report. If None, the report is only returned as a string. Defaults to None.

    ### Returns:
    str: The formatted report as a string.

    ### Raises:
    - PermissionError: If permission is denied when writing to the output file.
    - IOError: If there is an error writing to the output file.

    ### Examples:
    - Generate a report and print it:

    ```python
    results = batch_check_integrity("/path/to/directory")
    report = generate_integrity_report(results)
    print(report)
    ```

    - Generate a report and save it to a file:

    ```python
    results = batch_check_integrity("/path/to/directory")
    generate_integrity_report(results, "integrity_report.txt")
    ```
    """
    report = [
        "=" * 50,
        f"Integrity Report - {results['timestamp']}",
        "=" * 50,
        f"Total files verified: {results['total_files']}",
        f"Files with integrity: {results['successful']}",
        f"Files with issues: {results['failed']}",
        "\nFile Details:"
    ]

    for file_path, details in results["file_details"].items():
        report.append(f"\nFile: {file_path}")
        report.append(f"Size: {details['size']}")
        report.append(f"Last Modified: {details['last_modified']}")
        report.append(f"SHA-256 Hash: {details['current_hash']}")
        if "reference_hash" in details:
            report.append(f"Reference Hash: {details['reference_hash']}")
        report.append(f"Status: {details['status']}")

    if results["errors"]:
        report.append("\nErrors Encountered:")
        for error in results["errors"]:
            report.append(f"- {error}")

    report_text = "\n".join(report)

    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(report_text)
        except (IOError, PermissionError) as e:
            raise IOError(f"Error writing report to {output_file}: {str(e)}")

    return report_text

def get_creation_time(file):
    """
    # file.get_creation_time(file)

    ---

    ### Overview
    Returns the creation date and time of the specified file or directory.

    ### Parameters:
    - file (str): The path to the file or directory.

    ### Returns:
    datetime: The creation date and time of the file or directory.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get creation time of a file:

    ```python
    creation_time = fsfile.get_creation_time("example.txt")
    print(creation_time)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        return datetime.datetime.fromtimestamp(stat_info.st_ctime)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting creation time for {file}: {str(e)}")

def get_creation_time_utc(file):
    """
    # file.get_creation_time_utc(file)

    ---

    ### Overview
    Returns the creation date and time, in Coordinated Universal Time (UTC), of the specified file or directory.

    ### Parameters:
    - file (str): The path to the file or directory.

    ### Returns:
    datetime: The creation date and time in UTC.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get UTC creation time of a file:

    ```python
    creation_time_utc = fsfile.get_creation_time_utc("example.txt")
    print(creation_time_utc)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        return datetime.datetime.utcfromtimestamp(stat_info.st_ctime)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting UTC creation time for {file}: {str(e)}")

def get_last_access_time(file):
    """
    # file.get_last_access_time(file)

    ---

    ### Overview
    Returns the date and time the specified file or directory was last accessed.

    ### Parameters:
    - file (str): The path to the file or directory.

    ### Returns:
    datetime: The last access date and time of the file or directory.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get last access time of a file:

    ```python
    access_time = fsfile.get_last_access_time("example.txt")
    print(access_time)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        return datetime.datetime.fromtimestamp(stat_info.st_atime)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting last access time for {file}: {str(e)}")

def get_last_access_time_utc(file):
    """
    # file.get_last_access_time_utc(file)

    ---

    ### Overview
    Returns the last access date and time, in Coordinated Universal Time (UTC), of the specified file or directory.

    ### Parameters:
    - file (str): The path to the file or directory.

    ### Returns:
    datetime: The last access date and time in UTC.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get UTC last access time of a file:

    ```python
    access_time_utc = fsfile.get_last_access_time_utc("example.txt")
    print(access_time_utc)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        return datetime.datetime.utcfromtimestamp(stat_info.st_atime)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting UTC last access time for {file}: {str(e)}")

def get_last_write_time(file):
    """
    # file.get_last_write_time(file)

    ---

    ### Overview
    Returns the date and time the specified file or directory was last written to.

    ### Parameters:
    - file (str): The path to the file or directory.

    ### Returns:
    datetime: The last write date and time of the file or directory.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get last write time of a file:

    ```python
    write_time = fsfile.get_last_write_time("example.txt")
    print(write_time)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        return datetime.datetime.fromtimestamp(stat_info.st_mtime)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting last write time for {file}: {str(e)}")

def get_last_write_time_utc(file):
    """
    # file.get_last_write_time_utc(file)

    ---

    ### Overview
    Returns the last write date and time, in Coordinated Universal Time (UTC), of the specified file or directory.

    ### Parameters:
    - file (str): The path to the file or directory.

    ### Returns:
    datetime: The last write date and time in UTC.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get UTC last write time of a file:

    ```python
    write_time_utc = fsfile.get_last_write_time_utc("example.txt")
    print(write_time_utc)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        return datetime.datetime.utcfromtimestamp(stat_info.st_mtime)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting UTC last write time for {file}: {str(e)}")

def get_unix_file_mode(file, octal=False):
    """
    # file.get_unix_file_mode(file)

    ---

    ### Overview
    Gets the Unix file mode of the file on the path.

    ### Parameters:
    - file (str): The path to the file.
    - octal (bool, optional): If True, returns the mode in octal format. Defaults to False.

    ### Returns:
    int: The Unix file mode (permissions) of the file.

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.

    ### Examples:
    - Get Unix file mode of a file:

    ```python
    mode = fsfile.get_unix_file_mode("example.txt")
    print(mode)
    ```

    - Get Unix file mode in octal format:
    ```python
    mode_octal = fsfile.get_unix_file_mode("example.txt", octal=True)
    print(mode_octal)
    ```
    """
    try:
        if not exists(file):
            raise FileNotFoundError(f"File '{file}' does not exist.")
        stat_info = os.stat(file)
        if octal:
            return oct(stat_info.st_mode)
        return stat_info.st_mode
    except (IOError, PermissionError) as e:
        raise IOError(f"Error getting Unix file mode for {file}: {str(e)}")

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

def load_reference_hashes(input_file):
    """
    # file.load_reference_hashes(input_file)

    ---

    ### Overview
    Loads SHA-256 checksums from a JSON file for use in integrity verification.

    ### Parameters:
    - input_file (str): Path to the JSON file containing the reference hashes.

    ### Returns:
    dict: A dictionary mapping file paths to their reference SHA-256 hashes.

    ### Raises:
    - FileNotFoundError: If the input file does not exist.
    - PermissionError: If permission is denied when reading the input file.
    - IOError: If there is an error reading the input file or parsing the JSON.

    ### Examples:
    - Load reference hashes from a JSON file:

    ```python
    ref_hashes = load_reference_hashes("hashes.json")
    ```
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Reference hash file '{input_file}' does not exist.")
    except (IOError, PermissionError) as e:
        raise IOError(f"Error reading reference hashes from {input_file}: {str(e)}")
    except json.JSONDecodeError as e:
        raise IOError(f"Invalid JSON format in {input_file}: {str(e)}")

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

def save_reference_hashes(paths, output_file):
    """
    # file.save_reference_hashes(paths, output_file)

    ---

    ### Overview
    Calculates SHA-256 checksums for specified files or directories and saves them to a JSON file.
    The resulting file can be used as a reference for integrity verification.

    ### Parameters:
    - paths (str or list): A single path or list of paths to files or directories to calculate hashes for.
    - output_file (str): Path to the JSON file where the hashes will be saved.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If a specified file or directory does not exist.
    - PermissionError: If permission is denied when accessing a file or directory or writing to the output file.
    - IOError: If there is an error writing to the output file.

    ### Examples:
    - Save hashes for a directory:

    ```python
    save_reference_hashes("/path/to/directory", "hashes.json")
    ```

    - Save hashes for multiple files:

    ```python
    save_reference_hashes(["/path/to/file1.txt", "/path/to/file2.txt"], "hashes.json")
    ```
    """
    hashes = {}
    
    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        try:
            if dir.exists(path):
                files = get_files(path, fullpath=True)
            else:
                files = [path] if exists(path) else []
                if not files:
                    raise FileNotFoundError(f"Path '{path}' does not exist.")

            for file_path in files:
                try:
                    hash_value = calculate_checksum(file_path)
                    hashes[file_path] = hash_value
                except (IOError, PermissionError) as e:
                    logging.error(f"Error calculating hash for {file_path}: {str(e)}")

        except FileNotFoundError as e:
            logging.error(str(e))
        except PermissionError as e:
            logging.error(f"Permission denied for {path}: {str(e)}")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(hashes, f, indent=2)
    except (IOError, PermissionError) as e:
        raise IOError(f"Error writing hashes to {output_file}: {str(e)}")

def set_creation_time(file, creation_time):
    """
    # file.set_creation_time(file, creation_time)

    ---

    ### Overview
    Sets the modification time of the specified file as an approximation of the creation time, since Python's standard library does not directly support setting creation time on Unix systems. The creation time can be provided as a datetime object or a string in the format "YYYY-MM-DD HH:MM:SS".

    ### Parameters:
    - file (str): The path to the file.
    - creation_time (datetime or str): The creation time to set, either as a datetime object or a string in "YYYY-MM-DD HH:MM:SS" format.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.
    - OSError: If an error occurs while setting the modification time.
    - ValueError: If the creation time string is not in the correct format.

    ### Examples:
    - Set the modification time of a file using a datetime object:

    ```python
    from datetime import datetime
    fsfile.set_creation_time("example.txt", datetime(2023, 1, 1, 12, 0))
    ```

    - Set the modification time using a string:

    ```python
    fsfile.set_creation_time("example.txt", "2023-01-01 12:00:00")
    ```
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    
    # Note: Setting creation time is not directly supported in Python's standard library.
    # This is a limitation, as os.utime only sets access and modification times.
    # For Unix, we can approximate by setting modification time as a fallback.
    if not type(creation_time) == datetime.datetime:
        creation_time = datetime.datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S")
    os.utime(file, (os.path.getatime(file), creation_time.timestamp()))

def set_creation_time_utc(file, creation_time_utc):
    """
    # file.set_creation_time_utc(file, creation_time_utc)

    ---

    ### Overview
    Sets the modification time of the specified file in Coordinated Universal Time (UTC) as an approximation of the creation time, since Python's standard library does not directly support setting creation time on Unix systems. The time is converted to local time before setting. The creation time can be provided as a datetime object or a string in the format "YYYY-MM-DD HH:MM:SS".

    ### Parameters:
    - file (str): The path to the file.
    - creation_time_utc (datetime or str): The creation time in UTC, either as a datetime object or a string in "YYYY-MM-DD HH:MM:SS" format.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.
    - OSError: If an error occurs while setting the modification time.
    - ValueError: If the creation time string is not in the correct format.

    ### Examples:
    - Set the UTC modification time of a file using a datetime object:

    ```python
    from datetime import datetime
    fsfile.set_creation_time_utc("example.txt", datetime(2023, 1, 1, 12, 0))
    ```

    - Set the UTC modification time using a string:

    ```python
    fsfile.set_creation_time_utc("example.txt", "2023-01-01 12:00:00")
    ```
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    if not type(creation_time_utc) == datetime.datetime:
        creation_time_utc = datetime.datetime.strptime(creation_time_utc, "%Y-%m-%d %H:%M:%S")
    local_time = creation_time_utc.timestamp() - datetime.datetime.now().astimezone().utcoffset().total_seconds()
    os.utime(file, (os.path.getatime(file), local_time))

def set_last_access_time(file, last_access_time):
    """
    # file.set_last_access_time(file, last_access_time)

    ---

    ### Overview
    Sets the last access time of the specified file. The access time can be provided as a datetime object or a string in the format "YYYY-MM-DD HH:MM:SS". The file's modification time remains unchanged.

    ### Parameters:
    - file (str): The path to the file.
    - last_access_time (datetime or str): The last access time to set, either as a datetime object or a string in "YYYY-MM-DD HH:MM:SS" format.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.
    - OSError: If an error occurs while setting the access time.
    - ValueError: If the access time string is not in the correct format.

    ### Examples:
    - Set the last access time of a file using a datetime object:

    ```python
    from datetime import datetime
    fsfile.set_last_access_time("example.txt", datetime(2023, 1, 1, 12, 0))
    ```

    - Set the last access time using a string:

    ```python
    fsfile.set_last_access_time("example.txt", "2023-01-01 12:00:00")
    ```
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    if not type(last_access_time) == datetime.datetime:
        last_access_time = datetime.datetime.strptime(last_access_time, "%Y-%m-%d %H:%M:%S")
    os.utime(file, (last_access_time.timestamp(), os.path.getmtime(file)))

def set_last_access_time_utc(file, last_access_time_utc):
    """
    # file.set_last_access_time_utc(file, last_access_time_utc)

    ---

    ### Overview
    Sets the last access time of the specified file in Coordinated Universal Time (UTC). The time is converted to local time before setting. The access time can be provided as a datetime object or a string in the format "YYYY-MM-DD HH:MM:SS". The file's modification time remains unchanged.

    ### Parameters:
    - file (str): The path to the file.
    - last_access_time_utc (datetime or str): The last access time in UTC, either as a datetime object or a string in "YYYY-MM-DD HH:MM:SS" format.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.
    - OSError: If an error occurs while setting the access time.
    - ValueError: If the access time string is not in the correct format.

    ### Examples:
    - Set the UTC last access time of a file using a datetime object:

    ```python
    from datetime import datetime
    fsfile.set_last_access_time_utc("example.txt", datetime(2023, 1, 1, 12, 0))
    ```

    - Set the UTC last access time using a string:

    ```python
    fsfile.set_last_access_time_utc("example.txt", "2023-01-01 12:00:00")
    ```
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    if not type(last_access_time_utc) == datetime.datetime:
        last_access_time_utc = datetime.datetime.strptime(last_access_time_utc, "%Y-%m-%d %H:%M:%S")
    local_time = last_access_time_utc.timestamp() - datetime.datetime.now().astimezone().utcoffset().total_seconds()
    os.utime(file, (local_time, os.path.getmtime(file)))

def set_last_write_time(file, last_write_time):
    """
    # file.set_last_write_time(file, last_write_time)

    ---

    ### Overview
    Sets the last write (modification) time of the specified file. The write time can be provided as a datetime object or a string in the format "YYYY-MM-DD HH:MM:SS". The file's access time remains unchanged.

    ### Parameters:
    - file (str): The path to the file.
    - last_write_time (datetime or str): The last write time to set, either as a datetime object or a string in "YYYY-MM-DD HH:MM:SS" format.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.
    - OSError: If an error occurs while setting the write time.
    - ValueError: If the write time string is not in the correct format.

    ### Examples:
    - Set the last write time of a file using a datetime object:

    ```python
    from datetime import datetime
    fsfile.set_last_write_time("example.txt", datetime(2023, 1, 1, 12, 0))
    ```

    - Set the last write time using a string:

    ```python
    fsfile.set_last_write_time("example.txt", "2023-01-01 12:00:00")
    ```
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    if not type(last_write_time) == datetime.datetime:
        last_write_time = datetime.datetime.strptime(last_write_time, "%Y-%m-%d %H:%M:%S")
    os.utime(file, (os.path.getatime(file), last_write_time.timestamp()))

def set_last_write_time_utc(file, last_write_time_utc):
    """
    # file.set_last_write_time_utc(file, last_write_time_utc)

    ---

    ### Overview
    Sets the last write (modification) time of the specified file in Coordinated Universal Time (UTC). The time is converted to local time before setting. The write time can be provided as a datetime object or a string in the format "YYYY-MM-DD HH:MM:SS". The file's access time remains unchanged.

    ### Parameters:
    - file (str): The path to the file.
    - last_write_time_utc (datetime or str): The last write time in UTC, either as a datetime object or a string in "YYYY-MM-DD HH:MM:SS" format.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If permission is denied when accessing the file.
    - OSError: If an error occurs while setting the write time.
    - ValueError: If the write time string is not in the correct format.

    ### Examples:
    - Set the UTC last write time of a file using a datetime object:

    ```python
    from datetime import datetime
    fsfile.set_last_write_time_utc("example.txt", datetime(2023, 1, 1, 12, 0))
    ```

    - Set the UTC last write time using a string:

    ```python
    fsfile.set_last_write_time_utc("example.txt", "2023-01-01 12:00:00")
    ```
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    if not type(last_write_time_utc) == datetime.datetime:
        last_write_time_utc = datetime.datetime.strptime(last_write_time_utc, "%Y-%m-%d %H:%M:%S")
    local_time = last_write_time_utc.timestamp() - datetime.datetime.now().astimezone().utcoffset().total_seconds()
    os.utime(file, (os.path.getatime(file), local_time))

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