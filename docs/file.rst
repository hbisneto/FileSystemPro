.. _file-module:

File Module
===========

The File module provides functions for handling file operations, such as integrity checks, file creation, deletion, enumeration, and file splitting/reassembling.

**Features**:
- Checksum calculation using SHA-256
- File creation, deletion, and renaming
- File splitting and reassembling
- File enumeration and existence checks

.. automodule:: filesystem.file
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Checking File Integrity**

.. code-block:: python

   from filesystem import file as fsfile

   integrity = fsfile.check_integrity("/path/to/file", "/path/to/reference_file")
   print("Files are identical:", integrity)

**Output**:

.. code-block:: text

   Files are identical: True