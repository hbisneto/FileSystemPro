# Directory Module

## Overview

The `directory` module in **FileSystemPro** delivers a robust, cross-platform toolkit for managing directories, encompassing path construction, creation/deletion, recursive enumeration, size computation, timestamp manipulation (creation/access/write times in local and UTC formats), symbolic links, temporary directories, movement/renaming, and visual tree generation. It builds on standard library modules like `os`, `shutil`, `glob`, and `tempfile`, while integrating with the `wrapper` module for rich metadata returns (e.g., absolute paths, sizes as formatted strings, timestamps). A global `current_directory` tracks the working directory, synced with `os.chdir()` via `set_current_directory()`.

This module is designed for **programmers crafting file explorers, build tools, or automation scripts**, where precise directory handling is crucial. Functions emphasize safety (e.g., existence checks, permission errors), efficiency (iterators for large dirs), and portability (Unix creation time approximations via change time). Enumeration supports glob patterns and recursion options ("TopDirectoryOnly" or "AllDirectories"). Tree views mimic the `tree` CLI, auto-ignoring common dev artifacts like `.git`.

**Key Design Principles**:

- **Immutable Globals**: `current_directory` mirrors `os.getcwd()` post-changes.
- **Timestamp Handling**: Local via `fromtimestamp()`; UTC via `utcfromtimestamp()`. Setting approximates via `utime()` (access/modification times).
- **Path Safety**: Functions validate inputs (e.g., absolute paths in `combine()`); use `os.path` norms.
- **Overwrite Controls**: Explicit flags for moves/renames to prevent data loss.
- **Recursion Awareness**: Walks skip ignored dirs in trees; enumeration yields paths directly.

**Compatibility**:

- Python 3.10+ (uses `os.scandir()`, `datetime`).
- Platforms: Cross-platform (symlinks Unix-preferred; timestamps Unix-limited).
- Dependencies: Standard library only.

## Features

- **Path Manipulation**: Join/combine paths (with absolute checks), get parent/name, resolve symlinks.
- **Creation & Linking**: Create dirs (recursive), temp subdirs, symbolic links.
- **Deletion & Movement**: Delete (recursive), move (root/contents, overwrite), rename.
- **Enumeration**: List files/dirs/entries with glob patterns and recursion (iterators or lists).
- **Existence & Metrics**: Check existence, compute recursive sizes (bytes or "2.5 GB").
- **Timestamps**: Get/set creation/access/write times (local/UTC, datetime or str input; str formats: "%Y-%m-%d %H:%M:%S" or with microseconds).
- **Visualization**: Generate tree strings, ignoring `.git`, `__pycache__`, etc.
- **Working Directory**: Get/set current dir with global tracking.
- **Metadata Integration**: Returns `wrapper.get_object()` dicts where useful (e.g., `{'abspath': '/path', 'size': '0.0 bytes', 'created': '2025-11-10 19:48:00'}`).

## Installation and Setup

Part of **FileSystemPro**—install via:

```bash
pip install filesystempro
```

No config needed; import and use. For timestamps, ensure `datetime` awareness (local TZ via system).

## Usage

Import the module:

```python
from filesystem import directory as dir  # Alias for brevity
```

Functions are module-level; paths should be absolute for reliability (pair with `filesystem` constants like `fs.documents`).

### Function Reference

Functions are grouped by category. All raise `FileNotFoundError`/`PermissionError` where applicable unless noted.

#### Path Operations

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `combine(*args, paths=[])` | `*args`: Paths (first absolute).<br>`paths` (list): Alt list (priority). | `str`: Joined path. | `ValueError` (non-absolute first). |
| `join(path1='', path2='', path3='', path4='', paths=[])` | Individual paths + list (filters empties). | `str`: Concatenated path (no double sep). | None. |
| `get_parent(path)` | `path` (str). | `str`: Parent dir. | None. |
| `get_parent_name(path)` | `path` (str). | `str`: Parent name. | None. |
| `get_name(path)` | `path` (str; assumes dir if no ext). | `str`: Dir/file name. | None. |
| `resolve_link_target(path, return_final_target=False)` | `path` (str).<br>`return_final_target` (bool). | `str`: Link target. | `ValueError` (not link), `OSError`. |

#### Creation & Deletion

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `create(path, create_subdirs=True)` | `path` (str).<br>`create_subdirs` (bool). | `dict`: Metadata. | `FileExistsError` (if False & exists), `PermissionError`. |
| `create_temp_subdirectory(prefix="")` | `prefix` (str). | `str`: Temp path. | None (system temp). |
| `create_symbolic_link(path_target, path_link)` | Targets (str). | `dict`: Link metadata. | `FileNotFoundError`, `ValueError` (not dir), `FileExistsError`. |
| `delete(path, recursive=False)` | `path` (str).<br>`recursive` (bool). | None. | `FileNotFoundError`, `OSError` (non-empty). |
| `move(source, destination, move_root=True, overwrite=False)` | Paths (str), flags (bool). | `dict`: Dest metadata. | `FileNotFoundError`, `FileExistsError` (if not overwrite), `OSError`. |
| `rename(old_path, new_path)` | Paths (str). | `bool`: Success. | `FileExistsError`. |

#### Enumeration

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `enumerate_directories(path, search_pattern="*", search_option="TopDirectoryOnly")` | `path` (str), pattern (str), option (str). | Iterator[str]: Dir paths. | `FileNotFoundError`, `PermissionError`. |
| `enumerate_files(path, search_pattern="*", search_option="TopDirectoryOnly")` | As above. | Iterator[str]: File paths. | As above. |
| `get_directories(path, search_pattern="*", search_option="TopDirectoryOnly")` | As above. | `list[str]`: Dir paths. | As above. |
| `get_files(path, search_pattern="*", search_option="TopDirectoryOnly")` | As above. | `list[str]`: File paths. | As above. |
| `get_filesystem_entries(path, search_pattern="*", search_option="TopDirectoryOnly")` | As above. | `list[str]`: All entries. | As above. |

#### Metrics & Existence

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `exists(path)` | `path` (str). | `bool`: Exists. | None. |
| `get_size(directory_path, show_unit=False)` | `path` (str), `show_unit` (bool). | `int` or `str`: Size (bytes or formatted). | `FileNotFoundError`, `PermissionError`. |
| `get_tree(directory, indent="", prefix="├── ")` | `directory` (str), indents (str). | `list[str]`: Tree lines. | `PermissionError` (partial). |

#### Timestamps (Get)

All return `datetime`; UTC variants use `utcfromtimestamp()`. Unix: creation ≈ change time.

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `get_creation_time(path)` / `get_creation_time_utc(path)` | `path` (str). | `datetime`: Time. | `FileNotFoundError`, `PermissionError`. |
| `get_last_access_time(path)` / `get_last_access_time_utc(path)` | As above. | `datetime`: Access time. | As above. |
| `get_last_write_time(path)` / `get_last_write_time_utc(path)` | As above. | `datetime`: Write time. | As above. |

#### Timestamps (Set)

Accept `datetime` or str ("%Y-%m-%d %H:%M:%S" or with ".%f"); approx via `utime()`.

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `set_creation_time(path, creation_time)` / `set_creation_time_utc(path, creation_time_utc)` | `path` (str), time (datetime/str). | None. | `FileNotFoundError`, `ValueError` (parse), `PermissionError`. |
| `set_last_access_time(path, last_access_time)` / `set_last_access_time_utc(...)` | As above. | None. | As above. |
| `set_last_write_time(path, last_write_time)` / `set_last_write_time_utc(...)` | As above. | None. | As above. |

#### Working Directory

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `get_current_directory()` | None. | `str`: Current dir. | None. |
| `set_current_directory(path)` | `path` (str). | None. | `FileNotFoundError`, `PermissionError`. |

## Examples

### Path Operations and Creation

```python
from filesystem import directory as dir
import filesystem as fs

# Join paths safely
joined = dir.join(fs.documents, "project", "data")
print(joined)  # e.g., "/home/user/Documents/project/data"

# Create dir with subdirs
result = dir.create(f"{fs.desktop}/new_project/subdir", create_subdirs=True)
print(f"Created: {result['abspath']} (Size: {result['size']})")

# Create symlink
dir.create_symbolic_link(f"{fs.desktop}/new_project", f"{fs.documents}/project_link")
```

### Enumeration and Size

```python
from filesystem import directory as dir

# List .py files recursively
py_files = dir.get_files("/path/to/project", "*.py", "AllDirectories")
for file_path in py_files:
    print(file_path)

# Iterator for large dirs
for file_path in dir.enumerate_files("/path/to/large_dir", search_option="AllDirectories"):
    print(f"File: {file_path}")

# Size with units
size_bytes = dir.get_size("/path/to/project")
size_formatted = dir.get_size("/path/to/project", show_unit=True)
print(f"Size: {size_bytes} bytes or {size_formatted}")
```

### Movement and Timestamps

```python
from filesystem import directory as dir
from datetime import datetime

# Move dir contents (overwrite)
move_result = dir.move("/source/dir", "/dest/dir", move_root=False, overwrite=True)
print(f"Moved to: {move_result['abspath']}")

# Rename
success = dir.rename("/old/dir", "/new/dir")
print(f"Renamed: {success}")

# Get/set timestamps (str input)
write_time = dir.get_last_write_time("/path/to/dir")
print(write_time)  # datetime(2025, 11, 10, 19, 48, 0)

dir.set_last_write_time("/path/to/dir", "2023-01-01 12:00:00")
utc_time = dir.get_last_write_time_utc("/path/to/dir")
print(utc_time)
```

### Tree Visualization

```python
from filesystem import directory as dir

tree_lines = dir.get_tree("/path/to/project")
for line in tree_lines:
    print(line)
# Sample output:
# ├── README.md
# ├── src
# │   └── main.py
# └── tests
#     └── test.py
```

### Current Directory Management

```python
from filesystem import directory as dir

old_cwd = dir.get_current_directory()
print(f"Current: {old_cwd}")

dir.set_current_directory("/path/to/project")
print(f"New: {dir.get_current_directory()}")  # /path/to/project

# Restore
dir.set_current_directory(old_cwd)
```

## Best Practices

- **Absolute Paths**: Use `filesystem` constants (e.g., `fs.user`) as bases; validate with `exists()` before ops.
- **Recursion Caution**: For huge dirs, prefer iterators (`enumerate_*`) over lists (`get_*`) to save memory.
- **Timestamp Parsing**: Always specify TZ for UTC; test str formats in scripts.
- **Error Wrapping**: Catch `PermissionError`/`OSError` for user-friendly messages (e.g., "Access denied").
- **Symlinks**: Check `os.path.islink()` before resolving; avoid cycles.
- **Size Calcs**: Cache results for repeated calls; use `show_unit=True` for logs.
- **Tree Output**: Customize `ignore_list` by forking `get_tree()` for project-specific skips.
- **Cross-Platform**: Test timestamps on Unix (no true birthtime); use `os.sep` for manual joins.

## Limitations

- **Unix Timestamps**: Creation time is change time (`getctime`); setting uses modtime approx—no birthtime support.
- **Symlinks**: Creation fails on Windows without admin; resolution may loop if cyclic.
- **Enumeration**: Glob patterns are fnmatch-based (not regex); hidden files included unless patterned (e.g., ".*").
- **Move Cross-Device**: `shutil.move` copies+delete for non-same FS—inefficient for large dirs.
- **Tree Depth**: No limit; deep nests may truncate output—add recursion cap if needed.
- **No Async**: Synchronous I/O; thread for UIs.
- **Size Overhead**: Recursive walks scan all files—skip via custom walkers for exts.

## Contributing

See the root [README.md](https://github.com/hbisneto/FileSystemPro/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., async enumeration) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE) for details.