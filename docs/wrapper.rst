.. _wrapper-module:

Wrapper Module
==============

The Wrapper module is a comprehensive toolkit that provides a set of utility functions specifically designed to facilitate file and directory operations. These operations may include creating, reading, updating, and deleting files or directories. It is an integral part of the FileSystemPro library, designed to provide detailed information about files and directories, including functions for retrieving metadata and checking file extensions.

Features
--------

- **Metadata Retrieval**: Gathers comprehensive metadata about a file or directory path.
- **Extension Check**: Determines whether a file has an extension.

.. automodule:: filesystem.wrapper
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

The Wrapper module in FileSystemPro brings a comprehensive set of methods that streamline and enhance file and directory management.

.. code-block:: python

   from filesystem import wrapper as wra

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Method
     - Description
   * - wrapper.get_object(path)
     - This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).
   * - wrapper.has_extension(file_path)
     - Checks if the given file path has an extension. This function can return True or False based on the string, even if the file or directory does not exist.

Examples
--------

**Has Extension**

The following example checks if the given file path has an extension using **Wrapper**.

.. code-block:: python

   from filesystem import wrapper as wra

   bool_extension = wra.has_extension("/path/to/file.txt")
   print(bool_extension)

**Output**:

.. code-block:: text

   True

This will return **True** because the file has an extension (.txt).

.. code-block:: python

   from filesystem import wrapper as wra

   bool_extension = wra.has_extension("/path/to/file")
   print(bool_extension)

**Output**:

.. code-block:: text

   False

This will return **False** because the file does not have an extension.