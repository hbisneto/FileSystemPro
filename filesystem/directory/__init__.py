import glob
import os
import shutil
from filesystem import wrapper as wra

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

def create(path, create_subdirs=True):
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
    # return get_object(path)

def delete(path, recursive=False):
    """
    This function is designed to delete a directory at a given `path`.
    
    If `recursive` is set to `True`, the function will delete the directory and all its contents. 
    
    If `recursive` is set to `False`, the function will only delete the directory if it's empty. 
    
    Default is `False`.
    """
    if not os.path.exists(path):
        raise Exception(f'\n\n>> The directory "{path}" does not exist.')

    if not os.listdir(path) or recursive:
        shutil.rmtree(path)
    else:
        raise Exception(f'\n\n>> The directory "{path}" is not empty.\n>> Use delete(path, True) to remove anyway.')

def exists(directory_path):
    if os.path.isdir(directory_path):
        return True
    else:
        return False

def get_files(path):
    """
    This function takes a path as input (which can include wildcards), 
    expands any user home directory symbols (~), and returns a list of dictionaries containing 
    the attributes of each file or directory that matches the path.
    """
    path = os.path.expanduser(path)
    result = []
    for x in glob.glob(path):
        result.append(wra.get_object(x))
    return result

def get_parent_name(path):
    if path.endswith('/'):
        path = path[:-1]
        return os.path.basename(path)
    return os.path.basename(os.path.dirname(path))

def get_parent(path):
        """
        This function returns the parent directory of the given path.
        
        Parameters:
        path (str): The path of which to find the parent directory. Can be absolute or relative.

        Returns:
        str: The parent directory of the given path.
        """
        return os.path.dirname(path)

def get_name(path):
    if wra.has_extension(path):
        return f'{get_parent_name(path)}'
    else:
        return os.path.basename(os.path.dirname(path + '/'))

def join(path1='', path2='', path3='', path4='', paths=[]):
    """
    This function concatenates multiple directory paths into a single path string.

    Parameters:
    - path1, path2, path3, path4 (str): Individual directory paths. Default is an empty string.
    - paths (list): A list of additional directory paths. Default is an empty list.

    The function checks each path and if the path does not end with an OS-specific separator (`os.sep`),
    it appends the separator to the path. This is done for `path1`, `path2`, `path3`, `path4`,
    and each path in the `paths` list.

    The function then concatenates all the paths into a single string `key_dir`.

    Returns:
    - key_dir (str): The concatenated directory path string. The trailing separator is removed before returning.
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
    
def list(path):
    """
    Lists all the directories in a given path
    """
    directory_list = []
    for dir in os.listdir(path):
        if os.path.isdir(join(path, dir)):
            directory_list.append(dir)
    
    return directory_list

def rename(old_directory_path, new_directory_path):
    # Check if the old directory exists
    if os.path.isdir(old_directory_path):
        os.rename(old_directory_path, new_directory_path)
        # print(f"Directory '{old_directory_path}' has been renamed to '{new_directory_path}'.")
        return True
    else:
        # print(f"The directory '{old_directory_path}' does not exist.")
        return False
