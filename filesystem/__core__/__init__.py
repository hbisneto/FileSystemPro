"""
# __core__

---

## Overview
The `__core__` module is the operational heart of the **FileSystemPro** library, responsible for managing the current version, checking for updates on GitHub, and performing this check asynchronously and non-blockingly. It ensures users are promptly notified of new releases upon import, keeping the library up-to-date with the latest features and security patches.

## Features
- **Automatic update check** on module import.
- **Simplified version comparison** using numeric digit extraction.
- **Asynchronous execution** via background thread to avoid blocking.
- **Colorful console notifications** with clear update instructions.
- **Optional callback** for custom update handling.

## Detailed Functionality

### Update Checking
The `__checkupdates__` function makes a request to the GitHub API to fetch the `latest` release tag.  
It compares the current version (`__version__ = "2.1.0.0"`) with the latest one by extracting only numeric digits from both strings, enabling reliable integer-based comparison even with `v` prefixes or non-numeric suffixes.

### Asynchronous Execution
The `check_updates_async` function wraps the check in a **daemon thread**, ensuring the update verification runs in the background without interrupting the main program flow.

### Auto-Check on Import
At the end of the module, the following is executed automatically:

```python
check_updates_async(user='hbisneto', repo='filesystempro')
```
"""

import requests
import threading
from filesystem.console import console

__version__ = "2.1.0.0"
"""Version of the FileSystemPro package."""

def __checkupdates__(user, repo, callback=None):
    """
    Checks for updates to the FileSystemPro package on GitHub (synchronous version).

    Uses simple digit extraction for version comparison.

    Parameters:
    user (str): The GitHub username.
    repo (str): The repository name.
    callback (callable): Optional callback to notify on update (e.g., print).

    Returns:
    tuple: (current_version_str, latest_version_str) or (None, None) on error.
    """

    url = f'https://api.github.com/repos/{user}/{repo}/releases/latest'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        release_data = response.json()
        latest_tag = release_data['tag_name'].lstrip('v')
        
        current_version_string = ''.join(filter(str.isdigit, __version__))
        current_version = int(current_version_string)
        update_version_string = ''.join(filter(str.isdigit, latest_tag))
        update_version = int(update_version_string)

        if current_version < update_version:
            msg = f'[{console.blue()("Notice")}]: New release available: {console.red()(f"v{__version__}")} -> {console.green()(f"v{latest_tag}")}'
            update_msg = f'[{console.blue()("Notice")}]: To update, run: {console.green()(f"pip install --upgrade filesystempro")}'
            if callback:
                callback(msg + "\n" + update_msg)
            else:
                print(msg)
                print(update_msg)
            return __version__, latest_tag
        return __version__, latest_tag
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        return None, None

def check_updates_async(user, repo, callback=None):
    """Asynchronous wrapper for __checkupdates__ to avoid blocking."""
    def _async_check():
        __checkupdates__(user, repo, callback)
    
    thread = threading.Thread(target=_async_check, daemon=True)
    thread.start()

check_updates_async(user='hbisneto', repo='filesystempro')