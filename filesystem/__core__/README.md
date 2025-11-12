# __Core__ Module

## Overview

The `__core__` module is the foundational backbone of the **FileSystemPro** package, responsible for managing runtime configuration, logging, performance optimizations, feature toggles, and automated update notifications. It provides a centralized, extensible system for customizing package behavior without code changes, using a layered approach: defaults → JSON config file → .env file → environment variables. This ensures flexibility for developers, from quick prototyping (e.g., enabling DEBUG logging) to production deployments (e.g., disabling update checks).

Key design principles:

- **Non-Blocking Operations**: Async update checks prevent I/O delays during imports.
- **Persistence**: Changes to config are saved to a JSON file (`.config/config.json`) in the module directory, surviving restarts.
- **Stdlib + Minimal Deps**: Relies on standard library for .env parsing and threading; uses `requests` only for updates.
- **Global State Management**: Uses a singleton-like `__config__` dict, initialized lazily on first access.

This module is ideal for **programmers integrating FileSystemPro into larger applications**, such as CLI tools, GUIs, or scripts requiring tunable logging or feature flags. It auto-initializes on import, so no explicit setup is needed unless customizing defaults.

**Compatibility**:

- Python 3.10+ (uses `pathlib`, `threading`, `logging`).
- Platforms: Cross-platform (file paths via `Path`).
- Dependencies: `requests` (for updates; install via `pip install requests` if needed).

## Features

- **Configuration Management**: Load/merge from multiple sources (defaults, JSON, .env, env vars); save overrides dynamically.
- **Logging Setup**: Dynamic level adjustment (DEBUG, INFO, WARNING, ERROR) with immediate application to the root logger.
- **Performance Tuning**: Adjustable cache sizes for downstream modules (e.g., file watchers).
- **Feature Toggles**: JSON-based flags for enabling/disabling experimental or optional behaviors (e.g., advanced logging).
- **Update Checker**: Asynchronous GitHub API integration to detect new releases; notifies via console or callback with upgrade instructions. Compares versions by extracting numeric parts (e.g., "3.0.0.0" vs. "3.1.0.0").
- **Environment Support**: Parses `.env` files from CWD or user home; supports boolean/int/JSON coercion.
- **Error Resilience**: Graceful fallbacks (e.g., warnings on parse errors) without crashing imports.

## Configuration Sources

Configurations are layered for overrides (later sources take precedence):

1. **Defaults**: Hardcoded in `DEFAULT_CONFIG`.
2. **JSON File**: `filesystem/.config/config.json` (auto-created if missing).
3. **.env File**: `.env` in CWD or `~/.env` (key-value pairs like `FILESYSTEMPRO_LOGGING_LEVEL=DEBUG`).
4. **Environment Variables**: `os.getenv()` (e.g., `FILESYSTEMPRO_UPDATE_CHECKER_ENABLED=false`).

### Default Configuration
| Key                       | Type/Value                  | Description | Default Value |
|---------------------------|-----------------------------|-------------|---------------|
| `update_checker_enabled` | `bool`                     | Enables async GitHub update checks on import. | `True` |
| `logging_level`          | `str` (DEBUG/INFO/WARNING/ERROR) | Sets root logger level. | `"INFO"` |
| `performance_cache_size` | `int`                      | Max cache entries for performance-sensitive ops (e.g., path resolution). | `1024` |
| `feature_toggles`        | `dict`                     | Nested flags (e.g., `{"experimental_features": False}`). | `{"experimental_features": False}` |

### .env File Template
Place this in your project's root or home directory to override defaults:

```
# Update Checker
FILESYSTEMPRO_UPDATE_CHECKER_ENABLED=false

# Logging
FILESYSTEMPRO_LOGGING_LEVEL=DEBUG

# Performance
FILESYSTEMPRO_PERFORMANCE_CACHE_SIZE=2048

# Feature Toggles (valid JSON string)
FILESYSTEMPRO_FEATURE_TOGGLES={"experimental_features": true, "advanced_logging": true}
```

**Notes**:

- Booleans: Accept "true"/"1"/"yes" (case-insensitive).
- JSON for toggles must be valid; errors log warnings and skip.
- Changes via functions (e.g., `set_logging_level()`) persist to JSON but won't override active .env/env vars on reload—restart for full reset.

## Usage

Import the module as `core` (or directly). It auto-initializes config and starts async update check (if enabled).

```python
from filesystem import __core__ as core
```

All functions are module-level; no classes to instantiate. Use `get_config()` to inspect state.

### Core Functions

#### `init_config() → None`
- **Description**: Lazy-initializes the global `__config__` dict, merging sources and creating/saving the JSON file if needed. Called automatically on first access.
- **Parameters**: None.
- **Returns**: None.
- **Raises**: `logging.warning` on file/JSON errors (no exceptions propagated).
- **Implementation Notes**: Ensures `CONFIG_DIR` exists; parses .env with stdlib only.

#### `get_config() → dict`
- **Description**: Returns a shallow copy of the current config for safe inspection/modification.
- **Parameters**: None.
- **Returns**: `dict` (copy of `__config__`).
- **Usage Tip**: Always use this before mutating—avoids race conditions in multi-threaded apps.

#### `save_config(config_dict: dict) → None`
- **Description**: Merges `config_dict` into `__config__` and persists to JSON. Useful for batch updates.
- **Parameters**:
  - `config_dict` (`dict`): Key-value pairs to update (e.g., `{"logging_level": "DEBUG"}`).
- **Returns**: None.
- **Raises**: `logging.error` on write failures.
- **Example**: `save_config({"performance_cache_size": 4096})`

#### `set_logging_level(level: str) → None`
- **Description**: Updates config and applies new level to `logging.root` immediately.
- **Parameters**:
  - `level` (`str`): "DEBUG", "INFO", "WARNING", or "ERROR".
- **Returns**: None.
- **Raises**: `AttributeError` if invalid level (use `getattr(logging, level.upper())` internally).
- **Notes**: Propagates to all loggers; combine with `console` module for colored output.

#### `set_performance_cache_size(size: int | str) → None`
- **Description**: Sets cache size in config (coerces str to int).
- **Parameters**:
  - `size` (`int` or `str`): Positive integer (e.g., 2048).
- **Returns**: None.
- **Raises**: `ValueError` on invalid int (logs warning).
- **Usage**: Tune for memory vs. speed; higher values for large file ops.

#### `toggle_feature(feature_name: str, enabled: bool) → None`
- **Description**: Enables/disables a feature flag in `feature_toggles`.
- **Parameters**:
  - `feature_name` (`str`): Key (e.g., "experimental_features").
  - `enabled` (`bool`): True to enable.
- **Returns**: None.
- **Raises**: `logging.warning` if feature unknown (ignores).
- **Notes**: Other modules (e.g., `watcher`) can query via `get_config()["feature_toggles"]`.

#### `check_updates_async(user: str, repo: str, callback: callable = None) → None`
- **Description**: Spawns a daemon thread for non-blocking GitHub release check. Notifies via callback or print.
- **Parameters**:
  - `user` (`str`): GitHub username (default: "hbisneto").
  - `repo` (`str`): Repo name (default: "filesystempro").
  - `callback` (`callable`): Optional function (e.g., `lambda msg: print(msg)`).
- **Returns**: None (async; returns versions via internal `__checkupdates__`).
- **Raises**: Handled internally (`logging.error` on network/JSON errors).
- **Version Logic**: Strips non-digits (e.g., "v3.1.0" → 310); alerts if newer.
- **Auto-Call**: Runs on import if enabled—customize via config.

**Internal Helpers** (not for direct use):
- `__parse_env_file__() → dict`: Parses .env (private).
- `__checkupdates__(...) → tuple[str, str]`: Sync version of update check (private).

## Examples

### Basic Configuration Inspection and Logging
```python
from filesystem import __core__ as core

# Auto-init on import
config = core.get_config()
print(config)
# Output: {'update_checker_enabled': True, 'logging_level': 'INFO', 'performance_cache_size': 1024, 'feature_toggles': {'experimental_features': False}}

# Switch to DEBUG logging
core.set_logging_level('DEBUG')
import logging
logging.debug("This now appears!")  # From filesystem.console import console for colors
```

### Feature Toggling and Performance Tuning
```python
from filesystem import __core__ as core

# Enable experimental features
core.toggle_feature('experimental_features', True)

# Increase cache for heavy ops
core.set_performance_cache_size(2048)

# Save and verify
core.save_config({})  # Flushes changes
updated_config = core.get_config()
print(updated_config['feature_toggles'])  # {'experimental_features': True}
print(updated_config['performance_cache_size'])  # 2048
```

### Custom Update Check
```python
from filesystem import __core__ as core

def on_update(msg):
    print(f"Custom alert: {msg}")

# Manual async check (e.g., on app startup)
core.check_updates_async(user='hbisneto', repo='filesystempro', callback=on_update)

# In a loop (e.g., every hour)
import time
while True:
    core.check_updates_async(callback=on_update)
    time.sleep(3600)
```

### Integrating with Other Modules
```python
from filesystem import __core__ as core
from filesystem.file import get_files  # Hypothetical; cache uses performance_size

# Tune for file ops
core.set_performance_cache_size(4096)

# Use toggles in logic
config = core.get_config()
if config['feature_toggles'].get('experimental_features', False):
    files = get_files('/path', use_experimental=True)  # Custom flag
else:
    files = get_files('/path')
```

### .env Override Example
Create `.env` in your project:
```
FILESYSTEMPRO_UPDATE_CHECKER_ENABLED=false
FILESYSTEMPRO_FEATURE_TOGGLES={"advanced_logging": true}
```
Then import:
```python
from filesystem import __core__ as core
print(core.get_config()['update_checker_enabled'])  # False
```

## Best Practices

- **Import Early**: Call `init_config()` in app entrypoint for consistent state.
- **Thread Safety**: Config updates are not atomic—use locks for high-concurrency (e.g., `threading.Lock` around `save_config`).
- **Validation**: Wrap `get_config()` in your code with type checks (e.g., `isinstance(config['performance_cache_size'], int)`).
- **Disabling Updates**: Set `update_checker_enabled=False` in production to avoid network calls.
- **Testing**: Mock `requests.get` and `Path.home()` for unit tests; verify JSON persistence.
- **Extensibility**: Subclass or monkey-patch `DEFAULT_CONFIG` for forks.

## Limitations

- **Version Comparison**: Numeric-only (ignores alphas like "3.0.0a"); upgrade to semantic versioning lib if needed.
- **.env Parsing**: Basic (no quotes/escapes); use `python-dotenv` for complex files.
- **No Encryption**: Config file is plain JSON—avoid secrets; use env vars for sensitive data.
- **GitHub Dependency**: Update checks fail offline; no proxy support out-of-box.
- **Global Logger**: Affects entire app—use named loggers (`logging.getLogger(__name__)`) for isolation.

## Contributing

See the root [README.md](https://github.com/hbisneto/FileSystemPro/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE) for details.