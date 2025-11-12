# FileSystem Module

## Overview

The `FileSystem` module is the central entry point for the **FileSystemPro** package. It provides a cross-platform abstraction layer for accessing essential file system paths and utilities, automatically detecting the underlying operating system (Linux, macOS, or Windows). This module eliminates the need for manual path construction or OS-specific conditionals in your code, enabling seamless file system interactions across platforms.

Key responsibilities include:

- **OS Detection and Configuration**: Identifies the platform and initializes environment-specific paths.
- **Standard Folder Paths**: Predefines common user directories like Home, Desktop, Documents, etc., using reliable sources (e.g., environment variables on Unix-like systems, Windows Registry on Windows).
- **Utility Constants**: Offers global helpers like the current working directory, path separator, and username for quick reference.
- **Platform Extensions**: Includes specialized paths unique to each OS (e.g., Templates on Linux, AppData on Windows).

Internally, it leverages the `__core__` submodule for foundational setup and the `console` submodule for enhanced output handling (e.g., ANSI color support). All constants are defined as module-level variables, making them directly accessible after import.

This module is designed for **programmers building cross-platform applications**, such as file managers, backup tools, or automation scripts. By using these constants, you ensure portability without sacrificing accuracy—paths are resolved at import time using authoritative OS APIs.

**Compatibility**:

- Python 3.10+ (tested up to 3.14).
- Platforms: Linux (including Linux2 variants), macOS (Darwin), Windows (win32/win64).
- Dependencies: Standard library only (`os`, `sys`, `getpass`, `winreg` on Windows).

## Features

- **Automatic Platform Detection**: Sets `PLATFORM_NAME` to "Linux", "macOS", or "Windows" based on `sys.platform`.
- **Core User Directories**: Immutable strings for Home (`user`), Desktop (`desktop`), Documents (`documents`), Downloads (`downloads`), Music (`music`), Pictures (`pictures`), Public (`public`), and Videos (`videos`).
- **OS-Specific Extensions**:
  - Linux: `linux_templates`.
  - macOS: `mac_applications`, `mac_movies` (note: `videos` aliases to Movies).
  - Windows: `windows_applicationData`, `windows_favorites`, `windows_localappdata`, `windows_temp`.
- **System Utilities**:
  - `CURRENT_LOCATION`: Path to the current working directory (`os.getcwd()`).
  - `OS_SEPARATOR`: OS-native path delimiter (`os.sep`, e.g., `/` on Unix, `\` on Windows).
  - `USER_NAME`: Capitalized username (`getpass.getuser()` with first letter uppercased).
- **Windows-Specific Reliability**: Uses `winreg` to query Shell Folders from the Registry for precise, user-configurable paths (e.g., if a user relocated their Documents folder).
- **Cross-Platform Portability**: Paths are constructed dynamically but cached as constants for performance.
- **Integration Ready**: Easily combines with other FileSystemPro modules like `file` (for file operations) or `directory` (for directory management).

## Installation and Setup

The `FileSystem` module is part of the **FileSystemPro** package. Install via pip:

```bash
pip install FileSystemPro
```

No additional configuration is required—the module auto-initializes on import.

## Usage

Import the module directly (recommended alias: `fs` for brevity). All constants are exposed at the module level—no classes or functions to instantiate.

```python
import filesystem as fs
```

### Accessing Constants

Constants are simple strings (except `PLATFORM_NAME`, which is a string enum-like value). Use them in path manipulations, file I/O, or logging.

#### Core Constants

| Constant          | Type   | Description | Example Value (Linux) | Example Value (Windows) |
|-------------------|--------|-------------|-----------------------|-------------------------|
| `PLATFORM_NAME`  | `str` | Detected OS name. | `"Linux"`            | `"Windows"`            |
| `user`           | `str` | User home directory. | `"/home/john"`       | `"C:\\Users\\John"`    |
| `desktop`        | `str` | Desktop folder path. | `"/home/john/Desktop"` | `"C:\\Users\\John\\Desktop"` |
| `documents`      | `str` | Documents folder path. | `"/home/john/Documents"` | `"C:\\Users\\John\\Documents"` |
| `downloads`      | `str` | Downloads folder path. | `"/home/john/Downloads"` | `"C:\\Users\\John\\Downloads"` |
| `music`          | `str` | Music folder path. | `"/home/john/Music"` | `"C:\\Users\\John\\Music"` |
| `pictures`       | `str` | Pictures folder path. | `"/home/john/Pictures"` | `"C:\\Users\\John\\Pictures"` |
| `public`         | `str` | Public shared folder path. | `"/home/john/Public"` | `"C:\\Users\\Public"` |
| `videos`         | `str` | Videos folder path. | `"/home/john/Videos"` | `"C:\\Users\\John\\Videos"` |

#### Utility Constants

| Constant          | Type   | Description | Example Value (Linux) | Example Value (Windows) |
|-------------------|--------|-------------|-----------------------|-------------------------|
| `CURRENT_LOCATION` | `str` | Current working directory. | `"/project/app"`     | `"C:\\project\\app"`   |
| `OS_SEPARATOR`   | `str` | Path separator. | `"/"`                | `"\\"`                 |
| `USER_NAME`      | `str` | Capitalized username. | `"John"`             | `"John"`               |

#### Platform-Specific Constants

These are always defined but only meaningful on their respective platforms. Use `if fs.PLATFORM_NAME == "Windows":` for conditional access.

| Constant                  | Type   | Platform | Description | Example Value |
|---------------------------|--------|----------|-------------|---------------|
| `linux_templates`        | `str` | Linux   | Templates folder. | `"/home/john/Templates"` |
| `mac_applications`       | `str` | macOS   | User Applications folder. | `"/Users/john/Applications"` |
| `mac_movies`             | `str` | macOS   | Movies folder (alias for `videos`). | `"/Users/john/Movies"` |
| `windows_applicationData`| `str` | Windows | Roaming AppData. | `"C:\\Users\\John\\AppData\\Roaming"` |
| `windows_favorites`      | `str` | Windows | Favorites folder. | `"C:\\Users\\John\\Favorites"` |
| `windows_localappdata`   | `str` | Windows | Local AppData. | `"C:\\Users\\John\\AppData\\Local"` |
| `windows_temp`           | `str` | Windows | Temporary files folder. | `"C:\\Users\\John\\AppData\\Local\\Temp"` |

**Notes**:

- Paths use absolute resolution and respect user customizations (e.g., via Windows Registry).
- On macOS, `videos` points to `Movies` for consistency with OS conventions—use `mac_movies` if you need the raw path.
- Constants are read-only; do not reassign them.

## Examples

### Basic Platform and Path Inspection

```python
import filesystem as fs

print(f"Running on: {fs.PLATFORM_NAME}")
print(f"Home directory: {fs.user}")
print(f"Path separator: '{fs.OS_SEPARATOR}'")
print(f"Current user: {fs.USER_NAME}")
print(f"Current working dir: {fs.CURRENT_LOCATION}")

# Output (example on Linux):
# Running on: Linux
# Home directory: /home/john
# Path separator: '/'
# Current user: John
# Current working dir: /project/app
```

### File Operations in Standard Folders

Integrate with other modules like `file` for real-world use:

```python
import filesystem as fs
from filesystem.file import get_files, create_file

# List files in Downloads
downloads_files = get_files(fs.downloads)
print(f"Files in Downloads: {downloads_files}")

# Create a file on Desktop
create_file(f"{fs.desktop}{fs.OS_SEPARATOR}example.txt", "Hello, FileSystemPro!")
print("File created on Desktop.")
```

### Platform-Conditional Paths

```python
import filesystem as fs

if fs.PLATFORM_NAME == "Windows":
    temp_dir = fs.windows_temp
    app_data = fs.windows_applicationData
    print(f"Temp: {temp_dir}")
    print(f"AppData: {app_data}")
elif fs.PLATFORM_NAME == "macOS":
    apps_dir = fs.mac_applications
    print(f"Apps: {apps_dir}")
elif fs.PLATFORM_NAME == "Linux":
    templates_dir = fs.linux_templates
    print(f"Templates: {templates_dir}")

# Cross-platform path joining (using OS_SEPARATOR)
safe_path = f"{fs.documents}{fs.OS_SEPARATOR}my_project{fs.OS_SEPARATOR}data.txt"
print(f"Safe path: {safe_path}")
```

### Advanced: Custom Path Building

```python
import filesystem as fs
from filesystem import directory

# Build a project structure in Documents
project_root = f"{fs.documents}{fs.OS_SEPARATOR}MyProject"
directory.create(f"{project_root}{fs.OS_SEPARATOR}src", create_subdirs=True)
directory.create(f"{project_root}{fs.OS_SEPARATOR}data", create_subdirs=True)
print(f"Project setup in: {project_root}")
```
> Learn more about Directory module in [About Directory Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/directory/README.md)

## Best Practices

- **Import Aliasing**: Always use `import filesystem as fs` to avoid namespace pollution.
- **Path Joining**: Prefer `os.path.join()` or f-strings with `OS_SEPARATOR` over hardcoding separators.
- **Error Handling**: While paths are resolved at import, wrap usage in try-except for runtime issues (e.g., permission errors).
- **Testing**: Mock `sys.platform` and environment vars in unit tests for cross-platform CI.
- **Performance**: Constants are evaluated once at import—safe for hot paths.
- **Security**: Avoid exposing sensitive paths (e.g., `windows_temp`) in logs; use them judiciously.

## Limitations

- Paths assume a standard user environment; corporate setups (e.g., roaming profiles) may vary.
- No support for mobile OS (iOS/Android) or embedded systems—extend via subclassing if needed.
- Windows Registry access requires admin privileges in rare cases; falls back to `USERPROFILE` if unavailable.

## Contributing

See the root [README.md](../README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE) for details.