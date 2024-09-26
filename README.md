# FileSystem Pro 

FileSystem is a powerful toolkit designed to handle file and directory operations with ease and efficiency across various operating systems.

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

### To Developers / Contributors

Clone this repository to your local machine using:

```sh
git clone https://github.com/hbisneto/FileSystemPro.git
```

Install setuptools / Upgrade setuptools

```sh
pip install --upgrade setuptools
```

> [!NOTE]
> Note: FileSystem Pro requires setuptools 69.5.1 or later.
><br> Python environment typically targets setuptools version 49.x.

Install wheel / Upgrade wheel

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
	    prints the OS separator
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

# Console

```py
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

# Directory

```py
from filesystem import directory as dir
```

The Directory module is a component of the FileSystemPro library that provides a collection of functions
for handling directory-related operations. It simplifies tasks such as path manipulation, 
directory creation and deletion, and file retrieval within directories.

## Features
- **Path Combination:** Dynamically combines multiple paths into a single path string.
- **Directory Creation:** Creates new directories, with an option to create necessary subdirectories.
- **Directory Deletion:** Deletes directories, with an option for recursive deletion.
- **Directory Existence Check:** Checks whether a directory exists at a specified path.
- **File Retrieval:** Retrieves a list of files within a directory using glob patterns.
- **Parent Directory Information:** Retrieves the name or path of a file's parent directory.
- **Directory Listing:** Lists all subdirectories within a given directory.
- **Directory Renaming:** Renames a directory if it exists.

<table>
  <tr>
  	<th>Method</th>
  	<th>Description</th>
  </tr>
  
  <tr>
    <td>directory.combine(*args, paths=[])</td>
    <td>
      Combines a list of paths or arguments into a single path. If the first argument or the first element in the paths list is not an absolute path, it raises a ValueError.
    </td>
  </tr>
  
  <tr>
    <td>directory.create(path, create_subdirs = True)</td>
    <td>
      Creates a directory at the specified path. If `create_subdirs` is True, all intermediate-level 
    directories needed to contain the leaf directory will be created. After the directory is created, 
    it returns the details of the created directory.
    </td>
  </tr>
  
  <tr>
    <td>directory.delete(path, recursive=False)</td>
    <td>
     Deletes a directory at the specified path. If `recursive` is True, the directory and all its contents will be removed.
  </td>
  
  <tr>
    <td>directory.exists(path)</td>
    <td>
     Checks if a directory exists at the specified path.
  </td>
  
  <tr>
    <td>directory.get_directories(path, fullpath=False)</td>
    <td>
     Retrieves a list of directories within the specified path.
  </td>
  
  <tr>
    <td>directory.get_name(path)</td>
    <td>
     Retrieves the name of the directory of the specified path. 
    If the path has an extension, it is assumed to be a file, and the parent directory name is returned. 
    If the path does not have an extension, it is assumed to be a directory, 
    and the directory name is returned.
  </td>
  
  <tr>
    <td>directory.get_parent_name(path)</td>
    <td>
     Retrieves the parent directory name from the specified path.
  </td>
  
  <tr>
    <td>directory.get_parent(path)</td>
    <td>
     Retrieves the parent directory from the specified path.
  </td>
  
  <tr>
    <td>directory.join(path1='', path2='', path3='', path4='', paths=[])</td>
    <td>
     Joins multiple directory paths into a single path. The function ensures that each directory path ends with a separator before joining. If a directory path does not end with a separator, one is added.
  </td>
  
  <tr>
    <td>directory.rename(old_path, new_path)</td>
    <td>
     Renames a directory from the old directory path to the new directory path. If the old directory path does not exist or is not a directory, the function returns False.
  </td>
  </tr>
</table>

## Sample Codes

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

# File

```py
from filesystem import file as fsfile
```

The File module is a comprehensive utility toolset that forms part of the FileSystemPro library. 
It provides a suite of functions designed to handle various file operations such as integrity checks,
file creation, deletion, enumeration, and file splitting and reassembling.

## Features
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
    <td>file.create(file, data, encoding="utf-8")</td>
    <td>
      Creates a file at the specified path and writes data into it. If the file already exists, 
    its contents are overwritten. The function then returns the details of the created file.
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
    <td>file.get_extension(file_path, lower=True)</td>
    <td>
      Extracts the file extension from the given file path and returns it in lowercase or uppercase based on the `lower` parameter.
    </td>
  </tr>

  <tr>
    <td>file.get_files(path, fullpath=False, extension=None)</td>
    <td>
      Retrieves a list of files from the specified directory. Optionally, it can return the full path of each file and filter files by their extension.
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

## Sample Codes

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

# Wrapper

```py
from filesystem import wrapper as wra
```

Wrapper is a comprehensive toolkit that provides a set of utility functions specifically designed to facilitate file and directory operations. These operations may include creating, reading, updating, and deleting files or directories.

<table>
  <tr>
    <th>Method</th>
    <th>Description</th>
    <th>Status</th>
  </tr>

  <tr>
    <td>wrapper.combine(*args, paths=[])</td>
    <td>
      This function is designed to combine file or directory paths. It takes any number of arguments *args and an optional parameter paths which is a list of paths. The function returns a combined path based on the inputs.
      If the paths list is provided, the function uses it to combine paths. It starts with the first path in the list and checks if it’s an absolute path. If it’s not, it raises a ValueError with a detailed error message. Then, it iterates over the rest of the paths in the list. If a path is absolute, it replaces the current result with this path. If a path is relative, it joins this path to the current result. Finally, it returns the combined path.
      If the paths list is not provided or is empty, the function uses the arguments passed *args. It starts with the first argument and checks if it’s an absolute path. If it’s not, it raises a ValueError with a detailed error message. Then, it iterates over the rest of the arguments. If an argument is an absolute path, it replaces the current result with this path. If an argument is a relative path and not an empty string, it adds this path to the current result. If the current result doesn’t end with a separator (os.sep), it adds one before adding the path. Finally, it returns the combined path.
      <br><br><strong>Please note:</strong> This function does not check if the paths exist or are valid, it only combines them based on the rules described. It’s up to the caller to ensure that the paths are valid and exist if necessary.
      <br><br>This method is intended to concatenate individual strings into a single string that represents a file path. However, if an argument other than the first contains a rooted path, any previous path components are ignored, and the returned string begins with that rooted path component. As an alternative to the combine method, consider using the join method.
    </td>
    <td>
    	Under support. Consider using directory.combine(*args, paths=[])
    </td>
  </tr>


  <tr>
    <td>
      wrapper.create_directory(path, create_subdirs=True)
    </td>
    <td>
      This function is used to create a directory at the specified <strong>path</strong>. If <strong>create_subdirs</strong> is <strong>True</strong>, the function creates all intermediate-level directories needed to contain the leaf directory. If <strong>create_subdirs</strong> is <strong>False</strong>, the function will raise an error if the directory already exists or if any intermediate-level directories in the path do not exist. 
      <br>Default is <strong>True</strong>
      <br>If the directories already exist, it does nothing.
    </td>
    <td>
    	Under support. Consider using directory.create(path, create_subdirs = True)
    </td>
  </tr>

  <tr>
    <td>
      wrapper.create_file(file_name, path, text, encoding="utf-8-sig")
    </td>
    <td>
      The function attempts to open a file at the specified <strong>path</strong> with the given <strong>file_name</strong> (with extension), in write mode with the specified <strong>encoding</strong>. It then writes the provided <strong>text</strong> into the file.
      <br>Finally, it calls Wrapper <strong>get_object</strong> with the full path to the newly created file and returns the resulting dictionary.
    </td>
    <td>
    	Under support. Consider using file.create(file, data, encoding="utf-8-sig")
    </td>
  </tr>

  <tr>
    <td>
      wrapper.delete(path, recursive=False)
    </td>
    <td>
      This function is designed to delete a directory at a given <strong>path</strong>.
      If <strong>recursive</strong> is set to <strong>True</strong>, the function will delete the directory and all its contents. If it’s <strong>False</strong>, the function will only delete the directory if it’s empty. Default is <strong>False</strong>.
    </td>
    <td>
    	Under support. Consider using directory.delete(path, recursive=False)
    </td>
  </tr>
  
  <tr>
    <td>
      wrapper.find_duplicates(path)
    </td>
    <td>
      Finds duplicate files in a given directory and its subdirectories. A file is considered a duplicate if it has the same checksum as another file.
    </td>
    <td>
      Supported
    </td>
  </tr>

  <tr>
    <td>
      wrapper.enumerate_files(path)
    </td>
    <td>
      This function performs a depth-first traversal of the directory tree at the given path (after expanding any user home directory symbols). It returns a list of dictionaries containing the attributes of each file and directory in the tree.
    </td>
    <td>
    	Under support. Consider using file.enumerate_files(path)
    </td>
  </tr>

  <tr>
    <td>
      wrapper.get_files(path)
    </td>
    <td>
      This function takes a path as input (which can include wildcards), expands any user home directory symbols (~), and returns a list of dictionaries containing the attributes of each file or directory that matches the path.
    </td>
    <td>
    	Under support. Consider using file.get_files(path)
    </td>
  </tr>

  <tr>
    <td>
      wrapper.get_object(path)
    </td>
    <td>
      This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).
    </td>
    <td>
    	Supported
    </td>
  </tr>
  
  <tr>
    <td>
      wrapper.get_size(file_path)
    </td>
    <td>
      Calculates the size of the file or directory at the specified path. If the path is a directory, 
      it calculates the total size of all files in the directory. The size is returned in bytes, KB, 
      MB, GB, or TB, depending on the size.
    </td>
    <td>
      Supported
    </td>
  </tr>
  
  <tr>
    <td>
      wrapper.has_extension(file_path)
    </td>
    <td>
      Checks if the given file path has an extension. This function can return True or False based on the string, even if the file or directory does not exist.
    </td>
    <td>
      Supported
    </td>
  </tr>

  <tr>
    <td>
      wrapper.join(path1='', path2='', path3='', path4='', paths=[])
    </td>
    <td>
      This function is designed to concatenate directory paths. It takes four optional string parameters <strong>path1</strong>, <strong>path2</strong>, <strong>path3</strong>, <strong>path4</strong> and an optional list of paths paths. The function returns a single string that represents the concatenated path.
      <br>For each of the parameters <strong>path1</strong>, <strong>path2</strong>, <strong>path3</strong> and <strong>path4</strong>, the function checks if the path ends with a separator. If it doesn’t, and the path is not an empty string, it adds a separator to the end of the path.
      If the paths list is provided and is not empty, the function iterates over each item in the list. For each item, it checks if the item ends with a separator. If it doesn’t, it adds a separator to the end of the item.
      Finally, the function returns the concatenated path.
      <br><br><strong>Please note:</strong> This function does not check if the paths exist or are valid, it only combines them based on the rules described. It’s up to the caller to ensure that the paths are valid and exist if necessary.
      <br><br>Unlike the <strong>combine</strong> method, the <strong>join</strong> method does not attempt to root the returned path. (That is, if <strong>path2</strong> or <strong>path3</strong> or <strong>path4</strong> is an absolute path, the <strong>join</strong> method does not discard the previous paths as the <strong>combine</strong> method does).
    </td>
    <td>
    	Under support. Consider using directory.join(path1='', path2='', path3='', path4='', paths=[])
    </td>
  </tr>

  <tr>
    <td>
      wrapper.list_directories(path)
    </td>
    <td>
      This function returns a list of all the directories in a given directory.
    </td>
    <td>
    	Under support. Consider using directory.get_directories(path)
    </td>
  </tr>

  <tr>
    <td>
      wrapper.list_files(path)
    </td>
    <td>
      This function returns a list of all the files in a given directory.
    </td>
    <td>
    	Under support. Consider using file.get_files(path)
    </td>
  </tr>

  <tr>
    <td>
      wrapper.make_zip(source, destination)
    </td>
    <td>
      This function is used to create a zip archive of a given source directory and move it to a specified destination.
    </td>
    <td>
    	Supported
    </td>
  </tr>
  
  <tr>
    <td>
      wrapper.read_zip_file_contents(zip_filename)
    </td>
    <td>
      Reads the contents of a ZIP file and returns a list of the names of the files contained within it.
    </td>
    <td>
    	New implementation
    </td>
  </tr>
  
</table>

## Sample Codes

<details>
<summary>Wrapper: Make a zip file</summary>

Creates a zip archive of the specified source directory or file and moves it to the specified destination using **Wrapper**

- Creates a zip archive of a **directory** and moves it to a destination.

```python
from filesystem import wrapper as wra

wra.make_zip("/path/to/directory", "/path/to/directory.zip")
```

- Creates a zip archive of a **file** and moves it to a destination.

```python
from filesystem import wrapper as wra

wra.make_zip("/path/to/file.txt", "/path/to/file.zip")
```
</details>

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

<details>
<summary>Wrapper: Get size of file or directory</summary>

Calculates the size of the file or directory at the specified path.

```py
import filesystem as fs
from filesystem import wrapper as wra

documents_size = wra.get_size(fs.documents)

print(documents_size)
```

Output:

```sh
1.6 GB
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

Copyright © 2023–2024 Bisneto Inc. All rights reserved.