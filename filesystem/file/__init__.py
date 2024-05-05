import codecs
import hashlib
import os
from filesystem import directory as dir
from filesystem import wrapper as wra

def calculate_checksum(file_path):
    """
    This function calculates the SHA-256 checksum of a file. 
    It takes a file path as an argument and returns the SHA-256 hash of the file's content. 
    
    It first creates a new SHA-256 hash object and opens the file in binary mode for reading.
    It reads the file in chunks of 4096 bytes (or 4KB), updating the hash object with each chunk.
    This is done until there are no more bytes to read from the file.
    Finally, it returns the hexadecimal representation of the hash.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_integrity(file_check, reference_file):
    """
    This function verifies whether the checksum of two files are the same. 
    It takes two arguments:
    
    file_check: The path of the file to be compared
    reference_file: The path of the reference file to be compared
    
    It calculates the checksum of both files using the calculate_checksum function.
    It then checks if the checksums of both files are equal.
    It returns `True` if the checksums are equal (indicating that the files are identical), 
    and `False` otherwise.
    """
    file_to_check = calculate_checksum(file_check)
    reference_check = calculate_checksum(reference_file)

    return file_to_check == reference_check

def create(filename, data, encoding="utf-8-sig"):
    """
    This function is designed to create a file with a specified filename and write data into it.

    filename: The directory where the file will be created, including the name of the file and its extension.
    data: The content that will be written into the file.
    encoding (Optional): It specifies the encoding to be used when opening the file for writing.

    ---

    ### Example
    - Creating a text file in Downloads folder

    ```
    import filesystem as fs
    from filesystem import file as fsfile

    downlods_folder = fs.downloads
    fsfile.create("Marketlist.txt", downlods_folder, "This is an inline text")
    ```

    - Creating a JSON file in Documents folder

    ```
    import filesystem as fs
    from filesystem import file as fsfile

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
    
    fsfile.create("data_person.json", "/Users/YOU/Documents", person)
    ```
    """

    try:
        with codecs.open(f'{filename}', "w", encoding=encoding) as custom_file:
            custom_file.write(data)
    except:
        pass
    # return get_object(f'{filename}')

def create_binary_file(filename, data):
    """
    This function is designed to create a binary file with a given filename and data.

    filename: Refers to the specified path where the new file will be created
    data: Refers to the specific content that will be written into the newly created file.
    """
    if type(data) != bytes:
        b_data = bytes(data.encode())
        with open(filename, 'wb') as binary_file:
            binary_file.write(b_data)
    else:
        with open(filename, 'wb') as binary_file:
            binary_file.write(data)

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

def enumerate_files(file):
    """
    This function performs a depth-first traversal of the directory tree at the given path 
    (after expanding any user home directory symbols).
    
    It returns a list of dictionaries containing the attributes of each file and directory in the tree.
    """
    results = []
    file = os.path.expanduser(file)
    for root, dirs, files in os.walk(file):
        results.append(wra.get_object(root))
        results.extend([wra.get_object(dir.join(root,x)) for x in files])
    return results

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

### Implementarion
def is_file(path):
    return path


def list(path):
    """
    Returns a list containing all the files inside of a given path
    """
    file_list = []
    for file in os.listdir(path):
        if os.path.isfile(dir.join(path, file)):
            file_list.append(file)
    return file_list

def rename(directory, old_name, new_name):
    old_file_path = dir.join(directory, old_name)
    new_file_path = dir.join(directory, new_name)

    # Check if the old file exists
    if exists(old_file_path):
        os.rename(old_file_path, new_file_path)
        # print(f"File '{old_name}' has been renamed to '{new_name}' in the directory '{directory}'.")
        # return True, new_file_path
        return True
    else:
        # print(f"The file '{old_name}' does not exist in the directory '{directory}'.")
        # return False, None
        return False

def reassemble_file(large_file, new_file):
    """
    This function is designed to reassemble a large file that has been split into smaller parts:
    It reassembles a large file that was previously split into parts,
    writes the reassembled content into a new file, and then deletes the part files.
    """
    parts = []
    i = 0
    while os.path.exists(f'{large_file}.fsp{str(i)}'):
        parts.append(f'{large_file}.fsp{str(i)}')
        i += 1

    if len(parts) != 0:
        with open(new_file, 'wb') as output_file:
            for part in parts:
                with open(part, 'rb') as part_file:
                    output_file.write(part_file.read())
            
        for part in parts:
            delete(part)

def split_file(file, chunk_size = 1048576):
    """
    The function `split_file` is designed to split a file into smaller chunks. 
    The default `chunk_size` is set to 1 megabyte (1 MB = 1048576 bytes), but it can be adjusted by providing a different value when calling the function.
    The function does not return any value. 
    It's a straightforward way to handle large files by breaking them down into more manageable pieces.
    """
    if exists(file) == False:
        return False

    with open(file, 'rb') as f:
        chunk = f.read(chunk_size)
        i = 0
        while chunk:
            with open(f'{file}.fsp{str(i)}', 'wb') as chunk_file:
                chunk_file.write(chunk)
            i += 1
            chunk = f.read(chunk_size)
    return True