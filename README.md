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

---

#### To Developers / Contributors

Clone this repository to your local machine using:

```sh
git clone https://github.com/hbisneto/FileSystemPro.git
```

Install setuptools

```sh
pip install setuptools
```

Upgrade setuptools

```sh
pip install --upgrade setuptools
```
> Note: FileSystem Pro requires setuptools 69.5.1 or later.
><br> Python environment typically targets setuptools version 49.x.

Install wheel

```sh
pip install wheel
```

Upgrade wheel

```sh
pip install --upgrade wheel
```

---

## Features
- **Cross-platform Compatibility:** The code is designed to work on multiple operating systems, including Linux, Mac, and Windows. This makes it versatile and adaptable to different environments.
- **Directory Path Identification:** The code identifies and defines the paths to several common user directories based on the operating system. This includes directories like Desktop, Documents, Downloads, Music, Pictures, Public, Videos, and others.
- **Current Working Directory:** The code uses `os.getcwd()` to get the current working directory.
- **String Formatting:** The code uses f-string formatting to create directory paths.
- **Monitoring System:** Watcher acts as a monitoring system for the file system. It keeps track of all activities within the file system.
- **Change Tracking:** It records any changes made within the file system. This includes the creation of new files, modification of existing files, and deletion of files.
- **Real-Time Updates:** The Watcher provides real-time updates on any changes made within the file system. This ensures that users have the most current information at all times.
- **Integrity Maintenance:** This feature is particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial. By tracking all changes, the Watcher helps ensure that the file system remains accurate and reliable.

---

## FileSystem

```py
import filesystem as fs
```
<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
    <!-- <th>Code Sample</th> -->
  </tr>
  
  <tr>
    <td>
    	CURRENT_LOCATION
    </td>
    <td>
	    Creates a string that represents the path to the current directory. (Where the application is running)
    </td>
    <!-- <td>
	    print(fs.CURRENT_LOCATION)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	OS_SEPARATOR
    </td>
    <td>
	    prints the OS separator
		<br>'/' for macOS and Linux 
		<br>'\\' for Windows
    </td>
    <!-- <td>
	    print(fs.OS_SEPARATOR)
    </td> -->
  </tr>

  <tr>
    <td>
    	USER_NAME
    </td>
    <td>
	    Creates a string that represents the username of the user currently logged in to the system.
    </td>
    <!-- <td>
	    print(fs.USER_NAME)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	user
    </td>
    <td>
	    Creates a string that represents the path to the current user's home directory.
    </td>
    <!-- <td>
	    print(fs.user)
    </td> -->
  </tr>

  <tr>
    <td>
    	desktop
    </td>
    <td>
	    Creates a string that represents the path to the current user's Desktop folder.
    </td>
    <!-- <td>
	    print(fs.desktop)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	documents
    </td>
    <td>
	    Creates a string that represents the path to the current user's Documents folder.
    </td>
    <!-- <td>
	    print(fs.documents)
    </td> -->
  </tr>

  <tr>
    <td>
    	downloads
    </td>
    <td>
	    Creates a string that represents the path to the current user's Downloads folder.
    </td>
    <!-- <td>
	    print(fs.downloads)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	music
    </td>
    <td>
	    Creates a string that represents the path to the current user's Music folder.
    </td>
    <!-- <td>
	    print(fs.music)
    </td> -->
  </tr>

  <tr>
    <td>
    	pictures
    </td>
    <td>
	    Creates a string that represents the path to the current user's Pictures folder.
    </td>
    <!-- <td>
	    print(fs.pictures)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	public
    </td>
    <td>
	    Creates a string that represents the path to the current user's Public folder.
    </td>
    <!-- <td>
	    print(fs.public)
    </td> -->
  </tr>

  <tr>
    <td>
    	videos
    </td>
    <td>
	    Creates a string that represents the path to the current user's Videos folder.
    </td>
    <!-- <td>
	    print(fs.videos)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	linux_templates
    </td>
    <td>
	    Creates a string that represents the path to the current user's Templates folder in Linux environment.
    </td>
    <!-- <td>
	    print(fs.linux_templates)
    </td> -->
  </tr>

  <tr>
    <td>
    	mac_applications
    </td>
    <td>
	    Creates a string that represents the path to the current user's Applications folder in macOS environment.
    </td>
    <!-- <td>
	    print(fs.mac_applications)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	windows_applicationData
    </td>
    <td>
	    Creates a string that represents the path to the current user's Roaming folder inside AppData in Windows environment.
    </td>
    <!-- <td>
	    print(fs.windows_applicationData)
    </td> -->
  </tr>

  <tr>
    <td>
    	windows_favorites
    </td>
    <td>
	    Creates a string that represents the path to the current user's Favorites folder in Windows environment.
    </td>
    <!-- <td>
	    print(fs.windows_favorites)
    </td> -->
  </tr>
  
  <tr>
    <td>
    	windows_localappdata
    </td>
    <td>
	    Creates a string that represents the path to the current user's Local folder inside AppData in Windows environment.
    </td>
    <!-- <td>
	    print(fs.windows_localappdata)
    </td> -->
  </tr>

  <tr>
    <td>
    	windows_temp
    </td>
    <td>
	    Creates a string that represents the path to the current user's Temp folder inside LocalAppData in Windows environment.
    </td>
    <!-- <td>
	    print(fs.windows_temp)
    </td> -->
  </tr>

</table>

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

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
  </tr>

  <tr>
    <td>combine(*args, paths=[])</td>
    <td>
      This function is designed to combine file or directory paths. It takes any number of arguments *args and an optional parameter paths which is a list of paths. The function returns a combined path based on the inputs.
      If the paths list is provided, the function uses it to combine paths. It starts with the first path in the list and checks if it’s an absolute path. If it’s not, it raises a ValueError with a detailed error message. Then, it iterates over the rest of the paths in the list. If a path is absolute, it replaces the current result with this path. If a path is relative, it joins this path to the current result. Finally, it returns the combined path.
      If the paths list is not provided or is empty, the function uses the arguments passed *args. It starts with the first argument and checks if it’s an absolute path. If it’s not, it raises a ValueError with a detailed error message. Then, it iterates over the rest of the arguments. If an argument is an absolute path, it replaces the current result with this path. If an argument is a relative path and not an empty string, it adds this path to the current result. If the current result doesn’t end with a separator (os.sep), it adds one before adding the path. Finally, it returns the combined path.
      <br><br><strong>Please note:</strong> This function does not check if the paths exist or are valid, it only combines them based on the rules described. It’s up to the caller to ensure that the paths are valid and exist if necessary.
      <br><br>This method is intended to concatenate individual strings into a single string that represents a file path. However, if an argument other than the first contains a rooted path, any previous path components are ignored, and the returned string begins with that rooted path component. As an alternative to the combine method, consider using the join method.
    </td>
  </tr>


  <tr>
    <td>
      create_directory(path, create_subdirs=True)
    </td>
    <td>
      This function is used to create a directory at the specified <strong>path</strong>. If <strong>create_subdirs</strong> is <strong>True</strong>, the function creates all intermediate-level directories needed to contain the leaf directory. If <strong>create_subdirs</strong> is <strong>False</strong>, the function will raise an error if the directory already exists or if any intermediate-level directories in the path do not exist. 
      <br>Default is <strong>True</strong>
      <br>If the directories already exist, it does nothing.
    </td>
  </tr>

  <tr>
    <td>
      create_file(file_name, path, text, encoding="utf-8-sig")
    </td>
    <td>
      The function attempts to open a file at the specified <strong>path</strong> with the given <strong>file_name</strong> (with extension), in write mode with the specified <strong>encoding</strong>. It then writes the provided <strong>text</strong> into the file.
      <br>Finally, it calls Wrapper <strong>get_object</strong> with the full path to the newly created file and returns the resulting dictionary.
    </td>
  </tr>

  <tr>
    <td>
      delete(path, recursive=False)
    </td>
    <td>
      This function is designed to delete a directory at a given <strong>path</strong>.
      If <strong>recursive</strong> is set to <strong>True</strong>, the function will delete the directory and all its contents. If it’s <strong>False</strong>, the function will only delete the directory if it’s empty. Default is <strong>False</strong>.
    </td>
  </tr>

  <tr>
    <td>
      enumerate_files(path)
    </td>
    <td>
      This function performs a depth-first traversal of the directory tree at the given path (after expanding any user home directory symbols). It returns a list of dictionaries containing the attributes of each file and directory in the tree.
    </td>
  </tr>

  <tr>
    <td>
      get_files(path)
    </td>
    <td>
      This function takes a path as input (which can include wildcards), expands any user home directory symbols (~), and returns a list of dictionaries containing the attributes of each file or directory that matches the path.
    </td>
  </tr>

  <tr>
    <td>
      get_object(path)
    </td>
    <td>
      This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).
    </td>
  </tr>

  <tr>
    <td>
      join(path1='', path2='', path3='', path4='', paths=[])
    </td>
    <td>
      This function is designed to concatenate directory paths. It takes four optional string parameters <strong>path1</strong>, <strong>path2</strong>, <strong>path3</strong>, <strong>path4</strong> and an optional list of paths paths. The function returns a single string that represents the concatenated path.
      <br>For each of the parameters <strong>path1</strong>, <strong>path2</strong>, <strong>path3</strong> and <strong>path4</strong>, the function checks if the path ends with a separator. If it doesn’t, and the path is not an empty string, it adds a separator to the end of the path.
      If the paths list is provided and is not empty, the function iterates over each item in the list. For each item, it checks if the item ends with a separator. If it doesn’t, it adds a separator to the end of the item.
      Finally, the function returns the concatenated path.
      <br><br><strong>Please note:</strong> This function does not check if the paths exist or are valid, it only combines them based on the rules described. It’s up to the caller to ensure that the paths are valid and exist if necessary.
      <br><br>Unlike the <strong>combine</strong> method, the <strong>join</strong> method does not attempt to root the returned path. (That is, if <strong>path2</strong> or <strong>path3</strong> or <strong>path4</strong> is an absolute path, the <strong>join</strong> method does not discard the previous paths as the <strong>combine</strong> method does).
    </td>
  </tr>

  <tr>
    <td>
      list_directories(path)
    </td>
    <td>
      This function returns a list of all the directories in a given directory.
    </td>
  </tr>

  <tr>
    <td>
      list_files(path)
    </td>
    <td>
      This function returns a list of all the files in a given directory.
    </td>
  </tr>

  <tr>
    <td>
      make_zip(source, destination)
    </td>
    <td>
      This function is used to create a zip archive of a given source directory and move it to a specified destination.
    </td>
  </tr>

</table>

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

```sh
[{'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}, {'modified': 1697605101.6574, 'created': 1697683292.4821024, 'access': 1697683294.46923, 'name': 'Python_Logo.png', 'size': 747809, 'abspath': '/Users/YOU/Downloads/Python_Logo.png', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'png'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697682292.5433743, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}]
```

#

2. **Filter Files by Extension:**

The following example is using a list comprehension to filter out files with extension `.py` from the pointers list:

```py
py_files = [x for x in pointers if x["extension"] == "py"]
print(py_files)
```

```sh
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

```sh
[{'modified': 1697683292.4821026, 'created': 1697683292.4821026, 'access': 1697683292.484029, 'name': 'Downloads', 'size': 224, 'abspath': '/Users/YOU/Downloads', 'dirname': '/Users/YOU', 'is_dir': True, 'is_file': False, 'is_link': False, 'exists': True, 'extension': ''}, {'modified': 1697683288.8639557, 'created': 1697683288.8639557, 'access': 1697602943.1846778, 'name': '.DS_Store', 'size': 6148, 'abspath': '/Users/YOU/Downloads/.DS_Store', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'DS_Store'}, {'modified': 1690685751.342114, 'created': 1690685751.4194765, 'access': 1690685751.342114, 'name': '.localized', 'size': 0, 'abspath': '/Users/YOU/Downloads/.localized', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'localized'}, {'modified': 1695535334.1411633, 'created': 1697604128.7045012, 'access': 1697604129.781534, 'name': 'CLI.py', 'size': 3345, 'abspath': '/Users/YOU/Downloads/CLI.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}, {'modified': 1697605101.6574, 'created': 1697683292.4821024, 'access': 1697683294.46923, 'name': 'Python_Logo.png', 'size': 747809, 'abspath': '/Users/YOU/Downloads/Python_Logo.png', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'png'}, {'modified': 1697681746.0940206, 'created': 1697682027.268841, 'access': 1697682292.5433743, 'name': 'Sample_File.py', 'size': 1031, 'abspath': '/Users/YOU/Downloads/Sample_File.py', 'dirname': '/Users/YOU/Downloads', 'is_dir': False, 'is_file': True, 'is_link': False, 'exists': True, 'extension': 'py'}]
```
</details>

---

# Watcher

```py
from filesystem import watcher as wat
```

Watcher serves as a monitoring system for the file system. It keeps track of any changes made within the file system, such as the creation of new files, modification of existing files, or deletion of files. This feature allows for real-time updates and can be particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial.

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

# Console

```
from filesystem import console as fsconsole
```

Console is a robust library designed to enable ANSI escape character sequences, which are used for generating colored terminal text and cursor positioning.
This library is a key addition to FileSystemPro as a third-party library, enhancing the toolkit for developers who require consistent terminal styling across different operating systems.

## Features

- **Universal Compatibility:** Console ensures that applications or libraries utilizing ANSI sequences for colored output on Unix or Macs can now operate identically on Windows systems.
- **Simplified Integration:** With no dependencies other than the standard library, integrating Console into your projects is straightforward. It’s tested across multiple Python versions, ensuring reliability.
- **Enhanced Terminal Experience:** By converting ANSI sequences into appropriate win32 calls, Console allows Windows terminals to emulate the behavior of Unix terminals, providing a consistent user experience.
- **Effortless Transition:** For developers transitioning to FileSystemPro, incorporating Console into your workflow is effortless, enabling you to maintain the visual aspects of your terminal applications without platform constraints.

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

## Sample Codes

> [!NOTE]
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

Remember, for the color changes to work, your Terminal must support ANSI escape sequences, which are used to set the color. Not all Terminals do, so if you’re not seeing the colors as expected, that could be why. 

---

Copyright © 2023–2024 Bisneto Inc. All rights reserved.