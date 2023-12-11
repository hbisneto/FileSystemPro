import codecs
import glob
import os
import shutil

def combine(*args, paths=[]):
    """
    This function is designed to combine file or directory paths. 
    It takes any number of arguments `*args` and an optional parameter paths which is a list of paths.
    The function returns a combined path based on the inputs.
    
    If the paths list is provided, the function uses it to combine paths. 
    It starts with the first path in the list and checks if it's an absolute path. 
    If it's not, it raises a `ValueError` with a detailed error message. 
    Then, it iterates over the rest of the paths in the list. 
    If a path is absolute, it replaces the current result with this path. 
    If a path is relative, it joins this path to the current result. Finally, it returns the combined path.
    
    If the paths list is not provided or is empty, the function uses the arguments passed `*args`.
    It starts with the first argument and checks if it's an absolute path.
    If it's not, it raises a `ValueError` with a detailed error message. 
    Then, it iterates over the rest of the arguments.
    If an argument is an absolute path, it replaces the current result with this path. 
    If an argument is a relative path and not an empty string, it adds this path to the current result. 
    If the current result doesn't end with a separator (os.sep), it adds one before adding the path.
    Finally, it returns the combined path.
    
    Please note: This function does not check if the paths exist or are valid, it only combines them based
    on the rules described.
    It's up to the caller to ensure that the paths are valid and exist if necessary.

    ```py
    from filesystem import wrapper as wr

    # Combine absolute and relative paths
    result = wr.combine('/home/user', 'directory', 'file.txt')
    print(result)  
    # Outputs: '/home/user/directory/file.txt'

    # Use an absolute path in the middle
    result = wr.combine('/home/user', '/otheruser', 'file.txt')
    print(result)
    # Outputs: '/otheruser/file.txt'

    # Use the paths parameter
    result = wr.combine(paths=['/home/user', 'directory', 'file.txt'])
    print(result)
    # Outputs: '/home/user/directory/file.txt'
    ```

    """
    if paths:
        result = paths[0]
        if not os.path.isabs(result):
            raise ValueError(
f'''Invalid argument: The path "{result}" is not an absolute path.
- The first argument inside paths list must to be an absolute path.

For example, "/home/user/directory" is a valid absolute path. Please provide a valid absolute path.

'''
)
        for path in paths:
            if os.path.isabs(path):
                result = path
            else:
                result = join(result, path)
        return result

    result = args[0]
    if not os.path.isabs(result):
        raise ValueError(
f'''Invalid argument: The path "{result}" is not an absolute path.
- The first argument must to be an absolute path.

For example, "/home/user/directory" is a valid absolute path. Please provide a valid absolute path.

'''
)
    for path in args[1:]:
        if path == '':
            continue
        if os.path.isabs(path):
            result = path
        else:
            if not result.endswith(os.sep):
                result += os.sep
            result += path
    return result
    
def create_directory(path, create_subdirs=True):
    """
    This function is used to create a directory at the specified `path`.
    
    If `create_subdirs` is `True`, the function creates all intermediate-level directories needed to contain 
    the leaf directory. 
    
    If `create_subdirs` is `False`, the function will raise an error if the directory already exists or if any
    intermediate-level directories in the path do not exist.
    
    Default is `True`
    
    If the directories already exist, it does nothing.
    """
    if create_subdirs:
        os.makedirs(path, exist_ok=True)
    else:
        os.mkdir(path)
    return get_object(path)

def create_file(file_name, path, text, encoding="utf-8-sig"):
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
        with codecs.open(f'{path}/{file_name}', "w", encoding=encoding) as custom_file:
            custom_file.write(text)
    except:
        pass
    return get_object(f'{path}/{file_name}')

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
    This function performs a depth-first traversal of the directory tree at the given path 
    (after expanding any user home directory symbols).
    
    It returns a list of dictionaries containing the attributes of each file and directory in the tree.
    """
    results = []
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        results.append(get_object(root))
        results.extend([get_object(join(root,x)) for x in files])
    return results

def get_files(path):
    """
    This function takes a path as input (which can include wildcards), 
    expands any user home directory symbols (~), and returns a list of dictionaries containing 
    the attributes of each file or directory that matches the path.
    """
    path = os.path.expanduser(path)
    result = []
    for x in glob.glob(path):
        result.append(get_object(x))
    return result

def get_object(path):
    """
    This function takes a file or directory path as input and returns a dictionary containing various attributes 
    of the file or directory. 
    These attributes include the time of last modification, creation time, last access time, name, size,
    absolute path, parent directory, whether it's a directory or file or link, whether it exists, and its extension
    (if it's a file).
    """
    def path_properties(path, fun, default=-1):
        try:
            return fun(path)
        except:
            return default
        
    head, tail = os.path.split(path)

    result = {}
    result["abspath"] = os.path.abspath(path)
    result["access"] = path_properties(path, os.path.getatime)
    result["created"] = path_properties(path, os.path.getctime)
    result["dirname"] = os.path.dirname(path)
    result["exists"] = os.path.exists(path)
    result["is_dir"] = os.path.isdir(path)
    result["is_file"] = os.path.isfile(path)
    result["is_link"] = os.path.islink(path)
    result["extension"] = tail.split(".")[-1] if result["is_file"] else ""
    ### EXT kept to cover version support. Remove on (MAJOR UPDATE ONLY)
    result["ext"] = tail.split(".")[-1] if result["is_file"] else ""
    result["modified"] = path_properties(path, os.path.getmtime)
    result["name"] = tail
    result["name_without_extension"] = tail.split('.')[0]
    result["size"] = path_properties(path, os.path.getsize)
    return result

def join(path1='', path2='', path3='', path4='', paths=[]):
    """
    This function is designed to concatenate directory paths. 
    It takes four optional string parameters `path1`, `path2`, `path3`, `path4`
    and an optional list of paths `paths`. 
    The function returns a single string that represents the concatenated path. 
    For each of the parameters `path1`, `path2`, `path3`, and `path4`,
    the function checks if the path ends with a separator.
    If it doesn't, and the path is not an empty string, it adds a separator to the end of the path. 
    If the `paths` list is provided and is not empty, the function iterates over each item in the list.
    For each item, it checks if the item ends with a separator.
    If it doesn't, it adds a separator to the end of the item. 
    Finally, the function returns the concatenated path. 

    Please note: This function does not check if the paths exist or are valid, 
    it only combines them based on the rules described. 
    It's up to the caller to ensure that the paths are valid and exist if necessary.

    Unlike the `combine` method, the `join` method does not attempt to root the returned path. 
    (That is, if `path2` or `path3` or `path4` is an absolute path, the `join` method does not discard the previous paths 
    as the `combine` method does.)
    
    ```py
    from filesystem import wrapper as wr

    # Combine paths
    result = wr.join('home', 'user', 'directory', 'file.txt')
    print(result)
    # Outputs: 'home/user/directory/file.txt'

    # Use the paths parameter
    result = wr.join(paths=['home', 'user', 'directory', 'file.txt'])
    print(result)
    # Outputs: 'home/user/directory/file.txt'
    ```

    """
    key_dir = ""
    if not path1.endswith(os.sep):
        if path1 != "":
            path1 = path1 + os.sep
    key_dir += path1
    if not path2.endswith(os.sep):
        if path2 != "":
            path2 = path2 + os.sep
    key_dir += path2
    if not path3.endswith(os.sep):
        if path3 != "":
            path3 = path3 + os.sep
    key_dir += path3
    if not path4.endswith(os.sep):
        if path4 != "":
            path4 = path4 + os.sep
    key_dir += path4

    if paths:
        for item in paths:
            if not item.endswith(os.sep):
                item = item + os.sep
            key_dir += item
    return key_dir[:-1]

def list_directories(path):
    """
    Lists all the directories in a given path
    """
    directory_list = []
    for dir in os.listdir(path):
        if os.path.isdir(join(path, dir)):
            directory_list.append(dir)
    
    return directory_list

def list_files(path):
    """
    Returns a list containing all the files inside of a given path
    """
    file_list = []
    for file in os.listdir(path):
        if os.path.isfile(join(path, file)):
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
