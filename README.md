# FileSystem Pro 

FileSystem Pro is designed to identify the operating system (OS) on which it’s running and define the paths to various user directories based on the OS.

## Getting Started

#### Recommendation

It's recommended Python 3.8 or later to use **FileSystem Pro**. You can download the latest version of Python in [python.org](https://www.python.org/).

#### Installation

Don't forget to upgrade pip:

```sh
pip install --upgrade pip
```

And install **FileSystem Pro:**

```sh
pip install filesystempro
```

You can also clone this repo to your local machine using:

```sh
git clone https://github.com/hbisneto/FileSystemPro.git
```

---

## Features
- **Cross-platform Compatibility:** The code is designed to work on multiple operating systems, including Linux, Mac, and Windows. This makes it versatile and adaptable to different environments.
- **Directory Path Identification:** The code identifies and defines the paths to several common user directories based on the operating system. This includes directories like Desktop, Documents, Downloads, Music, Pictures, Public, Videos, and others.
- **Current Working Directory:** The code uses `os.getcwd()` to get the current working directory.
- **String Formatting:** The code uses f-string formatting to create directory paths.
- **Monitoring System:** Wrapper acts as a monitoring system for the file system. It keeps track of all activities within the file system.
- **Change Tracking:** It records any changes made within the file system. This includes the creation of new files, modification of existing files, and deletion of files.
- **Real-Time Updates:** The Wrapper provides real-time updates on any changes made within the file system. This ensures that users have the most current information at all times.
- **Integrity Maintenance:** This feature is particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial. By tracking all changes, the Wrapper helps ensure that the file system remains accurate and reliable.

---

## FileSystem

```py
import filesystem as fs
```

<details>
<summary>fs.CURRENT_LOCATION</summary>

> Creates a string that represents the path to the current directory. (Where the application is running)

```py
print(fs.CURRENT_LOCATION)
```

</details>

<details>
<summary>fs.OS_SEPARATOR</summary>

> prints the OS separator 
<br>'`/`' for macOS and Linux
<br>'`\\`' for Windows

```py
print(fs.OS_SEPARATOR)
```

</details>

<details>
<summary>fs.USER_NAME</summary>

> Creates a string that represents the username of the user currently logged in to the system.

```py
print(fs.USER_NAME)
```

</details>

<details>
<summary>fs.user</summary>

> Creates a string that represents the path to the current user's home directory.

```py
print(fs.user)
```

</details>

<details>
<summary>fs.desktop</summary>

> Creates a string that represents the path to the current user's Desktop folder.

```py
print(fs.desktop)
```

</details>

<details>
<summary>fs.documents</summary>

> Creates a string that represents the path to the current user's Documents folder.

```py
print(fs.documents)
```

</details>

<details>
<summary>fs.downloads</summary>

> Creates a string that represents the path to the current user's Downloads folder.

```py
print(fs.downloads)
```

</details>

<details>
<summary>fs.music</summary>

> Creates a string that represents the path to the current user's Music folder.

```py
print(fs.music)
```

</details>

<details>
<summary>fs.pictures</summary>

> Creates a string that represents the path to the current user's Pictures folder.

```py
print(fs.pictures)
```

</details>

<details>
<summary>fs.public</summary>

> Creates a string that represents the path to the current user's Public folder.

```py
print(fs.public)
```

</details>

<details>
<summary>fs.videos</summary>

> Creates a string that represents the path to the current user's Videos folder.

```py
print(fs.videos)
```

</details>

<details>
<summary>fs.linux_templates</summary>

> Creates a string that represents the path to the current user's Templates folder in Linux environment.

```py
print(fs.linux_templates)
```

</details>

<details>
<summary>fs.mac_applications</summary>

> Creates a string that represents the path to the current user's Applications folder in macOS environment.

```py
print(fs.mac_applications)
```

</details>

<details>
<summary>fs.windows_applicationData</summary>

> Creates a string that represents the path to the current user's Roaming folder inside AppData in Windows environment.

```py
print(fs.windows_applicationData)
```

</details>

<details>
<summary>fs.windows_favorites</summary>

> Creates a string that represents the path to the current user's Favorites folder in Windows environment.

```py
print(fs.windows_favorites)
```

</details>

<details>
<summary>fs.windows_localappdata</summary>

> Creates a string that represents the path to the current user's Local folder inside AppData in Windows environment.

```py
print(fs.windows_localappdata)
```

</details>

<details>
<summary>fs.windows_temp</summary>

> Creates a string that represents the path to the current user's Temp folder inside LocalAppData in Windows environment.

```py
print(fs.windows_temp)
```

</details>

## Sample Codes

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

---

# Wrapper

```py
from filesystem import wrapper as wra
```

Wrapper is a comprehensive toolkit that provides a set of utility functions specifically designed to facilitate file and directory operations. These operations may include creating, reading, updating, and deleting files or directories.

<details>
<summary>combine(*args, paths=[]):</summary>

```py
wra.combine(*args, paths=[]):
```

This function is designed to combine file or directory paths. It takes any number of arguments `*args` and an optional parameter paths which is a list of paths. The function returns a combined path based on the inputs.
<br>If the paths list is provided, the function uses it to combine paths. It starts with the first path in the list and checks if it’s an absolute path. If it’s not, it raises a `ValueError` with a detailed error message. Then, it iterates over the rest of the paths in the list. If a path is absolute, it replaces the current result with this path. If a path is relative, it joins this path to the current result. Finally, it returns the combined path.
<br> If the paths list is not provided or is empty, the function uses the arguments passed `*args`. It starts with the first argument and checks if it’s an absolute path. If it’s not, it raises a `ValueError` with a detailed error message. Then, it iterates over the rest of the arguments. If an argument is an absolute path, it replaces the current result with this path. If an argument is a relative path and not an empty string, it adds this path to the current result. If the current result doesn’t end with a separator (os.sep), it adds one before adding the path. Finally, it returns the combined path.
<br><br> **Please note**: This function does not check if the paths exist or are valid, it only combines them based on the rules described. It’s up to the caller to ensure that the paths are valid and exist if necessary.
>This method is intended to concatenate individual strings into a single string that represents a file path. However, if an argument other than the first contains a rooted path, any previous path components are ignored, and the returned string begins with that rooted path component. As an alternative to the `combine` method, consider using the `join` method.
</details>

<details>
<summary>create_directory(path, create_subdirs=True)</summary>

```py
wra.create_directory(path, create_subdirs=True)
```

This function is used to create a directory at the specified `path`. If `create_subdirs` is `True`, the function creates all intermediate-level directories needed to contain the leaf directory. If `create_subdirs` is `False`, the function will raise an error if the directory already exists or if any intermediate-level directories in the path do not exist. Default is **`True`**
<br>If the directories already exist, it does nothing.
</details>

<details>
<summary>create_file(file_name, path, text, encoding="utf-8-sig"):</summary>

```py
wra.create_file(file_name, path, text, encoding="utf-8-sig")
```

The function attempts to open a file at the specified `path` with the given `file_name` (with extension), in write mode with the specified `encoding`. It then writes the provided `text` into the file.
</details>

<details>
<summary>delete(path, recursive=False)</summary>

```py
wra.delete(path, recursive=False)
```

This function is designed to delete a directory at a given `path`.
<br>If `recursive` is set to `True`, the function will delete the directory and all its contents. If it’s `False`, the function will only delete the directory if it’s empty. Default is **`False`**.
</details>

<details>
<summary>enumerate_files(path)</summary>

```py
wra.enumerate_files(path)
```

This function performs a depth-first traversal of the directory tree at the given path (after expanding any user home directory symbols). It returns a list of dictionaries containing the attributes of each file and directory in the tree.
</details>

<details>
<summary>get_files(path):</summary>

```py
wra.get_files(path)
```

This function takes a path as input (which can include wildcards), expands any user home directory symbols (`~`), and returns a list of dictionaries containing the attributes of each file or directory that matches the path.
</details>

<details>
<summary>get_object(path):</summary>

```py
wra.get_object(path)
```

This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).
</details>

<details>
<summary>join(path1='', path2='', path3='', path4='', paths=[]):</summary>

```py
wra.join(path1='', path2='', path3='', path4='', paths=[])
```

This function is designed to concatenate directory paths. It takes four optional string parameters `path1`, `path2`, `path3`, `path4` and an optional list of paths `paths`. The function returns a single string that represents the concatenated path.
<br> For each of the parameters `path1`, `path2`, `path3`, and `path4`, the function checks if the path ends with a separator. If it doesn’t, and the path is not an empty string, it adds a separator to the end of the path.
<br>If the paths list is provided and is not empty, the function iterates over each item in the list. For each item, it checks if the item ends with a separator. If it doesn’t, it adds a separator to the end of the item.
<br>Finally, the function returns the concatenated path.
<br><br> **Please note**: This function does not check if the paths exist or are valid, it only combines them based on the rules described. It’s up to the caller to ensure that the paths are valid and exist if necessary.
> Unlike the `combine` method, the `join` method does not attempt to root the returned path. (That is, if `path2` or `path3` or `path4` is an absolute path, the `join` method does not discard the previous paths as the `combine` method does.)
</details>

<details>
<summary>list_directories(path):</summary>

```py
wra.list_directories(path)
```

This function returns a list of all the directories in a given directory.
</details>

<details>
<summary>list_files(path):</summary>

```py
wra.list_files(path)
```

This function returns a list of all the files in a given directory.
</details>

<details>
<summary>make_zip(source, destination):</summary>

```py
wra.make_zip(source, destination)
```

This function is used to create a zip archive of a given source directory and move it to a specified destination.
</details>

## Sample Codes

<details>
<summary>Wrapper: Creating a Folder</summary>

The following example shows how to create a new directory named `database` inside the `Documents` directory using **Wrapper**

```py
import filesystem as fs
from filesystem import wrapper as wra

bd_folder = "database"
try:
   wra.create_directory(f'{fs.documents}/{bd_folder}')
except:
   print("Could`t create the folder")
```
</details>

<details>
<summary>Wrapper: Get Files</summary>

1. **Get Files:**

The following example shows how to get files information from **Downloads** folder.

```py
import filesystem as fs
from filesystem import wrapper as wra

pointers = wra.get_files(f'{fs.downloads}/*')
print(pointers)
```

Output:

```py
[{'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}, {'modified': 1697605101.6574, 'created': 1697683292.4821024, 'access': 1697683294.46923, 'name': 'Python_Logo.png', 'size': 747809, 'abspath': '/Users/YOU/Downloads/Python_Logo.png', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'png'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697682292.5433743, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}]
```

#

2. **Filter Files by Extension:**

The following example is using a list comprehension to filter out files with extension `.py` from the pointers list:

```py
py_files = [x for x in pointers if x["extension"] == "py"]
print(py_files)
```

```py
[{'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697681829.0075543, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}]
```

#

3. **Get File Names Inside the Filter:**
The following code is using a list comprehension that prints the names of all filtered files in the `py_files` list:

```py
print([x["name"] for x in py_files])
```

Output:

```sh
['CLI.py', 'Sample_File.py']
```
</details>

<details>
<summary>Wrapper: Enumerate files (walk recursively) from a directory</summary>

The following code is using a list comprehension to generate a list of all files in the **Downloads** directory:

```py
tree = [x for x in wra.enumerate_files(fs.downloads)]
print(tree)
```

Output:

```py
[{'modified': 1697683292.4821026, 'created': 1697683292.4821026, 'access': 1697683292.484029, 'name': 'Downloads', 'size': 224, 'abspath': '/Users/YOU/Downloads', 'dirname': '/Users/YOU', 'is_dir': True, 'is_file': False, 'is_link': False, 'exists': True, 'extension': ''}, {'modified': 1697683288.8639557, 'created': 1697683288.8639557, 'access': 1697602943.1846778, 'name': '.DS_Store', 'size': 6148, 'abspath': '/Users/YOU/Downloads/.DS_Store', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'DS_Store'}, {'modified': 1690685751.342114, 'created': 1690685751.4194765, 'access': 1690685751.342114, 'name': '.localized', 'size': 0, 'abspath': '/Users/YOU/Downloads/.localized', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'localized'}, {'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}, {'modified': 1697605101.6574, 'created': 1697683292.4821024, 'access': 1697683294.46923, 'name': 'Python_Logo.png', 'size': 747809, 'abspath': '/Users/YOU/Downloads/Python_Logo.png', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'png'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697682292.5433743, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}]
```
</details>

---

# Watcher

```py
from filesystem import watcher as wat
```

Watcher serves as a monitoring system for the file system. It keeps track of any changes made within the file system, such as the creation of new files, modification of existing files, or deletion of files. This feature allows for real-time updates and can be particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial.

<details>
<summary>__init__(self, root):</summary>

This is the constructor method that initializes the `Watcher` object with a root directory to watch. It also saves the current state of the file system in `self.saved_state`.
</details>
<details>
<summary>get_state(self, path):</summary>

This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the `wrapper.enumerate_files(path)` function.
</details>
<details>
<summary>diff(self):</summary>

This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.
</details>
<details>
<summary>__str__(self):</summary>

This method returns a string representation of the `Watcher` object.
</details>

<!-- <details>
<summary>List Of Functions </summary>

Watcher is used to monitor changes in a file system.

- `__init__(self, root)`: This is the constructor method that initializes the `Watcher` object with a root directory to watch. It also saves the current state of the file system in `self.saved_state`.

- `get_state(self, path)`: This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the `core.enumerate_files(path)` function.

- `diff(self)`: This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.

- `__str__(self)`: This method returns a string representation of the `Watcher` object.
</details> -->

This class could be useful in scenarios where you need to monitor changes to a file system, for example, in a backup system or a live syncing service.

## Sample Codes

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

Copyright © 2023 Bisneto Inc. All rights reserved.