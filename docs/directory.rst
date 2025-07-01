.. _directory-module:

Directory Module
================

The Directory module is a component of the FileSystemPro library that provides a collection of functions for handling directory-related operations. It simplifies tasks such as path manipulation, directory creation and deletion, and file retrieval within directories, enhancing productivity and ensuring efficient directory management in applications.

Features
--------

- **Path Combination**: Dynamically combines multiple paths into a single path string.
- **Directory Creation**: Creates new directories, with an option to create necessary subdirectories.
- **Directory Deletion**: Deletes directories, with an option for recursive deletion.
- **Directory Existence Check**: Checks whether a directory exists at a specified path.
- **File Retrieval**: Retrieves a list of files within a directory using glob patterns.
- **Parent Directory Information**: Retrieves the name or path of a file's parent directory.
- **Directory Listing**: Lists all subdirectories within a given directory.
- **Directory Renaming**: Renames a directory if it exists.

.. automodule:: filesystem.directory
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

The Directory module in FileSystemPro brings a comprehensive set of methods that streamline and enhance directory management.

.. code-block:: python

   from filesystem import directory as dir

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Method
     - Description
   * - directory.combine(*args, paths=[])
     - Combines a list of paths or arguments into a single path. If the first argument or the first element in the paths list is not an absolute path, it raises a ValueError.
   * - directory.create(path, create_subdirs=True)
     - Creates a directory at the specified path. If `create_subdirs` is True, all intermediate-level directories needed to contain the leaf directory will be created. After the directory is created, it returns the details of the created directory.
   * - directory.delete(path, recursive=False)
     - Deletes a directory at the specified path. If `recursive` is True, the directory and all its contents will be removed.
   * - directory.exists(path)
     - Checks if a directory exists at the specified path.
   * - directory.get_directories(path, fullpath=True)
     - Create a list of directories within a specified path and returns either their full paths or just their names based on the **fullpath** parameter. Defaults to **True**.
   * - directory.get_name(path)
     - Retrieves the name of the directory of the specified path. If the path has an extension, it is assumed to be a file, and the parent directory name is returned. If the path does not have an extension, it is assumed to be a directory, and the directory name is returned.
   * - directory.get_parent(path)
     - Retrieves the parent directory from the specified path.
   * - directory.get_parent_name(path)
     - Retrieves the parent directory name from the specified path.
   * - directory.get_size(directory_path)
     - Calculates the total size of all files in the specified directory. The size is returned in bytes, KB, MB, GB, or TB, depending on the total size.
   * - directory.join(path1='', path2='', path3='', path4='', paths=[])
     - Joins multiple directory paths into a single path. The function ensures that each directory path ends with a separator before joining. If a directory path does not end with a separator, one is added.
   * - directory.move(source, destination, move_root=True)
     - The move function is designed to move files or directories from a source location to a destination. It provides flexibility by allowing you to specify whether intermediate-level subdirectories should be created during the move operation.
   * - directory.rename(old_path, new_path)
     - Renames a directory from the old directory path to the new directory path. If the old directory path does not exist or is not a directory, the function returns False.

Examples
--------

**Checking if a Directory Exists**

The following example checks whether a directory exists within the file system and prints the result using **Directory**.

.. code-block:: python

   import filesystem as fs
   from filesystem import directory as dir

   documents_exists = dir.exists(fs.documents)

   print(documents_exists)

**Output**:

.. code-block:: text

   True

**Listing directories inside a folder**

The following example shows how to list all directories in the specified path using **Directory**.

.. code-block:: python

   import filesystem as fs
   from filesystem import directory as dir

   folder_list = dir.get_directories(fs.documents)

   print(folder_list)

**Output**:

.. code-block:: text

   ['Work', 'School', 'PicsBackups', 'Office Documents']

**Renaming a folder**

The following example shows how to rename a folder using **Directory**.

.. code-block:: python

   import filesystem as fs
   from filesystem import directory as dir

   new_name = dir.rename(f'{fs.documents}/MyFolder', f'{fs.documents}/NewFolder')

   print(new_name)

**Output**:

.. code-block:: text

   True