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