"""
# Compression

---

## Overview
The Compression module is a module for creating, extracting, and reading compressed archive files
in both tar and zip formats.
It leverages Python's built-in `tarfile` and `zipfile` modules to handle these operations efficiently.

1. **Creating Archives:** The module provides functions to compress files and directories into tar or zip archives. It supports both single files and directories, as well as lists of files and directories.

2. **Extracting Archives:** It includes functions to extract files from tar or zip archives. Users can extract all contents or specify a list of files to extract.

3. **Reading Archives:** The module allows users to read the contents of tar or zip archives, listing all files contained within the archive.

### Tarfile Module

- **Functions**:
  1. **`create_tar(fullpath_files, destination)`**: Compresses a single file, directory, or a list of files/directories into a tar archive.
  2. **`extract(tar_filename, destination, extraction_list=[])`**: Extracts files from a tar archive to a specified destination. It can extract all files or a specified list of files.
  3. **`read_tar_archive(tar_filename)`**: Reads and lists the contents of a tar archive.

### Zipfile Module

- **Functions**:
  1. **`create_zip(fullpath_files, destination)`**: Compresses a single file, directory, or a list of files/directories into a zip archive.
  2. **`extract(zip_filename, destination, extraction_list=[])`**: Extracts files from a zip archive to a specified destination. It can extract all files or a specified list of files.
  3. **`read_zip_archive(zip_filename)`**: Reads and lists the contents of a zip archive.

This module is useful for managing compressed files, providing a unified interface for handling both tar and zip formats. It simplifies the process of archiving and extracting files, making it a valuable tool for data compression and archiving tasks.
"""

"""
# TarFile

---

## Overview
This module provides functions to create, extract, and read tar archives. It is designed to handle both single files and directories, making it versatile for various file compression and extraction needs.

## Features
- **Create Tar Archives:** Compress single files or directories into a tar archive.
- **Extract Tar Archives:** Extract all or specific files from a tar archive.
- **Read Tar Archives:** List the contents of a tar archive.


## Usage
To use these functions, simply import the module and call the desired function with appropriate parameters:

```python
import os
import tarfile

# Example: Creating a tar archive
create_tar('/path/to/file_or_directory', '/path/to/destination.tar')

# Example: Extracting from a tar archive
extract('/path/to/archive.tar', '/path/to/destination')

# Example: Reading a tar archive
contents = read_tar_archive('/path/to/archive.tar')
print(contents)
```
"""

"""
# ZipFile

---

## Overview
This module provides functions to create, extract, and read zip archives. It is designed to handle both single files and directories, making it versatile for various file compression and extraction needs.

## Features
- **Create Zip Archives:** Compress single files or directories into a zip archive.
- **Extract Zip Archives:** Extract all or specific files from a zip archive.
- **Read Zip Archives:** List the contents of a zip archive.

## Usage
To use these functions, simply import the module and call the desired function with appropriate parameters:

```python
import os
import zipfile

# Example: Creating a zip archive
create_zip('/path/to/file_or_directory', '/path/to/destination.zip')

# Example: Extracting from a zip archive
extract('/path/to/archive.zip', '/path/to/destination')

# Example: Reading a zip archive
contents = read_zip_archive('/path/to/archive.zip')
print(contents)
```
"""

# from . import tarfile
# from . import zipfile
import os
import tarfile as __tarfile__
import zipfile as __zipfile__

class TarFile():
  def create_tar(fullpath_files, destination):
    """
    # compression.create_tar(fullpath_files, destination)

    ---

    ### Overview
    Creates a tar archive at the specified destination path, compressing one or multiple files or directories provided in `fullpath_files`.

    ### Parameters:
    - **fullpath_files (str or list)**: The full path of a single file/directory or a list of files/directories to compress.
    - **destination (str)**: The destination path where the tar archive will be created.

    ### Returns:
    - **str**: A message indicating whether a single file/directory or a list of files/directories was compressed.

    ### Raises:
    - **FileNotFoundError**: If any of the specified files or directories do not exist.
    - **PermissionError**: If permission is denied for accessing the files or writing to the destination.
    - **ValueError**: If `fullpath_files` is neither a string nor a list.

    ### Examples:
    - Compresses a single file or directory into a tar archive.

    ```python
    create_tar("/path/to/file_or_directory", "/path/to/destination.tar")
    ```

    - Compresses multiple files or directories into a tar archive.

    ```python
    files_to_compress = ["/path/to/file1", "/path/to/file2", "/path/to/dir"]
    create_tar(files_to_compress, "/path/to/destination.tar")
    ```
    """
    def add_to_tar(tarf, path, base_path):
      if os.path.isfile(path):
        tarf.add(path, os.path.relpath(path, base_path))
      else:
        for root, _, files in os.walk(path):
          for file in files:
            file_path = os.path.join(root, file)
            tarf.add(file_path, os.path.relpath(file_path, base_path))

    if isinstance(fullpath_files, str):
      with __tarfile__.open(destination, 'w') as tarf:
        add_to_tar(tarf, fullpath_files, os.path.dirname(fullpath_files))
      return "ONLY ONE FILE OR DIRECTORY WAS COMPRESSED"

    if isinstance(fullpath_files, list):
      with __tarfile__.open(destination, 'w') as tarf:
        for item in fullpath_files:
          add_to_tar(tarf, item, os.path.dirname(item))
      return "A LIST OF FILE OR DIRECTORY WAS COMPRESSED"

  def extract(tar_filename, destination, extraction_list=[]):
    """
    # compression.extract(tar_filename, destination, extraction_list=[])

    ---

    ### Overview
    Extracts files from a tar archive to the specified destination directory. You can extract the entire archive or specify a list of files to extract.

    ### Parameters:
    - **tar_filename (str)**: The path of the tar archive to extract files from.
    - **destination (str)**: The directory where the files will be extracted.
    - **extraction_list (list, optional)**: A list of files or directories to extract. If empty, extracts all files. Defaults to an empty list.

    ### Returns:
    - **bool**: Returns `True` if extraction is successful, or `False` if a `KeyError` occurs.

    ### Raises:
    - **FileNotFoundError**: If the tar archive does not exist.
    - **KeyError**: If the specified file or directory is not found in the tar archive.
    - **Exception**: For any other errors that occur during the extraction process.

    ### Examples:
    - Extracts all files from a tar archive to the specified destination directory.

    ```python
    extract("/path/to/archive.tar", "/destination/directory")
    ```

    - Extracts specific files from a tar archive.

    ```python
    extract("/path/to/archive.tar", "/destination/directory", extraction_list=["file1.txt", "file2.txt"])
    ```
    """
    try:
      with __tarfile__.open(tar_filename, "r:*") as tar_file:
        if len(extraction_list) == 0:
          tar_file.extractall(destination)
          return True

        for item in extraction_list:
          if item in tar_file.getnames():
            tar_file.extract(item, destination)
          else:
            for i in tar_file.getnames():
              if i.startswith(item):
                tar_file.extract(i, destination)
        return True

    except FileNotFoundError:
      return "[FileSystem Pro]: File Not Found"
    except KeyError:
      return False
    except Exception as e:
      return f"[FileSystem Pro]: An error occurred.\nError: {e}"

  def read_tar_archive(tar_filename):
    """
    # compression.read_tar_archive(tar_filename)

    ---

    ### Overview
    Reads the contents of a tar archive and returns a list of the files within it.

    ### Parameters:
    - **tar_filename (str)**: The path of the tar archive to read.

    ### Returns:
    - **list**: A list of filenames contained in the tar archive.

    ### Raises:
    - **FileNotFoundError**: If the tar archive does not exist.
    - **Exception**: For any other errors that occur during the process.

    ### Examples:
    - Reads the contents of a tar archive.

    ```python
    read_tar_archive("/path/to/archive.tar")
    ```
    """
    try:
      with __tarfile__.open(tar_filename, "r") as tar_file:
        tar_contents_list = tar_file.getnames()
        return tar_contents_list
    except FileNotFoundError:
      return "[FileSystem Pro]: File Not Found"
    except Exception as e:
      return f"[FileSystem Pro]: An error occurred. Error: {e}"

class ZipFile():
  def add_to_zip(zip_path, files_to_add):
    with __zipfile__.ZipFile(zip_path, 'a') as zipf:
        if isinstance(files_to_add, str):
            zipf.write(files_to_add, os.path.basename(files_to_add))
        elif isinstance(files_to_add, list):
            for file in files_to_add:
                zipf.write(file, os.path.basename(file))
        else:
            raise ValueError("[filesystempro.compression.add_to_zip(zip_path, files_to_add)]: This function requires a string or a list of strings.")
  
  def create_zip(fullpath_files, destination):
    """
    # compression.zipfile.create_zip(fullpath_files, destination)

    ---
    
    ### Overview
    Creates a zip archive at the specified destination path, compressing one or multiple files or directories provided in `fullpath_files`.

    ### Parameters:
    - **fullpath_files (str or list)**: The full path of a single file/directory or a list of files/directories to compress.
    - **destination (str)**: The destination path where the zip archive will be created.

    ### Returns:
    - **str**: A message indicating whether a single file/directory or a list of files/directories was compressed.

    ### Raises:
    - **FileNotFoundError**: If any of the specified files or directories do not exist.
    - **PermissionError**: If the permission is denied for accessing the files or writing to the destination.
    - **ValueError**: If `fullpath_files` is neither a string nor a list.

    ### Examples:
    - Compresses a single file or directory into a zip archive.

    ```python
    create_zip("/path/to/file_or_directory", "/path/to/destination.zip")
    ```

    - Compresses multiple files or directories into a zip archive.

    ```python
    files_to_compress = ["/path/to/file1", "/path/to/file2", "/path/to/dir"]
    create_zip(files_to_compress, "/path/to/destination.zip")
    ```
    """
    def add_to_zip(zipf, path, base_path):
        if os.path.isfile(path):
            zipf.write(path, os.path.relpath(path, base_path))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, base_path))

    if isinstance(fullpath_files, str):
        with __zipfile__.ZipFile(destination, 'w') as zipf:
            add_to_zip(zipf, fullpath_files, os.path.dirname(fullpath_files))
        return "ONLY ONE FILE OR DIRECTORY WAS COMPRESSED"
    
    if isinstance(fullpath_files, list):
        with __zipfile__.ZipFile(destination, 'w') as zipf:
            for item in fullpath_files:
                add_to_zip(zipf, item, os.path.dirname(item))
        return "A LIST OF FILE OR DIRECTORY WAS COMPRESSED"
      
  def extract(zip_path, destination, extraction_list=None):
    """
    # compression.zipfile.extract(zip_path, destination, extraction_list=None)

    ---

    ### Overview
    Extracts files from a zip archive to the specified destination directory. You can extract the entire archive or specify a list of files to extract.

    ### Parameters:
    - **zip_path (str)**: The path of the zip archive from which to extract files.
    - **destination (str)**: The directory where the files will be extracted.
    - **extraction_list (None or list or str, optional)**: If `None`, extracts all files. If a list, extracts only the files specified in the list. If a string, extracts the file specified. Defaults to `None`.

    ### Returns:
    - **None**

    ### Raises:
    - **FileNotFoundError**: If the zip archive does not exist.
    - **PermissionError**: If permission is denied for reading the zip archive or writing to the destination.
    - **ValueError**: If `extraction_list` is not `None`, a list, or a string.

    ### Examples:
    - Extracts all files from a zip archive to the specified destination directory.

    ```python
    extract("/path/to/archive.zip", "/destination/directory")
    ```

    - Extracts specific files from a zip archive.

    ```python
    extract("/path/to/archive.zip", "/destination/directory", extraction_list=["file1.txt", "file2.txt"])
    ```

    - Extracts a single file from a zip archive.

    ```python
    extract("/path/to/archive.zip", "/destination/directory", extraction_list="file1.txt")
    ```
    """
    with __zipfile__.ZipFile(zip_path, 'r') as zip_ref:
        if extraction_list is None:
            zip_ref.extractall(destination)
        elif isinstance(extraction_list, list):
            for item in extraction_list:
                zip_ref.extract(item, destination)
        elif isinstance(extraction_list, str):
            zip_ref.extract(extraction_list, destination)
        else:
            raise ValueError("The parameter 'extraction_list' must be None, a list, or a string.")

  def read_zip_archive(zip_filename, show_compression_system_files=True):
    """
    # compression.zipfile.read_zip_archive(zip_filename, show_compression_system_files=True)

    ---
    
    ### Overview
    Reads the contents of a zip archive and returns a list of the files within it. You can choose to include or exclude compression system files (e.g., `__MACOSX/`, `.DS_Store`).

    ### Parameters:
    - **zip_filename (str)**: The path of the zip archive to read.
    - **show_compression_system_files (bool, optional)**: If `True`, includes compression system files in the list. Defaults to `True`.

    ### Returns:
    - **list**: A list of filenames contained in the zip archive.

    ### Raises:
    - **FileNotFoundError**: If the zip archive does not exist.
    - **Exception**: For any other errors that occur during the process.

    ### Examples:
    - Reads the contents of a zip archive and includes compression system files.

    ```python
    read_zip_archive("/path/to/archive.zip")
    ```

    - Reads the contents of a zip archive and excludes compression system files.

    ```python
    read_zip_archive("/path/to/archive.zip", show_compression_system_files=False)
    ```
    """
    try:
        with __zipfile__.ZipFile(zip_filename, "r") as zip_file:
            zip_contents_list = []
            all_contents_list = zip_file.namelist()
            for i in all_contents_list:
                if show_compression_system_files == True:
                    zip_contents_list.append(i)
                else:
                    if "__MACOSX/" not in i:
                        if ".DS_Store" not in i:
                            zip_contents_list.append(i)
            return zip_contents_list
    except FileNotFoundError:
        return "[FileSystem Pro]: File Not Found"
    except Exception as e:
        return f"[FileSystem Pro]: An error occurred. Error: {e}"

  def remove_from_zip(zip_path, files_to_remove):
      if isinstance(files_to_remove, str):
          files_to_remove = [files_to_remove]
      
      temp_zip = zip_path + "_temp.zip"
      with __zipfile__.ZipFile(zip_path, 'r') as zin, __zipfile__.ZipFile(temp_zip, 'w') as zout:
          for item in zin.infolist():
              if item.filename not in files_to_remove:
                  zout.writestr(item, zin.read(item.filename))
      os.replace(temp_zip, zip_path)

