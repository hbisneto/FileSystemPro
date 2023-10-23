import codecs
import glob
import os
import shutil

def create_directory(path, create_subdirs=True):
    if create_subdirs:
        os.makedirs(path, exist_ok=True)
    else:
        os.mkdir(path)

def create_file(file_name, path, text):
    """
#### Create a file in UTF-8 encode and write a string of text to this file.

filename: The name of the file you want to create, including its extension.
path: The directory where the file will be created.
text: The content that will be written into the file.

Usage Example:

```
import filesystem as fs
from filesystem import wrapper as wr
create_file("MarketList.txt", "/Users/YOU/Downloads", "This is an inline text")
```
    """

    try:
        with codecs.open(f'{path}/{file_name}', "w", "utf-8-sig") as custom_file:
            custom_file.write(text)
            custom_file.close()
    except:
        pass

def delete(path, recursive=False):
    if os.path.exists(path):
        if recursive:
            shutil.rmtree(path)
        else:
            if not os.listdir(path):
                os.rmdir(path)
            else:
                print(f'\n\n>> The directory "{path}" is not empty.\n>> Use delete(path, True) to remove anyway.')
    else:
        print(f'\n\n>> The directory "{path}" does not exist.')

def enumerate_files(path):
    results = []
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        results.append(get_path_properties(root))
        results.extend([get_path_properties(os.path.join(root,x)) for x in files])
    return results

def get_files(path):
    path = os.path.expanduser(path)
    print(path)
    result = []
    for x in glob.glob(path):
        result.append(get_path_properties(x))
    return result

def get_path_properties(pathname):
    def path_properties(pathname, fun, default=-1):
        try:
            return fun(pathname)
        except:
            return default
        
    head, tail = os.path.split(pathname)

    result = {}
    result["modified"] = path_properties(pathname, os.path.getmtime)
    result["created"] = path_properties(pathname, os.path.getctime)
    result["access"] = path_properties(pathname, os.path.getatime)
    result["name"] = tail
    result["name"] = tail
    result["size"] = path_properties(pathname, os.path.getsize)
    result["abspath"] = os.path.abspath(pathname)
    result["dirname"] = os.path.dirname(pathname)
    result["is_dir"] = os.path.isdir(pathname)
    result["is_file"] = os.path.isfile(pathname)
    result["is_link"] = os.path.islink(pathname)
    result["exists"] = os.path.exists(pathname)
    result["ext"] = tail.split(".")[-1] if result["is_file"] else ""
    return result

def list_directories(path):
    """
    Lists all the directories in a given path
    """
    directory_list = []
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            directory_list.append(dir)
    
    return directory_list

def list_files(path):
    """
    Lists all the files inside of a given path
    """
    file_list = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            file_list.append(file)
    return file_list