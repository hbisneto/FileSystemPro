import codecs
import glob
import os
import shutil

def create_directory(path, create_subdirs=True):
    """
    This function is used to create a directory at the specified `path`.
    
    If `create_subdirs` is `True`, the function creates all intermediate-level directories needed to contain the leaf directory. 
    
    If `create_subdirs` is `False`, the function will raise an error if the directory already exists or if any intermediate-level directories in the path do not exist.
    
    Default is `True`
    
    If the directories already exist, it does nothing.
    """
    if create_subdirs:
        os.makedirs(path, exist_ok=True)
    else:
        os.mkdir(path)

def create_file(file_name, path, text):
    """
    ### Create a file in UTF-8 encode and write a string of text to this file.

    filename: The name of the file you want to create, including its extension.
    path: The directory where the file will be created.
    text: The content that will be written into the file.

    ---

    ### Example
    - Creating a text file in Downloads folder

    ```
    import filesystem as fs
    from filesystem import wrapper as wr

    downlods_folder = fs.downloads
    wr.create_file("Marketlist.txt", downlods_folder, "This is an inline text")
    ```

    - Creating a JSON file in Documents folder

    ```
    import filesystem as fs
    from filesystem import wrapper as wr

    person = '''
    {
        "name": "John Doe",
        "age": 30,
        "gender": "Male",
        "nationality": "American",
        "profession": "Software Engineer",
        "address": {
            "street": "Flower Street",
            "number": 123,
            "city": "New York",
            "state": "New York",
            "country": "USA"
        },
        "contact": {
            "phone": "(123) 456-7890",
            "email": "john.doe@example.com"
        },
        "hobbies": ["Reading", "Traveling", "Running"]
    }
    '''
    
    wr.create_file("data_person.json", "/Users/YOU/Documents", person)
    ```
    """

    try:
        with codecs.open(f'{path}/{file_name}', "w", "utf-8-sig") as custom_file:
            custom_file.write(text)
            custom_file.close()
    except:
        pass

def delete(path, recursive=False):
    """
    This function is designed to delete a directory at a given `path`.
    
    If `recursive` is set to `True`, the function will delete the directory and all its contents. 
    
    If `recursive` is set to `False`, the function will only delete the directory if it's empty. 
    
    Default is `False`.
    """
    if not os.path.exists(path):
        print(f'\n\n>> The directory "{path}" does not exist.')
        return

    if not os.listdir(path) or recursive:
        shutil.rmtree(path)
    else:
        print(f'\n\n>> The directory "{path}" is not empty.\n>> Use delete(path, True) to remove anyway.')

def enumerate_files(path):
    """
    This function performs a depth-first traversal of the directory tree at the given path (after expanding any user home directory symbols).
    
    It returns a list of dictionaries containing the attributes of each file and directory in the tree.
    """
    results = []
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        results.append(get_path_properties(root))
        results.extend([get_path_properties(os.path.join(root,x)) for x in files])
    return results

def get_files(path):
    """
    This function takes a path as input (which can include wildcards), expands any user home directory symbols (~), and returns a list of dictionaries containing the attributes of each file or directory that matches the path.
    """
    path = os.path.expanduser(path)
    print(path)
    result = []
    for x in glob.glob(path):
        result.append(get_path_properties(x))
    return result

def get_path_properties(pathname):
    """
    This function takes a file or directory path as input and returns a dictionary containing various attributes of the file or directory. These attributes include the time of last modification, creation time, last access time, name, size, absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension (if it's a file).
    """
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

def make_zip(source, destination):
    """
    This function is used to create a zip archive of a given source directory and move it to a specified destination.
    """
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format), destination)