import hashlib
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
