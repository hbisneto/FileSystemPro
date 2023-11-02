from sys import platform
import os
import getpass

CURRENT_LOCATION = os.getcwd()
"""
Creates a string that represents the path to the current directory. (Where the application is running)
"""

USER_NAME = getpass.getuser()[0].upper() + getpass.getuser()[1:]
"""
Creates a string that represents the username of the user currently logged in to the system.
"""

### WHERE IS THE PUBLIC FOLDER FROM LINUX???
if platform == "linux" or platform == "linux2":
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
elif platform == "darwin":
    PLATFORM_NAME = "Mac"
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
elif platform == "win32" or platform == "win64":
    PLATFORM_NAME = "Windows"
    user = os.environ['USERPROFILE']
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
    public = os.environ['PUBLIC']
    """
    Creates a string that represents the path to the current user's Public folder.
    """
    videos = f'{user}/Videos'
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

```
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