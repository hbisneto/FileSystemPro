.. _compression-module:

Compression Module
==================

The Compression module is responsible for creating, extracting, and reading compressed archive files in tar and zip formats. It leverages Python's built-in `tarfile` and `zipfile` modules to handle these operations efficiently.

**Features**
------------

The Compression module offers robust and versatile tools for managing file compression and extraction, whether you prefer the tar or zip format.

- **Create Tar Archive**: Compresses a single file, directory, or a list of files and directories into a tar archive, bundling them into a single file for easier management and transport.
- **Extract Tar Archive**: Extracts files from a tar archive to a specified destination, with options to extract all files or a specified list, providing flexibility in handling archive contents.
- **Read Tar Archive**: Reads and lists the contents of a tar archive without extracting them, allowing you to inspect files and directories before extraction.
- **Create Zip Archive**: Compresses a single file, directory, or a list of files and directories into a zip archive, similar to tar but in a different format.
- **Extract Zip Archive**: Extracts files from a zip archive to a specified destination, with options to extract all files or a specified list.
- **Read Zip Archive**: Reads and lists the contents of a zip archive without extracting them, providing a convenient way to inspect files and directories.

**TarFile**
~~~~~~~~~~~

The TarFile module provides tools for managing file compression and extraction in tar format, making it an essential tool for efficient file management.

**ZipFile**
~~~~~~~~~~~

The ZipFile module provides tools for managing file compression and extraction in zip format, offering robust functionality for efficient file management.

**Methods**
-----------

.. code-block:: python

   from filesystem import compression

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Method
     - Description
   * - :code:`compression.tarfile.create_tar(fullpath_files, destination)`
     - Compresses files or directories into a TAR file. Returns a message indicating whether a single file/directory or a list of files/directories was compressed.
   * - :code:`compression.tarfile.extract(tar_filename, destination, extraction_list=[])`
     - Extracts files from a tar archive. It can extract all files or a specified list of files. Returns :code:`True` if successful, :code:`"[FileSystem Pro]: File Not Found"` if the tar file is not found, :code:`False` if a specified item in :code:`extraction_list` is not found, or an :code:`Error Message` if any other error occurs.
   * - :code:`compression.tarfile.read_tar_archive(tar_filename)`
     - Reads the contents of a TAR archive file and returns a list of the names of the files contained within it.
   * - :code:`compression.zipfile.create_zip(fullpath_files, destination)`
     - Compresses files or directories into a ZIP file. Returns a message indicating whether a single file/directory or a list of files/directories was compressed.
   * - :code:`compression.zipfile.extract(zip_path, destination, extraction_list=None)`
     - Reads the contents of a ZIP file and extracts files based on the provided parameters.
   * - :code:`compression.zipfile.read_zip_archive(zip_filename, show_compression_system_files=True)`
     - Reads the contents of a ZIP file and returns a list of the names of the files contained within it.

**API Reference**
-----------------

**TarFile**

.. automodule:: filesystem.compression.tarfile
   :members:
   :undoc-members:
   :show-inheritance:

**ZipFile**

.. automodule:: filesystem.compression.zipfile
   :members:
   :undoc-members:
   :show-inheritance:

**Examples**
------------

**TarFile Sample Codes**

*Creating a Tar Archive*

.. code-block:: python

   from filesystem import compression
   compression.tarfile.create_tar('/path/to/file_or_directory', '/path/to/destination.tar')

*Extracting from a Tar Archive*

.. code-block:: python

   from filesystem import compression
   compression.tarfile.extract('/path/to/archive.tar', '/path/to/destination')

*Reading a Tar Archive*

.. code-block:: python

   from filesystem import compression
   contents = compression.tarfile.read_tar_archive('/path/to/archive.tar')
   print(contents)

**ZipFile Sample Codes**

*Creating a Zip Archive*

.. code-block:: python

   from filesystem import compression
   compression.zipfile.create_zip('/path/to/file_or_directory', '/path/to/destination.zip')

*Extracting from a Zip Archive*

.. code-block:: python

   from filesystem import compression
   compression.zipfile.extract('/path/to/archive.zip', '/path/to/destination')

*Reading a Zip Archive*

.. code-block:: python

   from filesystem import compression
   contents = compression.zipfile.read_zip_archive('/path/to/archive.zip')
   print(contents)