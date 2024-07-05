### App.py
# This file is used to test only. It will not remain in the project.
# Delete this file after tests for the main branch

import filesystem as fs
from filesystem import file as fsfile

common, difference = fsfile.compare(f'{fs.documents}/Test/log.txt', f'{fs.documents}/Test/log_upd.txt')

for i in difference:
    print(f'Different Lines: {i}')