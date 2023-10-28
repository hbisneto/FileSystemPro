from sys import platform
import os
import getpass

CURRENT_LOCATION = os.getcwd()
USER_NAME = getpass.getuser().capitalize()

if platform == "linux" or platform == "linux2":
    PLATFORM_NAME = "Linux"
    user = f'/home/{os.environ["USER"]}'
    desktop = f'{user}/Desktop'
    documents = f'{user}/Documents'
    downloads = f'{user}/Downloads'
    music = f'{user}/Music'
    pictures = f'{user}/Pictures'
    public = f'{user}/Public'
    videos = f'{user}/Videos'
elif platform == "darwin":
    PLATFORM_NAME = "Mac"
    user = f'/Users/{os.environ["USER"]}'
    desktop = f'{user}/Desktop'
    documents = f'{user}/Documents'
    downloads = f'{user}/Downloads'
    music = f'{user}/Music'
    pictures = f'{user}/Pictures'
    public = f'{user}/Public'
    videos = f'{user}/Movies'
elif platform == "win32" or platform == "win64":
    PLATFORM_NAME = "Windows"
    user = os.environ['USERPROFILE']
    desktop = f'{user}/Desktop'
    documents = f'{user}/Documents'
    downloads = f'{user}/Downloads'
    music = f'{user}/Music'
    pictures = f'{user}/Pictures'
    public = os.environ['PUBLIC']
    videos = f'{user}/Videos'
    
linux_templates = f'{user}/Templates'
mac_applications = f'{user}/Applications'
mac_movies = f'{user}/Movies'
windows_applicationData = f'{user}/AppData/Roaming'
windows_localappdata = f'{user}/AppData/Local'
windows_temp = f'{windows_localappdata}/Temp'
windows_favorites = f'{user}/Favorites'