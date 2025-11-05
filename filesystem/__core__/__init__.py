# -*- coding: utf-8 -*-
#
# filesystem/__core__/__init__.py
# FileSystemPro
#
# Created by Heitor Bisneto on 12/11/2025.
# Copyright © 2023–2025 hbisneto. All rights reserved.
#
# This file is part of FileSystemPro.
# FileSystemPro is free software: you can redistribute it and/or modify
# it under the terms of the MIT License. See LICENSE for more details.
#

"""
# __Core__

---

## Overview
This module provides configuration management, logging setup, performance tuning, feature toggles, and automated update checking for the FileSystemPro package. It initializes a global config from defaults, JSON files, .env files, and environment variables, with support for saving changes and async operations to avoid blocking. Update checks query GitHub releases asynchronously, notifying via console or callbacks if newer versions are available.

### Environment Configuration (.env File)
The module supports configuration via a `.env` file placed in the current working directory or the user's home directory. Below is an example `.env` file that developers can use as a template to customize settings:

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

These values override defaults and can be combined with the JSON config file for layered configuration.

## Features
- **Config Loading/Saving:** Merge defaults with .env, env vars, and JSON file; persist changes to disk.
- **Logging Management:** Dynamically set levels (e.g., DEBUG, INFO) with immediate effect.
- **Performance Settings:** Adjust cache sizes for optimization.
- **Feature Toggles:** Enable/disable specific features like experimental ones.
- **Update Detection:** Async GitHub API polling for releases, with version comparison and user notifications (disable via config).

## Usage
To use these functions, import the module directly:

```python
from filesystem import __core__ as core
```

### Examples:

- Get current configuration:

```python
config = core.get_config()
print(config)  # e.g., {'update_checker_enabled': True, 'logging_level': 'INFO', ...}
```

- Set logging level:

```python
core.set_logging_level('DEBUG')
# Now logs at DEBUG level
```

- Toggle a feature:

```python
core.toggle_feature('experimental_features', True)
```

- Check for updates asynchronously:

```python
core.check_updates_async(user='hbisneto', repo='filesystempro', callback=print)
```

- Save custom config changes:

```python
custom_config = {'performance_cache_size': 2048}
core.save_config(custom_config)
```
"""

import requests
import json
import os
import threading
import logging
from pathlib import Path
from filesystem.console import console

# major.minor.patch.build
__version__ = "3.0.0.0"
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

__config__ = None

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
    global __config__  
    if __config__ is not None:  
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
      
    __config__ = initial_config  
    
    if not CONFIG_FILE.exists():  
        try:
            with open(CONFIG_FILE, 'w') as f:  
                json.dump(__config__, f, indent=4)  
            logging.debug(f"Created config file: {CONFIG_FILE}")  
        except IOError as e:  
            logging.warning(f"Failed to create config file: {e}")

    logging.basicConfig(level=getattr(logging, __config__['logging_level']))

def get_config():
    """Get the current configuration dict."""
    if __config__ is None:
        init_config()
    return __config__.copy()

def save_config(config_dict):
    """Save configuration to file (overrides .env initial values)."""
    if __config__ is None:
        init_config()
    __config__.update(config_dict)
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(__config__, f, indent=4)
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
