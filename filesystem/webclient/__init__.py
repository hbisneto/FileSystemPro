import filesystem as fs
import os
import re
import requests
from filesystem import directory as dir
from filesystem import file as fsfile
from filesystem import wrapper as wra

### ===== TASK 1: CREATE A DOWNLOAD FUNCTION (FOR SMALLER FILES) ===== ###
### CREATE A DOWNLOAD FUNCTION IN THE FULL SIZE (FOR SMALLER DOWNLOADS)
### THIS FUNCTION MUST To DOWNLOAD CONTENT INSIDE A TEMPORARY FILE
### AFTER ALL BYTES DOWNLOADED, 
### THE FILE IS RENAMED ACCORDINGLY TO THE DOWNLOADED NAME AND EXTENSION

### ===== TASK 2: CHANGE THE CURRENT FUNCTIONS NAMES ===== ###
### ===== TASK 3: GET THINGS READY TO LAUNCH ===== ###


def get_sorted_list(path, parts=[]):
    """
    # webclient.get_sorted_list(path, parts=[])
    
    ---

    ### Overview
    Returns a sorted list of file URLs from a specified directory.
    The function filters the files based on a specific pattern and sorts them based on the 
    numerical value after '.fsp' in the filename.

    ### Parameters:
    path (str): The directory path to get the files from.
    parts (list, optional): A list of parts to be included in the sorted list. Defaults to an empty list.

    ### Returns:
    sort_list (list): A sorted list of file URLs.

    ### Raises:
    None

    ### Examples:
    - Gets a sorted list of file URLs from a specified directory.

    ```python
    get_sorted_list("/path/to/directory")
    ```
    - Gets a sorted list of file URLs from a specified directory, including specific parts.

    ```python
    get_sorted_list("/path/to/directory", ["part1", "part2"])
    ```
    """
    files = fsfile.get_files(path)
    sort_list = []

    pattern = re.compile(r'.*\.fsp\d+$')
    filtered_list = list(filter(pattern.match, files))

    sort_parts = sorted(filtered_list, key=lambda x: int(x.split('.fsp')[-1]))
    for part in sort_parts:
        url = f'{path}{fs.OS_SEPARATOR}{part}'
        sort_list.append(url)
    
    return sort_list

def download_in_chunks(url, download_path, filename_extension = None, chunk_size=1048576):
    """
    # webclient.download_in_chunks(url, download_path, filename_extension = None, chunk_size=1048576):
    
    ---

    ### Overview
    Downloads a file in chunks from a given URL and saves it to a specified path. 
    If the file already exists, it will not be downloaded again. After the download, 
    the function reassembles the file and clears the cache.

    ### Parameters:
    url (str): The URL of the file to download.
    download_path (str): The path where the file will be saved.
    filename_extension (str, optional): The extension of the file. 
    If not provided, the basename of the URL or download path will be used. Defaults to None.
    chunk_size (int, optional): The size of the chunks in which the file will be downloaded.
    Defaults to 1048576 (1 MB).

    ### Returns:
    None

    ### Raises:
    - Exception: If the file does not exist at the provided URL (HTTP status code 404).
    - Exception: If an error occurred while trying to access the file (HTTP status code other than 200).

    ### Examples:
    - Downloads a file in chunks and saves it to a specified path.

    ```python
    download_in_chunks("https://example.com/file.zip", "/path/to/save")
    ```
    """
    if wra.has_extension(download_path):
        if filename_extension == None:
            filename_extension = os.path.basename(download_path)  # Obtém "UpdateContent.zip"
        else:
            pass
    else:
        if filename_extension != None:
            filename_extension = filename_extension
        else:
            filename_extension = os.path.basename(url)

    dir.create(download_path)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        index = 0
        for chunk in response.iter_content(chunk_size):
            save_to = f'{download_path}/{filename}.fsp{index}'
            if os.path.exists(save_to) and open(save_to, 'rb').read() == chunk:
                pass # print(f'O arquivo "{save_to}" não será baixado novamente.')
            else:
                with open(save_to, 'wb') as file:
                    file.write(chunk)
                #print(f"Fazendo download do arquivo: {save_to}")
            index += 1
    else:
        if response.status_code != 200:
            if response.status_code == 404:
                raise Exception(
                    f'''Could not download the file from "{url}". 
The file does not exist at the provided URL (HTTP status code 404).
Please check the URL and try again.'''
                    )
            else:
                raise Exception(
                    f'''Could not download the file from "{url}".
An error occurred while trying to access the file (HTTP status code {response.status_code}).
Please check your network connection and the file URL, and try again.'''
                    )
    ### REASSEMBLE THE FILE
    parts = []
    all_files = fsfile.get_files(download_path)
    for file in all_files:
        file = f'{download_path}{fs.OS_SEPARATOR}{file}'
        parts.append(file)
    
    reassemble_cache(
        download_path, 
        output_file=f'{download_path}{fs.OS_SEPARATOR}{filename_extension}',
        parts=get_sorted_list(download_path, parts=parts)
    )

    ### CLEAR ALL THE MESS
    clear_cache(download_path, parts=parts)

def reassemble_cache(download_path, output_file, parts = []):
    """
    # webclient.reassemble_cache(download_path, output_file, parts = [])
    
    ---

    ### Overview
    Reassembles a file from its parts.
    The function reads each part from the download path and writes its contents to the output file.

    ### Parameters:
    download_path (str): The path where the parts of the file are located.
    output_file (str): The path to the output file where the reassembled file will be written.
    parts (list, optional): A list of parts to be included in the reassembled file. Defaults to an empty list.

    ### Returns:
    None

    ### Raises:
    - FileNotFoundError: If a part does not exist at the provided path.
    - PermissionError: If the permission to read a part or write to the output file is denied.

    ### Examples:
    - Reassembles a file from its parts and writes it to a specified output file.

    ```python
    reassemble_cache("/path/to/parts", "/path/to/output/file")
    ```
    - Reassembles a file from specific parts and writes it to a specified output file.

    ```python
    reassemble_cache("/path/to/parts", "/path/to/output/file", ["part1", "part2"])
    ```
    """
    with open(output_file, 'wb') as outfile:
        for part in parts:
            file_path = os.path.join(download_path, part)

            with open(file_path, 'rb') as infile:
                contents = infile.read()
                outfile.write(contents)

def clear_cache(download_path, parts=[]):
    """
    # webclient.clear_cache(download_path, parts=[])
    
    ---

    ### Overview
    Clears the cache by deleting specified files from a given download path. The function first gets a sorted list of files to delete and then deletes each file.

    ### Parameters:
    download_path (str): The path where the files to be deleted are located.
    parts (list, optional): A list of parts to be included in the deletion. Defaults to an empty list.

    ### Returns:
    files_to_delete (list): A list of files that were deleted.

    ### Raises:
    - FileNotFoundError: If a file does not exist at the provided path.
    - PermissionError: If the permission to delete a file is denied.

    ### Examples:
    - Clears the cache by deleting all files from a specified download path.

    ```python
    clear_cache("/path/to/download")
    ```
    - Clears the cache by deleting specific parts from a specified download path.

    ```python
    clear_cache("/path/to/download", ["part1", "part2"])
    ```
    """
    files_to_delete = get_sorted_list(download_path, parts=parts)

    for file in files_to_delete:
        fsfile.delete(file)

    return files_to_delete