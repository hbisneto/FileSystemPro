import os

def exists(file):
    """
    This function checks if a given file exists in the file system.
    
    It determines the existence of the file and returns `True` if the file exists, otherwise `False`.

    file: The path to the file to be checked.
    """
    is_file = os.path.isfile(file)
    if is_file:
        return True
    return False

def delete(file):
    """
    This function attempts to delete a file specified by the file parameter.
    
    It first checks if the file exists by calling the exists function.
    If the file is present, it is deleted.
    If the file does not exist, the function does nothing.

    file: The path to the file to be deleted.
    """
    if exists(file):
        os.remove(file)
    else:
        pass
