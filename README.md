# FileSystem Pro

FileSystem Pro is designed to identify the operating system (OS) on which it’s running and define the paths to various user directories based on the OS.

## Getting Started

#### Dependencies

It's recommended Python 3.9 or later to use **FileSystem Pro**. You can download the latest version of Python in [python.org](https://www.python.org/).

#### Installation

Don't forget to upgrade pip:

```
pip3 install --upgrade pip
```

And install **FileSystem Pro:**

```
pip3 install filesystempro
```

You can also clone this repo to your local machine using:

```sh
git clone https://github.com/hbisneto/FileSystemPro.git
```

#

## Features
- **Cross-platform Compatibility:** The code is designed to work on multiple operating systems, including Linux, Mac, and Windows. This makes it versatile and adaptable to different environments.
- **Directory Path Identification:** The code identifies and defines the paths to several common user directories based on the operating system. This includes directories like Desktop, Documents, Downloads, Music, Pictures, Public, Videos, and others.
- **Current Working Directory:** The code uses `os.getcwd()` to get the current working directory.
- **String Formatting:** The code uses f-string formatting to create directory paths.
- **Monitoring System:** Wrapper acts as a monitoring system for the file system. It keeps track of all activities within the file system.
- **Change Tracking:** It records any changes made within the file system. This includes the creation of new files, modification of existing files, and deletion of files.
- **Real-Time Updates:** The Wrapper provides real-time updates on any changes made within the file system. This ensures that users have the most current information at all times.
- **Integrity Maintenance:** This feature is particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial. By tracking all changes, the Wrapper helps ensure that the file system remains accurate and reliable.

#

# Wrapper

Wrapper is a comprehensive toolkit that provides a set of utility functions specifically designed to facilitate file and directory operations. These operations may include creating, reading, updating, and deleting files or directories.

#### Watcher

Wrapper also serves as a monitoring system for the file system. It keeps track of any changes made within the file system, such as the creation of new files, modification of existing files, or deletion of files. This feature allows for real-time updates and can be particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial.

## Usage Example

These directories are dynamically generated based on the operating system platform (linux, darwin for Mac, and Windows)
#

<details>
<summary>FileSystem: Default Variables</summary>

```py
import filesystem as fs

# prints the current directory
print(fs.CURRENT_LOCATION)

# prints the User directory
print(fs.user)

# prints the Desktop directory
print(fs.desktop)

# prints the Documents directory
print(fs.documents)

# prints the Downloads directory
print(fs.downloads)

# prints the Music directory
print(fs.music)

# prints the Pictures directory
print(fs.pictures)

# prints the Public directory
print(fs.public)

# prints the Videos directory
print(fs.videos)

# prints Templates directory folder in Linux Environments
print(fs.linux_templates) # (specific to Linux)

# prints Applications directory folder in macOS Environments
print(fs.mac_applications) # (specific to Mac)

# prints Movies directory folder in macOS Environments
print(fs.mac_movies) # (specific to Mac)

# prints ApplicationData directory folder in Windows Environments
print(fs.windows_applicationData) # (specific to Windows)

# prints LocalAppData directory folder in Windows Environments
print(fs.windows_localappdata) # (specific to Windows)

# prints Temp directory folder in Windows Environments
print(fs.windows_temp) # (specific to Windows)

# prints Favorites directory folder in Windows Environments
print(fs.windows_favorites) # (specific to Windows)
```

</details>

#

<details>
<summary>FileSystem: Reaching Desktop Folder</summary>

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

#

<details>
<summary>Wrapper: Default Functions</summary>

1. `create_directory(path, create_subdirs=True)`: This function is used to create a directory at the specified `path`. If `create_subdirs` is `True`, the function creates all intermediate-level directories needed to contain the leaf directory. If `create_subdirs` is `False`, the function will raise an error if the directory already exists or if any intermediate-level directories in the path do not exist. Default is **`True`**
<br>If the directories already exist, it does nothing.

2. `create_file(file_name, path, text)`: This function opens a file with the name `file_name` in the directory specified by `path` and writes the content of `text` into the file.

3. `delete(path, recursive=False)`: This function is designed to delete a directory at a given `path`.
<br>If `recursive` is set to `True`, the function will delete the directory and all its contents. If it’s `False`, the function will only delete the directory if it’s empty. Default is **`False`**.

4. `enumerate_files(path)`: This function performs a depth-first traversal of the directory tree at the given path (after expanding any user home directory symbols). It returns a list of dictionaries containing the attributes of each file and directory in the tree.

5. `get_files(path)`: This function takes a path as input (which can include wildcards), expands any user home directory symbols (`~`), and returns a list of dictionaries containing the attributes of each file or directory that matches the path.

6. `get_path_properties(pathname)`: This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).

7. `list_directories(path)`: This function returns a list of all the directories in a given directory.

8. `list_files(path)`: This function returns a list of all the files in a given directory.

9. `make_zip(source, destination)`: This function is used to create a zip archive of a given source directory and move it to a specified destination.

</details>

#

<details>
<summary>Wrapper: Watcher</summary>

Wrapper Watcher is used to monitor changes in a file system.

- `__init__(self, root)`: This is the constructor method that initializes the `Watcher` object with a root directory to watch. It also saves the current state of the file system in `self.saved_state`.

- `get_state(self, path)`: This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the `core.enumerate_files(path)` function.

- `diff(self)`: This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.

- `__str__(self)`: This method returns a string representation of the `Watcher` object.
</details>

This class could be useful in scenarios where you need to monitor changes to a file system, for example, in a backup system or a live syncing service.

#

<details>
<summary>Wrapper: Creating a Folder</summary>

The following example shows how to create a new directory named `database` inside the `Documents` directory using **Wrapper**

```py
import filesystem as fs
from filesystem import wrapper as wr

bd_folder = "database"
try:
   wr.create_directory(f'{fs.documents}/{bd_folder}')
except:
   print("Could`t create the folder")
```
</details>

#

<details>
<summary>Wrapper: Get Files</summary>

#### Get files

The following example shows how to get files information from 'Downloads' folder.

```py
# Let's use 'Downloads' folder as example
# That's why I'll import filesystem
import filesystem as fs
# Let's use Wrapper to get info from files in 'Downloads' folder
from filesystem import wrapper as wr
```

```py
# Using the get_files syntax
pointers = wr.get_files(f'{fs.downloads}/*')

print(pointers)
```

Output:

```sh
[{'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'py'}, {'modified': 1697605101.6574, 'created': 1697683292.4821024, 'access': 1697683294.46923, 'name': 'Python_Logo.png', 'size': 747809, 'abspath': '/Users/YOU/Downloads/Python_Logo.png', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'png'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697682292.5433743, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'py'}]
```

#

#### Filter files by extension
The following example is using a list comprehension to filter out files with extension `.py` from the pointers list:

```py
py_files = [x for x in pointers if x["ext"] == "py"]
print(py_files)
```

```sh
[{'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'py'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697681829.0075543, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'py'}]
```

#

#### Get file names inside the filter
The following code is using a list comprehension that prints the names of all filtered files in the `py_files` list:

```py
print([x["name"] for x in py_files])
```

Output:

```sh
['CLI.py', 'Sample_File.py']
```
</details>

#

<details>
<summary>Wrapper: Enumerate files (walk recursively) from a directory</summary>

The following code is using a list comprehension to generate a list of all files in the `downloads` directory:

```py
tree = [x for x in wr.enumerate_files(fs.downloads)]
print(tree)
```

Output:

```sh
[{'modified': 1697683292.4821026, 'created': 1697683292.4821026, 'access': 1697683292.484029, 'name': 'Downloads', 'size': 224, 'abspath': '/Users/YOU/Downloads', 'dirname': '/Users/YOU', 'is_dir': True, 'is_file': False, 'is_link': False, 'exists': True, 'ext': ''}, {'modified': 1697683288.8639557, 'created': 1697683288.8639557, 'access': 1697602943.1846778, 'name': '.DS_Store', 'size': 6148, 'abspath': '/Users/YOU/Downloads/.DS_Store', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'DS_Store'}, {'modified': 1690685751.342114, 'created': 1690685751.4194765, 'access': 1690685751.342114, 'name': '.localized', 'size': 0, 'abspath': '/Users/YOU/Downloads/.localized', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'localized'}, {'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'py'}, {'modified': 1697605101.6574, 'created': 1697683292.4821024, 'access': 1697683294.46923, 'name': 'Python_Logo.png', 'size': 747809, 'abspath': '/Users/YOU/Downloads/Python_Logo.png', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'png'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697682292.5433743, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'ext': 'py'}]
```

#

Copyright © 2023 Bisneto Inc. All rights reserved.