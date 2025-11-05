# -*- coding: utf-8 -*-
#
# filesystem/__init__.py
# FileSystemPro
#
# Created by Heitor Bisneto on 12/11/2025.
# Copyright © 2023–2025 hbisneto. All rights reserved.
#
# This file is part of FileSystemPro.
# FileSystemPro is free software: you can redistribute it and/or modify
# it under the terms of the MIT License. See LICENSE for more details.
#

"""
# FileSystem

---

## Overview
This module serves as the primary entry point for the FileSystemPro package, automatically detecting the operating system (Linux, macOS, or Windows) and defining cross-platform constants for essential paths, such as the user's home directory, common folders (Desktop, Documents, Downloads, Music, Pictures, Public, Videos), and platform-specific locations (e.g., Templates on Linux, Applications on macOS, AppData on Windows). It also provides utility constants like the current working directory, OS path separator, and username (with the first letter capitalized). These constants enable seamless, platform-agnostic file system interactions without manual path construction. Internally, it imports core configuration and console utilities for enhanced functionality.

## Features
- **Platform Detection:** Automatically identifies Linux, macOS, or Windows and sets `PLATFORM_NAME` accordingly.
- **User Directory Constants:** Pre-defined paths for home (`user`), Desktop (`desktop`), Documents (`documents`), Downloads (`downloads`), Music (`music`), Pictures (`pictures`), Public (`public`), and Videos (`videos`).
- **Platform-Specific Paths:** Additional constants like `linux_templates`, `mac_applications`, `mac_movies`, `windows_applicationData`, `windows_favorites`, `windows_localappdata`, and `windows_temp` for specialized folders.
- **Global Utilities:** `CURRENT_LOCATION` (current working directory), `OS_SEPARATOR` (OS-specific path delimiter), and `USER_NAME` (current username with first letter uppercased).
- **Windows Registry Integration:** Uses Windows Registry queries for accurate shell folder paths (e.g., Desktop, Documents).

## Usage
To use these constants, import the module as `filesystem` (or alias as `fs`) and access them directly:

```python
import filesystem as fs
```

### Examples:

- Access platform name and user home directory:

```python
import filesystem as fs
print(f"Platform: {fs.PLATFORM_NAME}")
print(f"Home: {fs.user}")  # e.g., "/home/username" on Linux
```

- Use common folder paths for operations:

```python
import filesystem as fs
desktop_path = fs.desktop
documents_path = fs.documents
print(f"Desktop: {desktop_path}")
print(f"Documents: {documents_path}")
# Example: List files in Downloads
from filesystem import file
files = file.get_files(fs.downloads)
print(files)
```

- Platform-specific paths:

```python
import filesystem as fs
if fs.PLATFORM_NAME == "Windows":
    temp_path = fs.windows_temp
    print(f"Temp: {temp_path}")
elif fs.PLATFORM_NAME == "macOS":
    apps_path = fs.mac_applications
    print(f"Applications: {apps_path}")
```

- OS separator and current location:

```python
import filesystem as fs
print(f"Separator: '{fs.OS_SEPARATOR}'")  # '/' or '\'
print(f"Current Location: {fs.CURRENT_LOCATION}")
print(f"User: {fs.USER_NAME}")  # e.g., "Username"
```
"""

from filesystem import __core__
from .console import console
import getpass
import os
from sys import platform as PLATFORM

CURRENT_LOCATION = os.getcwd()
"""
Creates a string that represents the path to the current directory. (Where the application is running)
"""
OS_SEPARATOR = os.sep
"""
The os.sep is an attribute in the os module in Python. It represents the character that is used by the operating system to separate pathname components, and it varies between different operating systems.

For instance, on Windows, it would return a backslash (\\), while on Unix or Linux, it would return a forward slash (/). So, OS_SEPARATOR will contain the appropriate file path separator for the operating system on which the Python script is running. This is useful for creating file paths in a cross-platform compatible way.

"""
USER_NAME = getpass.getuser()[0].upper() + getpass.getuser()[1:]
"""
Creates a string that represents the username of the user currently logged in to the system.
"""

if PLATFORM == "linux" or PLATFORM == "linux2":
    PLATFORM_NAME = "Linux"
    user = f'/home/{os.environ["USER"]}'
    """
    Creates a string that represents the path to the current user's home directory.
    """
    desktop = f'{user}/Desktop'
    """
    Creates a string that represents the path to the current user's Desktop folder.
    """
    documents = f'{user}/Documents'
    """
    Creates a string that represents the path to the current user's Documents folder.
    """
    downloads = f'{user}/Downloads'
    """
    Creates a string that represents the path to the current user's Downloads folder.
    """
    music = f'{user}/Music'
    """
    Creates a string that represents the path to the current user's Music folder.
    """
    pictures = f'{user}/Pictures'
    """
    Creates a string that represents the path to the current user's Pictures folder.
    """
    public = f'{user}/Public'
    """
    Creates a string that represents the path to the current user's Public folder.
    """
    videos = f'{user}/Videos'
    """
    Creates a string that represents the path to the current user's Videos folder.
    """
elif PLATFORM == "darwin":
    PLATFORM_NAME = "macOS"
    user = f'/Users/{os.environ["USER"]}'
    """
    Creates a string that represents the path to the current user's home directory.
    """
    desktop = f'{user}/Desktop'
    """
    Creates a string that represents the path to the current user's Desktop folder.
    """
    documents = f'{user}/Documents'
    """
    Creates a string that represents the path to the current user's Documents folder.
    """
    downloads = f'{user}/Downloads'
    """
    Creates a string that represents the path to the current user's Downloads folder.
    """
    music = f'{user}/Music'
    """
    Creates a string that represents the path to the current user's Music folder.
    """
    pictures = f'{user}/Pictures'
    """
    Creates a string that represents the path to the current user's Pictures folder.
    """
    public = f'{user}/Public'
    """
    Creates a string that represents the path to the current user's Public folder.
    """
    videos = f'{user}/Movies'
    """
    Creates a string that represents the path to the current user's Videos folder.
    """
elif PLATFORM == "win32" or PLATFORM == "win64":
    PLATFORM_NAME = "Windows"
    import winreg
    def get_registry_paths(folder_name):
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            return winreg.QueryValueEx(key, folder_name)[0]
    
    user = os.environ['USERPROFILE']
    """
    Creates a string that represents the path to the current user's home directory.
    """
    desktop = get_registry_paths("Desktop")
    """
    Creates a string that represents the path to the current user's Desktop folder.
    """
    documents = get_registry_paths("Personal")
    """
    Creates a string that represents the path to the current user's Documents folder.
    """
    downloads = get_registry_paths("{374DE290-123F-4565-9164-39C4925E467B}")
    """
    Creates a string that represents the path to the current user's Downloads folder.
    """
    music = get_registry_paths("My Music")
    """
    Creates a string that represents the path to the current user's Music folder.
    """
    pictures = get_registry_paths("My Pictures")
    """
    Creates a string that represents the path to the current user's Pictures folder.
    """
    public = os.environ['PUBLIC']
    """
    Creates a string that represents the path to the current user's Public folder.
    """
    videos = get_registry_paths("My Video")
    """
    Creates a string that represents the path to the current user's Videos folder.
    """

linux_templates = f'{user}/Templates'
"""
Creates a string that represents the path to the current user's Templates folder in Linux environment.
"""
mac_applications = f'{user}/Applications'
"""
Creates a string that represents the path to the current user's Applications folder in macOS environment.
"""
mac_movies = f'{user}/Movies'
"""
Creates a string that represents the path to the current user's Movies folder in macOS environment.

- Tip: Use `fs.videos` instead:

```python
import filesystem as fs
print(fs.videos)
```
"""
windows_applicationData = f'{user}/AppData/Roaming'
"""
Creates a string that represents the path to the current user's Roaming folder inside AppData in Windows environment.
"""
windows_favorites = f'{user}/Favorites'
"""
Creates a string that represents the path to the current user's Favorites folder in Windows environment.
"""
windows_localappdata = f'{user}/AppData/Local'
"""
Creates a string that represents the path to the current user's Local folder inside AppData in Windows environment.
"""
windows_temp = f'{windows_localappdata}/Temp'
"""
Creates a string that represents the path to the current user's Temp folder inside LocalAppData in Windows environment.
"""