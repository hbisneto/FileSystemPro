import requests
import io

def download_data(url):
    response = requests.get(url)
    return bytearray(response.content)

def download_file(url, download_file_path, chunk_size = 1048576):
    response = requests.get(url, stream=True)
    with open(download_file_path, 'wb') as f:
        int_progress = 0
        for chunk in response.iter_content(chunk_size):
            int_progress += 1
            f.write(chunk)

def raw_data(url):
    response = requests.get(url, stream=True)
    return response.raw

def strem_data(url):
    # Send a GET request to the URL with stream=True to get the data as a stream
    response = requests.get(url, stream=True)
    # Convert the raw stream into a BytesIO object for additional functionality
    data_stream = io.BytesIO(response.content)
    # Return the stream
    return data_stream

def open_read_stream(url):
    # Open a stream to point to the data stream coming from the Web resource
    response = requests.get(url)
    # Convert the content of the response to a stream
    stream = io.StringIO(response.text)
    return stream


