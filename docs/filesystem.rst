.. _filesystem-module:

FileSystem Module
=================

The FileSystem module provides a comprehensive suite of methods for managing and interacting with various directories and user folders across multiple operating systems. It intelligently identifies the user's operating system—Linux, macOS, or Windows—and configures file paths for essential directories like Desktop, Documents, Downloads, Music, Pictures, Public, and Videos. Leveraging Python's built-in libraries such as `os`, `sys`, and `getpass`, it ensures cross-platform compatibility and accurate path retrieval. For Windows environments, it uses the `winreg` module to query the Windows registry, ensuring the paths to these directories are accurately retrieved based on the system's registry settings.

**Features**
-----------

- **Cross-platform Compatibility**: Works on Linux, macOS, and Windows, making it versatile and adaptable to different environments.
- **Directory Path Identification**: Identifies and defines paths to common user directories such as Desktop, Documents, Downloads, Music, Pictures, Public, and Videos.
- **String Formatting**: Uses f-string formatting to create directory paths.
- **Registry-Based Path Retrieval**: On Windows, uses the `winreg` module to retrieve accurate paths from the Windows registry for folders like Home, Desktop, Documents, Downloads, Music, Pictures, Public, and Videos.

**Methods**
----------

.. code-block:: python

   import filesystem as fs

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Method
     - Description
   * - CURRENT_LOCATION
     - Creates a string that represents the path to the current directory (where the application is running).
   * - OS_SEPARATOR
     - Prints the OS-specific separator: '/' for macOS and Linux, '\\' for Windows.
   * - USER_NAME
     - Creates a string that represents the username of the user currently logged in to the system.
   * - user
     - Creates a string that represents the path to the current user's home directory.
   * - desktop
     - Creates a string that represents the path to the current user's Desktop folder.
   * - documents
     - Creates a string that represents the path to the current user's Documents folder.
   * - downloads
     - Creates a string that represents the path to the current user's Downloads folder.
   * - music
     - Creates a string that represents the path to the current user's Music folder.
   * - pictures
     - Creates a string that represents the path to the current user's Pictures folder.
   * - public
     - Creates a string that represents the path to the current user's Public folder.
   * - videos
     - Creates a string that represents the path to the current user's Videos folder.
   * - linux_templates
     - Creates a string that represents the path to the current user's Templates folder in a Linux environment.
   * - mac_applications
     - Creates a string that represents the path to the current user's Applications folder in a macOS environment.
   * - windows_applicationData
     - Creates a string that represents the path to the current user's Roaming folder inside AppData in a Windows environment.
   * - windows_favorites
     - Creates a string that represents the path to the current user's Favorites folder in a Windows environment.
   * - windows_localappdata
     - Creates a string that represents the path to the current user's Local folder inside AppData in a Windows environment.
   * - windows_temp
     - Creates a string that represents the path to the current user's Temp folder inside LocalAppData in a Windows environment.

The paths for Windows environments are retrieved using the `winreg` module to query the Windows registry for accurate and current folder locations. This ensures that paths such as Desktop, Documents, Downloads, Music, Pictures, Public, and Videos are accurately defined for the user based on the system's registry settings.

**API Reference**
-----------------

.. automodule:: filesystem
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Reaching the Desktop Folder**
----------------------------------------

.. code-block:: python

   import filesystem as fs

   desk = fs.desktop
   print(desk)

**Output** (example paths):

- On Linux: ``/home/YOU/Desktop``
- On macOS: ``/Users/YOU/Desktop``
- On Windows: ``C:\\Users\\YOU\\Desktop``