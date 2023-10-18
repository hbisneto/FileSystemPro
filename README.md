# FileSystem

FileSystem is designed to identify the operating system (OS) on which it’s running and define the paths to various user directories based on the OS.

## Getting Started

#### Dependencies

It's recommended Python 3.9 or later to use **FileSystem**. You can find it at [python.org](https://www.python.org/).

#### Installation
Clone this repo to your local machine using:

```sh
git clone https://github.com/hbisneto/FileSystem.git
```
## Features
- **Cross-platform Compatibility:** The code is designed to work on multiple operating systems, including Linux, Mac, and Windows. This makes it versatile and adaptable to different environments.
- **Directory Path Identification:** The code identifies and defines the paths to several common user directories based on the operating system. This includes directories like Desktop, Documents, Downloads, Music, Pictures, Public, Videos, and others.
- **Current Working Directory:** The code uses `os.getcwd()` to get the current working directory.
- **String Formatting:** The code uses f-string formatting to create directory paths.

#

## Usage Example

These directories are dynamically generated based on the operating system platform (linux, darwin for Mac, and Windows). Learn more about how to use the library below:

#

<details>
<summary>Default Variables</summary>

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
<summary>Reaching Desktop Folder</summary>

In this exemple of code, we will get the Desktop URL of your operating system.

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
<summary>Creating A Folder</summary>

This exemple shows how to create a folder inside the `Documents` folder.

```py
import filesystem as fs
import os

bd_folder = "database"
try:
   # The directory "database" will be added inside "Documents"
   # /Users/YOU/Documents/database
   os.mkdir(os.path.join(fs.documents, bd_folder))
except:
   print("Could`t create the folder")
```
</details>

#

Copyright © 2023 Bisneto Inc. All rights reserved.
