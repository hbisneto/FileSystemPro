# import filesystem
# from filesystem import webclient

# print("[Program]: Your file is downloading...")
# webclient.download_file(
#     "https://dl.dropboxusercontent.com/scl/fi/kmgl5z7elx62ys24zqwaw/UpdateContent.zip?rlkey=akjgiwc0kmmjnfbetwe2r0lfv&dl=0",
#     f'{filesystem.documents}/Test/Dropbox/download.zip',
#     )
# print("[Program]: Your file has been downloaded!")

import requests

def stream_data(url):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk
    else:
        yield 'Error: Unable to download data from {}'.format(url)

# Usage
for chunk in stream_data('http://example.com'):
    print(chunk)



