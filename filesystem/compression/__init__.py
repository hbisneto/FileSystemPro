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

from . import tarfile
from . import zipfile