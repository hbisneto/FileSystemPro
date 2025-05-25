"""
# Watcher

---

## Overview
The Watcher module is a part of the FileSystemPro library that provides file monitoring capabilities.
It is designed to track changes within a specified directory, 
alerting users to any modifications, creations, or deletions of files.

## Features
- `Real-Time Monitoring:` Continuously monitors a directory for any file changes.
- `Change Detection:` Identifies updated, created, or removed files since the last check.
- `State Preservation:` Maintains a record of the directory's state for comparison.

## How It Works
The `Watcher` class within the module is initialized with a root directory to monitor. 
It uses the `get_state` method to create a snapshot of the current state of the directory, 
mapping absolute file paths to their metadata.

### State Tracking
Upon initialization, `Watcher` stores the state of the directory. 
The `diff` method compares the current state with the saved state to detect any changes. 
It categorizes changes into three types:
- `Updated:` Files that have been modified since the last state.
- `Created:` New files that have been added to the directory.
- `Removed:` Files that have been deleted from the directory.

### Results
The `diff` method returns a list of changes,
with each entry containing the file's path and the type of change. 
This allows for easy integration with other systems that may need to respond to file system events.

## Usage
To use the `Watcher` module, instantiate the `Watcher` class with the directory you wish to monitor:

```python
from filesystem import watcher as wat
watcher = wat('/path/to/directory')
```
"""
import time
from datetime import datetime
from filesystem import file as fsfile

class Watcher(object):
    """
    Watcher Class
    """
    def __init__(self, root):
        """
        This is the constructor method that initializes the Watcher object with a root directory to watch
        """
        self.root = root
        self.saved_state = self.get_state(root)

    def get_state(self, path):
        """
        This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the core.enumerate_files(path) function
        """
        files = fsfile.enumerate_files(path)
        named_files = dict([(x["abspath"], x,) for x in files])
        return named_files

    def diff(self):
        """
        This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.
        """
        current_state = self.get_state(self.root)
        changed = []
        for k, v1 in current_state.items():
            if k not in self.saved_state:
                continue
            v2 = self.saved_state[k]
            if v1["modified"] != v2["modified"]:
                changed.append(k)
        
        current_set = set(current_state.keys())
        stored_set = set(self.saved_state)
        
        created =  current_set.difference(stored_set)
        removed =  stored_set.difference(current_set)
        
        results = []
        for x in changed:
            i = current_state[x]
            i["change"] = "updated"
            results.append(i)
        
        for x in created:
            i = current_state[x]
            i["change"] = "created"
            results.append(i)

        for x in removed:
            i = self.saved_state[x]
            i["change"] = "removed"
            results.append(i)
        
        self.saved_state = current_state
        return results

    def __str__(self):
        """
        This method returns a string representation of the Watcher object.
        """
        return "filesystem.Watcher: %s" % (self.root)

def get_changes(directory:str, delay=5.0, create_log_file=False, log_filename="FSWatcherLog.log"):
    watcher = Watcher(directory)
    while True:
        changes = watcher.diff()
        if changes:
            print(f"Changes detected at: {datetime.now()}:")
            for change in changes:
                if create_log_file == True:
                    fsfile.append_text(log_filename, text=f"{change['abspath']} was {change['change']}")
                print(f"{change['abspath']} was {change['change']}")
        time.sleep(delay)