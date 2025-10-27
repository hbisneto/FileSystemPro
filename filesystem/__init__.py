"""
# FileSystem

---

## Overview
FileSystem is a library for managing file paths in a user's system, 
depending on the operating system (OS) they are using.
It uses Python's built-in libraries like `os`, `sys`, and `getpass` to interact with the system and
manage file paths.

Here's a brief description of what the code does:

1. `User Identification:` It identifies the current user using the `getpass.getuser()`
function and stores the username with the first letter capitalized.

2. `Platform Identification:` It identifies the platform (OS) using `sys.platform`. 
Depending on whether the platform is Linux, macOS, or Windows, it sets up different file paths.

3. `File Paths:` For each platform, it sets up file paths for common user directories like Desktop,
Documents, Downloads, Music, Pictures, Public, and Videos.
The paths are formed using the user's home directory path and the standard directory names for each platform.

   - For `Linux`, it uses the `/home/{username}` directory as the base.
   - For `macOS`, it uses the `/Users/{username}` directory as the base.
   - For `Windows`, it uses the `USERPROFILE` environment variable to get the base directory.

4. `Special Directories:` Apart from the common directories, it also sets up paths for some
special directories based on the platform. For example, `Templates` in Linux, `Applications` and
`Movies` in macOS, and several `AppData` related paths in Windows.

This library can be useful for scripts that need to work with user files and need to be compatible across
different operating systems. 
It provides an easy way to get the correct file paths regardless of the platform.
"""

import getpass
import os
from sys import platform as PLATFORM

## VERIFY IF THE LIBRARY HAS SOME AVAILABLE UPDATE
from filesystem import __core__
## VERIFY IF THE LIBRARY HAS SOME AVAILABLE UPDATE

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