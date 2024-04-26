import filesystem
from filesystem import webclient

webclient.download_file(
    "https://dl.dropboxusercontent.com/scl/fi/kmgl5z7elx62ys24zqwaw/UpdateContent.zip?rlkey=akjgiwc0kmmjnfbetwe2r0lfv&dl=0",
    f'{filesystem.documents}/Test/Dropbox/download.zip',
    )
