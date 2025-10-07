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
allowing for easy adjustments and fine-tuning of operational parameters. Supports persistent storage via JSON and overrides via .env.
- `Update Checker Integration:` Seamlessly incorporates the update checker functionality, 
ensuring that the library remains up-to-date with the latest features and security patches. Now optional and asynchronous.
- `Internal Settings Control:` Offers a comprehensive interface for managing internal settings, 
which dictate the behavior of the library's various modules and functions, including logging and feature toggles.

## Detailed Functionality
The core module acts as a command center, 
orchestrating the library's internal mechanisms through a series of well-defined interfaces and protocols. 
It is responsible for initializing the library, setting up the environment, 
and providing a consistent experience across different platforms and configurations.

### Configuration Management
The module contains a configuration manager that stores all the necessary settings in a structured format (JSON). 
This manager is accessible throughout the library, 
allowing other modules to retrieve or update their configurations as needed. 
It supports various data types and structures, ensuring compatibility and flexibility.
Supports defaults, .env overrides, and persistence to `.config/config.json`.

### Environment Configuration (.env Support)
For user autonomy, create a `.env` file in your project root (current directory) or home directory. The library will load it automatically during `init_config()`. 
Use prefix `FILESYSTEMPRO_` for vars. Changes here set initial values, which can be overridden by JSON or API calls.

**Template .env (copy to .env and customize):**

```
# Update Checker
# Controls whether the update checker runs automatically (true/false, 1/0, yes/no)
FILESYSTEMPRO_UPDATE_CHECKER_ENABLED=true

# Logging
# logging level (DEBUG, INFO, WARNING, ERROR)
FILESYSTEMPRO_LOGGING_LEVEL=DEBUG

# Performance
# Size of the cache for performance optimizations (integer number)
FILESYSTEMPRO_PERFORMANCE_CACHE_SIZE=1024

# Feature Toggles (JSON-like strings)
# Feature toggles (use a valid JSON string)
FILESYSTEMPRO_FEATURE_TOGGLES = {"experimental_features": true, "advanced_logging": false}
```

Note: For complex values like `feature_toggles`, use JSON strings. The library parses them automatically. Supports env vars as fallback.

### Update Checker Integration
The update checker is a critical component that the core module integrates tightly. 
It utilizes the core module's configuration management system to store and retrieve the 
current version information. This integration allows the update checker to function efficiently, 
checking for updates in the background without interrupting the user's workflow. 
Can be disabled via config or .env.

### Internal Settings Control
Through the core module, users can access and modify the library's internal settings, 
such as logging levels, performance options, and feature toggles. 
This control is crucial for tailoring the library to specific needs and environments, 
providing developers with the ability to optimize their usage of FileSystemPro.

## Usage
To utilize the core module, simply import it at the beginning of your script:

```python
from filesystem import __core__
__core__.init_config()  # Loads .env and JSON
__core__.check_updates_async()  # Optional async update check
```

For configuration via .env: See template above.

For runtime changes:
```python
config = __core__.get_config()
config['logging_level'] = 'DEBUG'
__core__.save_config(config)
```
"""

import requests
import json
import os
import threading
import logging
from pathlib import Path
from filesystem import console as fsconsole

# major.minor.patch.build
__version__ = "2.0.0.0"
"""Version of the FileSystemPro package."""

MODULE_DIR = Path(__file__).parent
CONFIG_DIR = MODULE_DIR / ".config"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "update_checker_enabled": True,
    "logging_level": "INFO",
    "performance_cache_size": 1024,
    "feature_toggles": {
        "experimental_features": False
    }
}

_config = None

def __parse_env_file__():
    """Simple .env parser using stdlib only. Returns dict of key-value pairs."""
    env_dict = {}
    env_paths = [Path.cwd() / ".env", Path.home() / ".env"]
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                env_dict[key.strip()] = value.strip()
            except IOError as e:
                logging.warning(f"Failed to parse {env_path}: {e}")
            break
    return env_dict

def init_config():  
    """Initialize the configuration manager, loading from env vars, defaults, or file."""  
    global _config  
    if _config is not None:  
        return  
  
    initial_config = DEFAULT_CONFIG.copy()

    CONFIG_DIR.mkdir(exist_ok=True)  
    if CONFIG_FILE.exists():  
        try:  
            with open(CONFIG_FILE, 'r') as f:  
                loaded = json.load(f)  
                initial_config = {**initial_config, **loaded}  
        except (json.JSONDecodeError, IOError) as e:  
            logging.warning(f"Failed to load config: {e}. Using defaults.")
    env_vars = __parse_env_file__()
      
    update_checker_str = env_vars.get('FILESYSTEMPRO_UPDATE_CHECKER_ENABLED') or os.getenv('FILESYSTEMPRO_UPDATE_CHECKER_ENABLED')  
    if update_checker_str is not None:  
        initial_config['update_checker_enabled'] = update_checker_str.lower() in ('true', '1', 'yes')  
      
    logging_level = env_vars.get('FILESYSTEMPRO_LOGGING_LEVEL') or os.getenv('FILESYSTEMPRO_LOGGING_LEVEL')  
    if logging_level:  
        initial_config['logging_level'] = logging_level.upper()  
      
    cache_size_str = env_vars.get('FILESYSTEMPRO_PERFORMANCE_CACHE_SIZE') or os.getenv('FILESYSTEMPRO_PERFORMANCE_CACHE_SIZE')  
    if cache_size_str:  
        try:  
            initial_config['performance_cache_size'] = int(cache_size_str)  
        except ValueError:  
            logging.warning("Invalid int in FILESYSTEMPRO_PERFORMANCE_CACHE_SIZE.")  
      
    toggles_str = env_vars.get('FILESYSTEMPRO_FEATURE_TOGGLES') or os.getenv('FILESYSTEMPRO_FEATURE_TOGGLES')  
    if toggles_str:  
        try:  
            initial_config['feature_toggles'] = json.loads(toggles_str)  
        except json.JSONDecodeError:  
            logging.warning("Invalid JSON in FILESYSTEMPRO_FEATURE_TOGGLES.")  
      
    _config = initial_config  
    
    if not CONFIG_FILE.exists():  
        try:
            with open(CONFIG_FILE, 'w') as f:  
                json.dump(_config, f, indent=4)  
            logging.debug(f"Created config file: {CONFIG_FILE}")  
        except IOError as e:  
            logging.warning(f"Failed to create config file: {e}")

    logging.basicConfig(level=getattr(logging, _config['logging_level']))

def get_config():
    """Get the current configuration dict."""
    if _config is None:
        init_config()
    return _config.copy()

def save_config(config_dict):
    """Save configuration to file (overrides .env initial values)."""
    if _config is None:
        init_config()
    _config.update(config_dict)
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(_config, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to save config: {e}")

def set_logging_level(level):
    """Set logging level (e.g., 'DEBUG', 'INFO', 'WARNING')."""
    config = get_config()
    config['logging_level'] = level.upper()
    save_config(config)
    logging.getLogger().setLevel(getattr(logging, level.upper()))

def set_performance_cache_size(size):
    """Set cache size for performance tuning."""
    config = get_config()
    config['performance_cache_size'] = int(size)
    save_config(config)

def toggle_feature(feature_name, enabled):
    """Toggle a feature (e.g., 'experimental_features')."""
    config = get_config()
    if feature_name in config['feature_toggles']:
        config['feature_toggles'][feature_name] = bool(enabled)
        save_config(config)
    else:
        logging.warning(f"Unknown feature: {feature_name}")

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
    if not get_config().get('update_checker_enabled', True):
        return __version__, __version__

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
            msg = f"[{fsconsole.foreground.BLUE}Notice{fsconsole.style.RESET_ALL}]: New release available: {fsconsole.foreground.RED}v{__version__}{fsconsole.style.RESET_ALL} -> {fsconsole.foreground.GREEN}v{latest_tag}{fsconsole.style.RESET_ALL}"
            update_msg = f"[{fsconsole.foreground.BLUE}Notice{fsconsole.style.RESET_ALL}]: Update with: {fsconsole.foreground.GREEN}pip install --upgrade filesystempro{fsconsole.style.RESET_ALL}"
            if callback:
                callback(msg + "\n" + update_msg)
            else:
                print(msg)
                print(update_msg)
            return __version__, latest_tag
        return __version__, latest_tag
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logging.error(f"Update check failed: {e}")
        return None, None

def check_updates_async(user, repo, callback=None):
    """Asynchronous wrapper for __checkupdates__ to avoid blocking."""
    def _async_check():
        __checkupdates__(user, repo, callback)
    
    thread = threading.Thread(target=_async_check, daemon=True)
    thread.start()

# Initialize config on import
init_config()
# Auto-check for updates asynchronously (can be disabled via config or .env)
check_updates_async(user='hbisneto', repo='filesystempro')
