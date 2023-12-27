import getpass
import os
# import requests
from sys import platform as PLATFORM

__version__ = "1.1.0.0"

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

# def __checkupdates__(user, repo):
#     ### TAG PATTERN: v1.2.3.4
#     current_version_string = ''.join(filter(str.isdigit, __version__))
#     current_version = int(current_version_string)
#     update_version = 0

#     ### Check updates online using 'requests'
#     url = f'https://api.github.com/repos/{user}/{repo}/releases'
#     response = requests.get(url)
#     releases = response.json()
    
#     for release in releases:
#         if update_version == 0:
#             tag_name = f'{release["tag_name"]}'
#             update_version_string = ''.join(filter(str.isdigit, tag_name))
#             update_version = int(update_version_string)

#     if int(update_version_string[0]) > int(current_version_string[0]):
#         print("="*80)
#         print(">> FileSystem Pro: New update is available!")
#         print("="*80)
#         print(f">> You are running version (v{__version__}), but a new version ({tag_name}) is available!")
#         print(">> You can run pip install --upgrade filesystempro")
#         print("="*80)

# __checkupdates__("hbisneto","FileSystemPro")