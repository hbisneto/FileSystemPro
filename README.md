# FileSystem Pro 

FileSystem is a powerful toolkit designed to handle file and directory operations with ease and efficiency across various operating systems.

## Getting Started

This section will guide you through setting up the environment required to run **FileSystem Pro** effectively. Follow the steps below to ensure a smooth installation and configuration.

<details>
	<summary>Expand to get started</summary>
	
#### Requirements

It's recommended to use Python 3.8 or later to use **FileSystem Pro**. You can download the latest version of Python at [python.org](https://www.python.org/).

#### Installation

Don't forget to upgrade pip:

```sh
pip install --upgrade pip
```

And install **FileSystem Pro:**

```sh
pip install filesystempro
```

---

### For Developers / Contributors

Clone this repository to your local machine using:

```sh
git clone https://github.com/hbisneto/FileSystemPro.git
```

Install setuptools / Upgrade setuptools

```sh
pip install --upgrade setuptools
```

> Note: FileSystem Pro requires setuptools 69.5.1 or later.
><br> Python environment typically targets setuptools version 49.x.

Install wheel / Upgrade wheel

```sh
pip install --upgrade wheel
```
</details>

---

# FileSystem Module

FileSystem provides a comprehensive suite of methods for managing and interacting with various directories and user folders across multiple operating systems. It intelligently identifies the user's operating system—Linux, macOS, or Windows—and configures file paths for essential directories like Desktop, Documents, Downloads, Music, Pictures, Public, and Videos. Leveraging Python's built-in libraries such as `os`, `sys`, and `getpass`, it ensures cross-platform compatibility and accurate path retrieval. For Windows environments, it uses the `winreg` module to query the Windows registry, ensuring the paths to these directories are accurately retrieved based on the system's registry settings. This makes FileSystem a versatile and reliable tool for any file management needs.

## Features

FileSystemPro introduces a range of features and enhancements to help you manage and monitor your system's devices more efficiently.

<details>
	<summary>Expand to learn about the features</summary>
	
- **Cross-platform Compatibility:** The code is designed to work on multiple operating systems, including Linux, Mac, and Windows. This makes it versatile and adaptable to different environments.
- **Directory Path Identification:** The code identifies and defines the paths to several common user directories based on the operating system. This includes directories like Desktop, Documents, Downloads, Music, Pictures, Public, Videos, and others.
- **String Formatting:** The code uses f-string formatting to create directory paths.
- **Device Module:** Includes powerful tools for managing and retrieving detailed information about your system's disks and CPU, such as disk partitions, CPU usage, and more.
- **Compression Module:** Responsible for creating, extracting, and reading compressed archive files in tar and zip formats. It leverages Python's built-in tarfile and zipfile modules to handle these operations efficiently.
- **Monitoring System (Watcher):** Acts as a monitoring system for the file system. It keeps track of all activities within the file system and provides real-time updates on any changes.
- **Change Tracking:** Records any changes made within the file system. This includes the creation of new files, modification of existing files, and deletion of files.
- **Integrity Maintenance:** This feature is particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial. By tracking all changes, the Watcher helps ensure that the file system remains accurate and reliable.
- **Registry-Based Path Retrieval:** For Windows, the module now uses the `winreg` module to retrieve accurate paths from the Windows registry. It defines paths for the current user's home, Desktop, Documents, Downloads, Music, Pictures, Public, and Videos folders by querying the Windows registry keys.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>

```py
import filesystem as fs
```

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>
  
  <tr>
    <td>
    	CURRENT_LOCATION
    </td>
    <td>
	    Creates a string that represents the path to the current directory. (Where the application is running)
    </td>
  </tr>
  
  <tr>
    <td>
    	OS_SEPARATOR
    </td>
    <td>
	    Prints the OS separator
		  <br>'/' for macOS and Linux 
		  <br>'\\' for Windows
    </td>
  </tr>

  <tr>
    <td>
    	USER_NAME
    </td>
    <td>
	    Creates a string that represents the username of the user currently logged in to the system.
    </td>
  </tr>
  
  <tr>
    <td>
    	user
    </td>
    <td>
	    Creates a string that represents the path to the current user's home directory.
    </td>
  </tr>

  <tr>
    <td>
    	desktop
    </td>
    <td>
	    Creates a string that represents the path to the current user's Desktop folder.
    </td>
  </tr>
  
  <tr>
    <td>
    	documents
    </td>
    <td>
	    Creates a string that represents the path to the current user's Documents folder.
    </td>
  </tr>

  <tr>
    <td>
    	downloads
    </td>
    <td>
	    Creates a string that represents the path to the current user's Downloads folder.
    </td>
  </tr>
  
  <tr>
    <td>
    	music
    </td>
    <td>
	    Creates a string that represents the path to the current user's Music folder.
    </td>
  </tr>

  <tr>
    <td>
    	pictures
    </td>
    <td>
	    Creates a string that represents the path to the current user's Pictures folder.
    </td>
  </tr>
  
  <tr>
    <td>
    	public
    </td>
    <td>
	    Creates a string that represents the path to the current user's Public folder.
    </td>
  </tr>

  <tr>
    <td>
    	videos
    </td>
    <td>
	    Creates a string that represents the path to the current user's Videos folder.
    </td>
  </tr>
  
  <tr>
    <td>
    	linux_templates
    </td>
    <td>
	    Creates a string that represents the path to the current user's Templates folder in Linux environment.
    </td>
  </tr>

  <tr>
    <td>
    	mac_applications
    </td>
    <td>
	    Creates a string that represents the path to the current user's Applications folder in macOS environment.
    </td>
  </tr>
  
  <tr>
    <td>
    	windows_applicationData
    </td>
    <td>
	    Creates a string that represents the path to the current user's Roaming folder inside AppData in Windows environment.
    </td>
  </tr>

  <tr>
    <td>
    	windows_favorites
    </td>
    <td>
	    Creates a string that represents the path to the current user's Favorites folder in Windows environment.
    </td>
  </tr>
  
  <tr>
    <td>
    	windows_localappdata
    </td>
    <td>
	    Creates a string that represents the path to the current user's Local folder inside AppData in Windows environment.
    </td>
  </tr>

  <tr>
    <td>
    	windows_temp
    </td>
    <td>
	    Creates a string that represents the path to the current user's Temp folder inside LocalAppData in Windows environment.
    </td>
  </tr>

</table>

The paths for Windows environment are retrieved using the `winreg` module to query the Windows registry for accurate and current folder locations. This ensures that paths such as Desktop, Documents, Downloads, Music, Pictures, Public, and Videos are accurately defined for the user based on the system's registry settings.

</details>

---

<details>
	<summary>Expand for sample codes</summary>

<details>
	<summary>FileSystem: Reaching the desktop folder</summary>
	
The following example shows how to get the `Desktop` directory path

```py
import filesystem as fs

desk = fs.desktop

print(desk)
```

Output:

```sh
## On Linux
/home/YOU/Desktop

## On macOS
/Users/YOU/Desktop

## On Windows
C:\Users\YOU\Desktop
```

</details>
</details>

---

# Compression Module

The Compression module is responsible for creating, extracting, and reading compressed archive files in tar and zip formats. It leverages Python's built-in tarfile and zipfile modules to handle these operations efficiently.

## Features

The Compression Module offers robust and versatile tools for managing file compression and extraction, whether you prefer the tar or zip format.

<details>
	<summary>Expand to learn about TarFile</summary>

### TarFile

The Tarfile module offers robust and versatile tools for managing file compression and extraction, making it an essential tool for efficient file management.
	
</details>

---

<details>
	<summary>Expand to learn about the ZipFile</summary>

### ZipFile

The Zipfile module offers robust and versatile tools for managing file compression and extraction, making it an essential tool for efficient file management.

</details>

---

<details>
	<summary>Expand to learn about the features</summary>


- **Create Tar Archive:** This feature allows you to compress a single file, directory, or a list of files and directories into a tar archive. It efficiently bundles multiple files and directories into a single archive file, making it easier to manage and transport.

- **Extract Tar Archive:** This feature enables you to extract files from a tar archive to a specified destination. You can choose to extract all files or only a specified list of files, providing flexibility in handling the contents of the archive.

- **Read Tar Archive:** This feature allows you to read and list the contents of a tar archive without extracting them. It provides a convenient way to view the files and directories within the archive before deciding which ones to extract.

- **Create Zip Archive:** This feature allows you to compress a single file, directory, or a list of files and directories into a zip archive. Similar to the tar archive creation, it bundles multiple files and directories into a single archive file, but in a different format.

- **Extract Zip Archive:** This feature enables you to extract files from a zip archive to a specified destination. You can choose to extract all files or only a specified list of files, giving you control over which files to retrieve from the archive.

- **Read Zip Archive:** This feature allows you to read and list the contents of a zip archive without extracting them. It provides a convenient way to inspect the files and directories within the archive before extraction, ensuring you have the information you need.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
The Compression module in FileSystemPro provides a comprehensive set of functions to efficiently manage file compression and extraction, enhancing productivity and versatility in handling various file formats and archives

```py
from filesystem import compression
```

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>

  <tr>
    <td>
      compression.tarfile.create_tar(fullpath_files, destination)
    </td>
    <td>
      The function compresses files or directories into a TAR file.
	    Returns a message indicating whether a single file/directory or a list of files/directories was compressed.
    </td>
  </tr>
  <tr>
    <td>
      compression.tarfile.extract(tar_filename, destination, extraction_list=[])
    </td>
    <td>
      Extract files from a tar archive. It can extract all files or a specified list of files from the archive.
	    Returns <strong>True</strong> if the extraction is successful, <strong>[FileSystem Pro]: File Not Found</strong> if the tar file is not found, <strong>False</strong> if a specified item in <strong>extraction_list</strong> is not found and <strong>Error Message</strong> if any other error occurs during extraction.
    </td>
  </tr>
  <tr>
    <td>
      compression.tarfile.read_tar_archive(tar_filename)
    </td>
    <td>
      Reads the contents of a TAR archive file and returns a list of the names of the files contained within it.
    </td>
  </tr>
  <tr>
    <td>
      compression.zipfile.create_zip(fullpath_files, destination)
    </td>
    <td>
      The function compresses files or directories into a ZIP file.
	    Returns a message indicating whether a single file/directory or a list of files/directories was compressed.
    </td>
  </tr>
  <tr>
    <td>
      compression.zipfile.extract(zip_path, destination, extraction_list=None)
    </td>
    <td>
      Reads the contents of a ZIP file and extracts files based on the provided parameters.
    </td>
  </tr>
  <tr>
    <td>
      compression.zipfile.read_zip_archive(zip_filename, show_compression_system_files=True)
    </td>
    <td>
      Reads the contents of a ZIP file and returns a list of the names of the files contained within it.
    </td>
  </tr>

</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>

### ZipFile Sample Codes
	
<details>
<summary>Compression: Creating a zip archive</summary>

This code demonstrates how to use the `create_zip` function to create a ZIP archive using **Compression**

```py
from filesystem import compression
compression.zipfile.create_zip('/path/to/file_or_directory', '/path/to/destination.zip')
```

</details>

---

<details>
<summary>Compression: Extracting from a zip archive</summary>

This code demonstrates how to use the `extract` function to extract files from a ZIP archive using **Compression**.

```py
from filesystem import compression
compression.zipfile.extract('/path/to/archive.zip', '/path/to/destination')
```

</details>

---

<details>
<summary>Compression: Reading a zip archive</summary>

This code demonstrates how to use the read_zip_archive function to read the contents of a ZIP archive using **Compression**.

```py
from filesystem import compression
contents = compression.zipfile.read_zip_archive('/path/to/archive.zip')
print(contents)
```

</details>

---
### TarFile Sample Codes
	
<details>
<summary>Compression: Creating a tar archive</summary>

This code demonstrates how to use the create_tar function to create a TAR archive using **Compression**.

```py
from filesystem import compression
compression.tar.create_tar('/path/to/file_or_directory', '/path/to/destination.tar')
```

</details>

---

<details>
<summary>Compression: Extracting from a tar archive</summary>

This code demonstrates how to use the extract function to extract files from a TAR archive using **Compression**.

```py
from filesystem import compression
compression.tar.extract('/path/to/archive.tar', '/path/to/destination')

```

</details>

---

<details>
<summary>Compression: Reading a tar archive</summary>

This code demonstrates how to use the read_tar_archive function to read the contents of a TAR archive using **Compression**.

```py
from filesystem import compression
contents = compression.tar.read_tar_archive('/path/to/archive.tar')
print(contents)
```

</details>
</details>

---

# Console Module

Console is a robust library designed to enable ANSI escape character sequences, which are used for generating colored terminal text and cursor positioning. This library is a key addition to FileSystemPro as a third-party library, enhancing the toolkit for developers who require consistent terminal styling across different operating systems.


## Features

Unlock the full potential of your Terminal with Console, a robust and feature-rich module that revolutionizes text styling and formatting.

<details>
	<summary>Expand to learn about the features</summary>
	
- **Universal Compatibility:** Console ensures that applications or libraries utilizing ANSI sequences for colored output on Unix or Macs can now operate identically on Windows systems.
- **Simplified Integration:** With no dependencies other than the standard library, integrating Console into your projects is straightforward. It’s tested across multiple Python versions, ensuring reliability.
- **Enhanced Terminal Experience:** By converting ANSI sequences into appropriate win32 calls, Console allows Windows terminals to emulate the behavior of Unix terminals, providing a consistent user experience.
- **Effortless Transition:** For developers transitioning to FileSystemPro, incorporating Console into your workflow is effortless, enabling you to maintain the visual aspects of your terminal applications without platform constraints.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
These constants are used to control the appearance of text output in the terminal, including foreground and background colors, as well as text styles. By utilizing these constants, developers can enhance the readability and visual appeal of their terminal applications, ensuring a consistent experience across different operating systems.

```py
from filesystem import console as fsconsole
```

<table>
  <tr>
    <th>Constants</th>
    <th>Colors</th>
  </tr>
  
  <tr>
    <td>foreground</td>
    <td>
      BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    </td>
  </tr>
  
  <tr>
    <td>background</td>
    <td>
      BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    </td>
  </tr>
  
  <tr>
    <td>style</td>
    <td>
      DIM, NORMAL, BRIGHT, RESET_ALL
  </td>
  </tr>
  
</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>
	
> Please note that **GitHub (and PYPI) does not support colored text** in README files. This is due to the limitations of the markdown language used in GitHub (and PYPI) READMEs, which does not have built-in support for text color changes.

<details>
<summary>Console: Printing a red foreground text message</summary>

The following example shows how to print some red foreground texts using **Console**

```py
from filesystem import console as fsconsole

# This will print a spaced text to your print message
print(fsconsole.foreground.RED, "This is a warn message")

# This will print a no space text to your print message
print(fsconsole.foreground.RED + "This is another warn message")

# You can use f-string format to assign the color to your print
print(f'{fsconsole.foreground.RED}This is a new warn message{fsconsole.foreground.RESET}')

# This text will be printed without color (default)
print("This is a normal text")
```

Output:

<pre><code><span style="color: red;"> This is a warn message
This is another warn message
This is a new warn message</span>
<span">This is a normal text</span></code></pre>

</details>

---

<details>
<summary>Console: Printing a blue background text message</summary>

The following example shows how to print some blue background texts using **Console**

```py
from filesystem import console as fsconsole

# This will print a spaced text to your print message
print(fsconsole.background.BLUE, 'This is a blue background message')

# This will print a no space text to your print message
print(fsconsole.background.BLUE + 'This is another blue background message')

# You can use f-string format to assign the color to your print
print(f'{fsconsole.background.BLUE}This is a new blue background message{fsconsole.background.RESET}')

# This text will be printed without color (default)
print('This is a normal text')
```

Output:

<pre><code><span style="background-color: #ADD8E6;"> This is a blue background message
This is another blue background warn message
This is a new blue background message</span>
<span">This is a normal text</span></code></pre>

</details>

---

<details>
<summary>Console: Different foregrounds, backgrounds and styles</summary>

The following example shows how to print some texts with different backgrounds, foregrounds and styles using **Console**

```py
# Prints a red foreground text
print(f'{fsconsole.foreground.RED}Some red text')
# Prints a red foreground text with a green background
print(f'{fsconsole.background.GREEN}And with a green background{fsconsole.style.RESET_ALL}')
# Prints a dim normal text with no background
print(f'{fsconsole.style.DIM}And in dim text{fsconsole.style.RESET_ALL}')
# Prints a normal text
print('Back to normal color')
```

Output:

<pre><code><span style="color: red;">Some red text</span>
<span style="background-color: #90EE90; color: red">And with a green background</span>
<span style="color: #A9A9A9">And in dim text</span>
<span>Back to normal color</span>
</code></pre>

</details>

---

Remember, for the color changes to work, your Terminal must support ANSI escape sequences, which are used to set the color. Not all Terminals do, so if you’re not seeing the colors as expected, that could be why. 
</details>
</details>

---

# Device Module

The Device module includes powerful tools for managing and retrieving detailed information about your system's disks and CPU.

## Features

The Device module includes powerful tools for managing and retrieving detailed information about your system's disks and CPU, enhancing productivity and ensuring efficient system management in applications.

<details>
	<summary>Expand to learn about Disks</summary>

### Disks

The Disks section of the Device module provides powerful tools for managing and retrieving detailed information about disk partitions, boot drive names, filesystem types, and storage metrics. It enhances productivity by simplifying disk management and ensuring efficient retrieval of disk-related information.	
</details>

---

<details>
	<summary>Expand to learn about the CPU</summary>

### CPU

The CPU section of the Device module offers essential metrics and functionalities for monitoring CPU performance, including CPU usage percentage, CPU times, and the number of CPU cores. It empowers developers to efficiently manage and optimize CPU usage within their applications.

</details>

---

<details>
	<summary>Expand to learn about the features</summary>


- **Boot Time:** Provides the system's boot time.
- **Current Disk Filesystem Name:** Returns the name of the current disk filesystem.
- **Disk Info:** Displays detailed information about the disks.
- **Disk I/O Counters:** Returns disk I/O counters.
- **Disk Partitions:** Retrieves disk partitions.
- **Boot Drive Name:** Returns the name of the boot drive.
- **Filter by Device:** Filters disk partitions based on the device.
- **Filter by Filesystem Type:** Filters disk partitions based on filesystem type.
- **Filter by Mount Point:** Filters disk partitions based on the mount point.
- **Filter by Options:** Filters disk partitions based on options.
- **Storage Metrics:** Provides storage metrics for a specific mount point.
- **CPU Usage Percentage:** Returns the CPU usage percentage.
- **CPU Usage Times:** Provides CPU usage times.
- **CPU Count:** Returns the number of CPUs (logical cores) available in the system.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
The Directory module in FileSystemPro brings a comprehensive set of methods that streamline and enhance directory management

```py
from filesystem import device
```

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>

  <tr>
    <td>
      directory.combine(*args, paths=[])
    </td>
    <td>
      Combines a list of paths or arguments into a single path. If the first argument or the first element in the paths list is not an absolute path, it raises a ValueError.
    </td>
  </tr>

</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>
	
<details>
<summary>Directory: Check if exists</summary>

The following example check whether a directory exists within the file system and print the result using **Directory**

```py
import filesystem as fs
from filesystem import directory as dir

documents_exists = dir.exists(fs.documents)

print(documents_exists)
```

Output:

```
True
```
</details>

<details>
<summary>Directory: Listing directories inside a folder</summary>

The following example shows how to lists all directories in the specified path using **Directory**

```py
import filesystem as fs
from filesystem import directory as dir

folder_list = dir.get_directories(fs.documents)

print(folder_list)
```

Output:

```
['Work', 'School', 'PicsBackups', 'Office Documents']
```
</details>

<details>
<summary>Directory: Renaming a folder</summary>

The following example shows how rename a folder using **Directory**

```py
import filesystem as fs
from filesystem import directory as dir

new_name = dir.rename(f'{fs.documents}/MyFolder', f'{fs.documents}/NewFolder')

print(new_name)
```

Output:

```
True
```
</details>

---

</details>

---

# Directory Module

The Directory module is a component of the FileSystemPro library that provides a collection of functions
for handling directory-related operations. It simplifies tasks such as path manipulation, 
directory creation and deletion, and file retrieval within directories.

## Features

The Directory module simplifies directory-related tasks like path manipulation, directory creation and deletion, and file retrieval. It enhances productivity and ensures efficient directory management in applications.

<details>
	<summary>Expand to learn about the features</summary>
	
- **Path Combination:** Dynamically combines multiple paths into a single path string.
- **Directory Creation:** Creates new directories, with an option to create necessary subdirectories.
- **Directory Deletion:** Deletes directories, with an option for recursive deletion.
- **Directory Existence Check:** Checks whether a directory exists at a specified path.
- **File Retrieval:** Retrieves a list of files within a directory using glob patterns.
- **Parent Directory Information:** Retrieves the name or path of a file's parent directory.
- **Directory Listing:** Lists all subdirectories within a given directory.
- **Directory Renaming:** Renames a directory if it exists.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
The Directory module in FileSystemPro brings a comprehensive set of methods that streamline and enhance directory management

```py
from filesystem import directory as dir
```

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>

  <tr>
    <td>
      directory.combine(*args, paths=[])
    </td>
    <td>
      Combines a list of paths or arguments into a single path. If the first argument or the first element in the paths list is not an absolute path, it raises a ValueError.
    </td>
  </tr>

  <tr>
    <td>
      directory.create(path, create_subdirs = True)
    </td>
    <td>
      Creates a directory at the specified path. If `create_subdirs` is True, all intermediate-level 
      directories needed to contain the leaf directory will be created. After the directory is created, 
      it returns the details of the created directory.
    </td>
  </tr>

  <tr>
    <td>
      directory.delete(path, recursive=False)
    </td>
    <td>
      Deletes a directory at the specified path. If `recursive` is True, the directory and all its contents will be removed.
    </td>
  </tr>

  <tr>
    <td>
      directory.exists(path)
    </td>
    <td>
      Checks if a directory exists at the specified path.
    </td>
  </tr>

  <tr>
    <td>
      directory.get_directories(path, fullpath=True)
    </td>
    <td>
      Create a list of directories within a specified path and returns either their full paths or just their names based on the <strong>fullpath</strong> parameter. Defaults to <strong>True</strong>.
    </td>
  </tr>

  <tr>
    <td>
      directory.get_name(path)
    </td>
    <td>
      Retrieves the name of the directory of the specified path. 
      If the path has an extension, it is assumed to be a file, and the parent directory name is returned. 
      If the path does not have an extension, it is assumed to be a directory, 
      and the directory name is returned.
    </td>
  </tr>
  
  <tr>
    <td>
      directory.get_parent(path)
    </td>
    <td>
      Retrieves the parent directory from the specified path.
    </td>
  </tr>

  <tr>
    <td>
      directory.get_parent_name(path)
    </td>
    <td>
      Retrieves the parent directory name from the specified path.
    </td>
  </tr>
  
    <tr>
    <td>
      directory.get_size(directory_path)
    </td>
    <td>
      Calculates the total size of all files in the specified directory. The size is returned in bytes, KB, MB, GB, or TB, depending on the total size.
    </td>
  </tr>
  
  <tr>
    <td>
      directory.join(path1='', path2='', path3='', path4='', paths=[])
    </td>
    <td>
      Joins multiple directory paths into a single path. The function ensures that each directory path ends with a separator before joining. If a directory path does not end with a separator, one is added.
    </td>
  </tr>
  
  <tr>
    <td>
      directory.move(source, destination, move_root=True)
    </td>
    <td>
      The move function is designed to move files or directories from a source location to a destination.
      It provides flexibility by allowing you to specify whether intermediate-level subdirectories should be created during the move operation.
    </td>
  </tr>


  <tr>
    <td>
      directory.rename(old_path, new_path)
    </td>
    <td>
      Renames a directory from the old directory path to the new directory path. If the old directory path does not exist or is not a directory, the function returns False.
    </td>
  </tr>
</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>
	
<details>
<summary>Directory: Check if exists</summary>

The following example check whether a directory exists within the file system and print the result using **Directory**

```py
import filesystem as fs
from filesystem import directory as dir

documents_exists = dir.exists(fs.documents)

print(documents_exists)
```

Output:

```
True
```
</details>

<details>
<summary>Directory: Listing directories inside a folder</summary>

The following example shows how to lists all directories in the specified path using **Directory**

```py
import filesystem as fs
from filesystem import directory as dir

folder_list = dir.get_directories(fs.documents)

print(folder_list)
```

Output:

```
['Work', 'School', 'PicsBackups', 'Office Documents']
```
</details>

<details>
<summary>Directory: Renaming a folder</summary>

The following example shows how rename a folder using **Directory**

```py
import filesystem as fs
from filesystem import directory as dir

new_name = dir.rename(f'{fs.documents}/MyFolder', f'{fs.documents}/NewFolder')

print(new_name)
```

Output:

```
True
```
</details>

---

</details>

---

# File Module

The File module is a comprehensive utility toolset that forms part of the FileSystemPro library. 
It provides a suite of functions designed to handle various file operations such as integrity checks,
file creation, deletion, enumeration, and file splitting and reassembling.


## Features

The File module is packed with a variety of features aimed at simplifying and optimizing file management tasks. From calculating file integrity to creating, deleting, and managing files, these features are designed to provide robust solutions for handling all your file-related operations.

<details>
	<summary>Expand to learn about the features</summary>
	
- **Checksum Calculation:** Utilizes SHA-256 hashing to calculate file checksums for integrity verification.
- **Integrity Check:** Compares checksums of two files to verify their integrity.
- **File Creation:** Supports creating both text and binary files with specified data.
- **File Deletion:** Safely deletes files by checking for their existence before removal.
- **File Enumeration:** Enumerates all files in a given directory, providing detailed file information.
- **File Existence Check:** Determines if a file exists at a given path.
- **File Listing:** Lists all files in a specified directory.
- **File Renaming:** Renames files within a directory after checking for their existence.
- **File Reassembling:** Reassembles split files back into a single file.
- **File Splitting:** Splits a file into smaller parts based on a specified chunk size.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
The Directory module in FileSystemPro brings a comprehensive set of methods that streamline and enhance directory management

```py
from filesystem import file as fsfile
```

<table>
  <tr>
  	<th>Method</th>
  	<th>Description</th>
  </tr>
  
  <tr>
    <td>file.append_text(file, text)</td>
    <td>
      Appends UTF-8 encoded text to an existing file, or creates a new file if it does not exist.
    </td>
  </tr>
  
  <tr>
    <td>file.calculate_checksum(file)</td>
    <td>
      Calculates the SHA-256 checksum of a file. This function reads the file in binary mode and updates the hash in chunks to efficiently handle large files.
    </td>
  </tr>

  <tr>
    <td>file.check_integrity(file, reference_file)</td>
    <td>
      Compares the SHA-256 checksums of two files to verify their integrity. This function is useful for ensuring that a file has not been altered or corrupted by comparing it to a reference file.
    </td>
  </tr>
  
  <tr>
    <td>file.copy(source, destination, overwrite=False)</td>
    <td>
      Copies a file or a list of files from the source to the destination. This function handles both single file copying and multiple file copying while providing options for overwriting existing files and performing various validation checks.
    </td>
  </tr>

  <tr>
    <td>file.create(file, data, overwrite=False, encoding="utf-8")</td>
    <td>
      Creates a file at the specified path and writes data into it. If the file already exists, its contents can be either appended to or overwritten based on the <strong>overwrite</strong> parameter. The function then returns the details of the created file
    </td>
  </tr>
  
  <tr>
    <td>file.create_binary_file(filename, data)</td>
    <td>
      Creates a binary file at the specified filename and writes data into it. If the data is not of bytes type,
    it is first encoded to bytes.
    </td>
  </tr>

  <tr>
    <td>file.delete(file)</td>
    <td>
      Deletes a file at the specified path if it exists.
    </td>
  </tr>
  
  <tr>
    <td>file.enumerate_files(file)</td>
    <td>
      Enumerates all files in a given directory and its subdirectories. 
      For each file and directory, it retrieves various attributes using the `wra.get_object` function.
    </td>
  </tr>
  
  <tr>
    <td>file.exists(file)</td>
    <td>
      Checks if a file exists at the specified path.
    </td>
  </tr>
  
  <tr>
    <td>file.find_duplicates(path)</td>
    <td>
      Finds duplicate files in a given directory and its subdirectories.
      A file is considered a duplicate if it has the same checksum as another file.
    </td>
  </tr>
  
  <tr>
    <td>file.get_extension(file_path, lower=True)</td>
    <td>
      Extracts the file extension from the given file path and returns it in lowercase or uppercase based on the `lower` parameter.
    </td>
  </tr>
  
  <tr>
    <td>file.get_filename(filepath)</td>
    <td>
      Extracts the filename from the given filepath and returns it.
    </td>
  </tr>

  <tr>
    <td>file.get_files(path, fullpath=True, extension=None)</td>
    <td>
      Retrieves a list of files from the specified directory. Optionally, it can return the full path of each file and filter files by their extension.
    </td>
  </tr>
  
  <tr>
    <td>file.get_size(file_path)</td>
    <td>
      Calculates the size of a file at the specified path.
      The size is returned in bytes, KB, MB, GB, or TB, depending on the size.
    </td>
  </tr>
  
  <tr>
    <td>file.move(source, destination, new_filename=None, replace_existing=False)</td>
    <td>
      The move function moves a file from a source location to a destination location. 
      If the destination file already exists,
      you can choose whether to replace it or keep the existing file. 
    </td>
  </tr>
  
  <tr>
    <td>file.rename(old_name, new_name)</td>
    <td>
      Renames a file in a given directory from `old_name` to `new_name`.
    </td>
  </tr>

  <tr>
    <td>file.reassemble_file(large_file, new_file)</td>
    <td>
      Reassembles a file that was previously split into parts. 
      The function checks for the existence of the split parts and reads each part, writing it to a new file. 
      After all parts have been written to the new file, the function deletes the parts.
    </td>
  </tr>
  
  <tr>
    <td>file.split_file(file, chunk_size = 1048576)</td>
    <td>
      Splits a large file into smaller chunks. The function reads the file in chunks of a specified size and writes each chunk to a new file. The new files are named by appending `.fsp` and an index number to the original filename.
    </td>
  </tr>  
</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>
	
<details>
<summary>File: Check Integrity</summary>

The following example check the integrity of a file against a reference file and print the result using **File**

```py
from filesystem import file as fsfile

integrity = fsfile.check_integrity("/path/to/file", "/path/to/reference_file")
print("Files are identical:", integrity)
```

Output:

```
Files are identical: True
```
</details>

<details>
<summary>File: Split File</summary>

The following example shows how to split a large file into 500 KB chunks using **File**

```py
from filesystem import file as fsfile

is_split = fsfile.split_file("large_file.iso", 512000)
print(is_split)
```

Output:

```
True
```
</details>

<details>
<summary>File: Reassemble File</summary>

The following example shows how to reassemble a file that was previously split into parts using **File**

```py
from filesystem import file as fsfile

fsfile.reassemble_file("large_file.iso", "new_file.iso")
```

Output:

```
None output
```
</details>

---

</details>

---

# Wrapper Module

Wrapper is a comprehensive toolkit that provides a set of utility functions specifically designed to facilitate file and directory operations. These operations may include creating, reading, updating, and deleting files or directories.


## Features

Wrapper is an integral part of the FileSystemPro library, designed to provide detailed information about 
files and directories. 
It includes functions for retrieving metadata and checking file extensions.

<details>
	<summary>Expand to learn about the features</summary>
	
- **Metadata Retrieval:** Gathers comprehensive metadata about a file or directory path.
- **Extension Check:** Determines whether a file has an extension.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
The Wrapper module in FileSystemPro brings a comprehensive set of methods that streamline and enhance file and directory management.

```py
from filesystem import wrapper as wra
```

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>
      wrapper.get_object(path)
    </td>
    <td>
      This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).
    </td>
  </tr>
  
  <tr>
    <td>
      wrapper.has_extension(file_path)
    </td>
    <td>
      Checks if the given file path has an extension. This function can return True or False based on the string, even if the file or directory does not exist.
    </td>
  </tr>
  
  
  
</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>
	
<details>
<summary>Wrapper: Has Extension</summary>

Checks if the given file path has an extension

```python
from filesystem import wrapper as wra

bool_extension = wra.has_extension("/path/to/file.txt")
print(bool_extension)
```

Output

```sh
True
```

This will return **True** because the file has an extension (.txt).

---

Checks if the given file path has an extension

```python
from filesystem import wrapper as wra

bool_extension = wra.has_extension("/path/to/file")
print(bool_extension)
```

Output

```sh
False
```

This will return **False** because the file does not have an extension.
</details>

---

</details>

---

# Watcher Module

Watcher serves as a monitoring system for the file system. It keeps track of any changes made within the file system, such as the creation of new files, modification of existing files, or deletion of files. This feature allows for real-time updates and can be particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial.


## Features

Watcher could be useful in scenarios where you need to monitor changes to a file system, for example, in a backup system or a live syncing service.

<details>
	<summary>Expand to learn about the features</summary>
	
- **Initialization:** The constructor method init(self, root) initializes the Watcher object with a root directory to watch and saves the current state of the file system.

- **State Retrieval:** The get_state(self, path) method returns a dictionary of all files in the given path with their metadata.

- **Change Detection:** The diff(self) method compares the current state of the file system with the saved state to identify any changes (created, updated, or removed files) and returns a list of dictionaries with the metadata of changed files and the type of change.

- **String Representation:** The str(self) method returns a string representation of the Watcher object.

</details>

---

<details>
	<summary>Expand to learn about the methods</summary>
	
The Wrapper module in FileSystemPro brings a comprehensive set of methods that streamline and enhance file and directory management.

```py
from filesystem import watcher as wat
```

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>

  <tr>
    <td>init(self, root)</td>
    <td>
      This is the constructor method that initializes the Watcher object with a root directory to watch. It also saves the current state of the file system in <strong>self.saved_state</strong>.
    </td>
  </tr>

  <tr>
    <td>get_state(self, path):</td>
    <td>
      This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the <strong>wrapper.enumerate_files(path)</strong> function.
    </td>
  </tr>

  <tr>
    <td>diff(self)</td>
    <td>
      This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.
    </td>
  </tr>

  <tr>
    <td>str(self)</td>
    <td>
      This method returns a string representation of the <strong>Watcher</strong> object.
    </td>
  </tr>
  
</table>
</details>

---

<details>
	<summary>Expand for sample codes</summary>
	
<details>
<summary>Watcher: Monitoring Documents Folder</summary>

This Watcher example is designed to monitor changes in **Documents** directory and print out the changes as they occur.

```py
# Native library
import time
from datetime import datetime

# FileSystemPro
import filesystem as fs
from filesystem import watcher as wat

# Create a new instance of Watcher class
watcher = wat.Watcher(f'{fs.documents}')

# Run `diff` method to get directory changes
while True:
    changes = watcher.diff()
    if changes:
        print(f"Changes detected at: {datetime.now()}:")
        for change in changes:
            print(f"{change['abspath']} was {change['change']}")
    time.sleep(5)  # Awaits for 5 seconds before a new verification
```

</details>

---

</details>

---

Copyright © 2023–2025 Bisneto Inc. All rights reserved.