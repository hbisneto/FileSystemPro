"""
# __core__

---

## Overview
The core module is the heart of the FileSystemPro library, 
providing essential functionalities that support and enhance the overall performance and usability 
of the library. It is designed to be robust and flexible, 
enabling seamless integration and configuration of various components, including the update checker.

## Features
- `Configuration Management:` Centralizes the configuration settings for the entire FileSystemPro library,
allowing for easy adjustments and fine-tuning of operational parameters.
- `Update Checker Integration:` Seamlessly incorporates the update checker functionality, 
ensuring that the library remains up-to-date with the latest features and security patches.
- `Internal Settings Control:` Offers a comprehensive interface for managing internal settings, 
which dictate the behavior of the library's various modules and functions.

## Detailed Functionality
The core module acts as a command center, 
orchestrating the library's internal mechanisms through a series of well-defined interfaces and protocols. 
It is responsible for initializing the library, setting up the environment, 
and providing a consistent experience across different platforms and configurations.

### Configuration Management
The module contains a configuration manager that stores all the necessary settings in a structured format. 
This manager is accessible throughout the library, 
allowing other modules to retrieve or update their configurations as needed. 
It supports various data types and structures, ensuring compatibility and flexibility.

### Update Checker Integration
The update checker is a critical component that the core module integrates tightly. 
It utilizes the core module's configuration management system to store and retrieve the 
current version information. This integration allows the update checker to function efficiently, 
checking for updates in the background without interrupting the user's workflow.

### Internal Settings Control
Through the core module, users can access and modify the library's internal settings, 
such as logging levels, performance options, and feature toggles. 
This control is crucial for tailoring the library to specific needs and environments, 
providing developers with the ability to optimize their usage of FileSystemPro.

## Usage
To utilize the core module, simply import it at the beginning of your script:

```python
from filesystem import __core__
```
"""

import requests
from filesystem import console as fsconsole

__version__ = "1.0.4.0"

def __checkupdates__(user, repo):
    """
    Checks for updates to the FileSystemPro package on GitHub.

    This function compares the current version of FileSystemPro, defined in the module,
    with the latest release version available on the specified user's GitHub repository.
    If a newer version is found, it notifies the user via the console.

    Parameters:
    user (str): The GitHub username of the repository owner.
    repo (str): The name of the repository.

    Returns:
    tuple: A tuple containing the current version and the latest version tag if an update is available.
           Returns (None, None) if there's an exception during the request.
    """
    ### TAG PATTERN: v1.2.3.4
    current_version_string = ''.join(filter(str.isdigit, __version__))
    current_version = int(current_version_string)
    update_version = 0

    ### Check updates online using 'requests'
    url = f'https://api.github.com/repos/{user}/{repo}/releases'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as err:
        return None, None
    releases = response.json()
    
    for release in releases:
        if update_version == 0:
            tag_name = f'{release["tag_name"]}'
            update_version_string = ''.join(filter(str.isdigit, tag_name))
            update_version = int(update_version_string)

    if current_version < update_version:
        print(f"[{fsconsole.foreground.BLUE}Notice{fsconsole.style.RESET_ALL}]: A new release of FileSystemPro is available: {fsconsole.foreground.RED}v{__version__}{fsconsole.style.RESET_ALL} -> {fsconsole.foreground.GREEN}{tag_name}{fsconsole.style.RESET_ALL}")
        print(f"[{fsconsole.foreground.BLUE}Notice{fsconsole.style.RESET_ALL}]: To update, run: {fsconsole.foreground.GREEN}pip install --upgrade filesystempro{fsconsole.style.RESET_ALL}")