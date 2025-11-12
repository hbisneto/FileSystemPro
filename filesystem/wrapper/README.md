# Wrapper Module

## Overview

The `wrapper` module in **FileSystemPro** serves as a convenient utility layer for gathering comprehensive, structured metadata about files or directories at a specified path. The primary function, `get_object`, returns a dictionary with essential details such as absolute paths, formatted timestamps (in "YYYY/MM/DD HH:MM:SS:ff" format for creation, access, and modification), existence and type flags (file, directory, symlink), basename components (name, extension, name without extension), parent directory, and formatted size (with units from bytes to TB for readability). For directories, size is computed recursively by summing all contained file sizes.

Additionally, `has_extension` provides a quick string-based check for whether a path includes a file extension, useful for validation even on non-existent paths. All functions leverage standard library APIs (`os`, `datetime`) for cross-platform consistency, with error propagation for issues like non-existence or permissions. This module is internally used by other FileSystemPro components (e.g., `file`, `directory`) but is exposed for direct use in custom workflows requiring unified metadata access.

This module is ideal for **programmers implementing file explorers, audit logs, or data catalogs**, where a single call yields a portable, human-readable snapshot of an object's properties without manual `os.stat` boilerplate. Timestamps use local system time; sizes format to one decimal place for precision.

**Key Design Choices**:

- **Formatted Outputs**: Strings for dates/sizes to simplify logging/UI display; raw values available via underlying modules.
- **Recursive Sizing**: Dirs include all files (no hidden/symlink recursion by default—use `os.walk` flags if needed).
- **Lightweight**: No dependencies beyond stdlib and sibling modules (`file`, `directory` for size helpers).
- **Error Handling**: Raises `FileNotFoundError`/`PermissionError` on access failures; no fallbacks.

**Compatibility**:

- Python 3.10+ (uses `os.walk`, `datetime.strftime` with `%f` for microseconds).
- Platforms: Cross-platform (Unix creation time ≈ change time).
- Dependencies: Standard library + `filesystem.file`/`directory`.

## Features

- **Unified Metadata Dict**: Single call returns 13+ properties: paths, times (formatted str), types (bools), names/exts, size (str with units).
- **Timestamp Formatting**: Consistent "YYYY/MM/DD HH:MM:SS:ff" (ff = microseconds) for creation/access/modified.
- **Size Formatting**: Auto-scales (e.g., "1.2 KB", "10.5 MB"); recursive for dirs.
- **Type Detection**: Flags for `is_dir`, `is_file`, `is_link`, `exists`.
- **Extension Handling**: Extracts last `.ext`; `has_extension` for quick bool checks.
- **Path Normalization**: Absolute paths, dirname, basename (with/without ext).
- **Non-Existent Tolerance**: `has_extension` works on strings; `get_object` raises on access.

## Installation and Setup

Part of **FileSystemPro**—install via:

```bash
pip install filesystempro
```

No configuration required; import and call. For custom formats, extend helpers (e.g., UTC via `datetime.utcfromtimestamp`).

## Usage

Import the module:

```python
from filesystem import wrapper as wra
```

### Core Functions

#### `get_object(path: str) → dict`

- **Description**: Fetches full metadata dict. Raises on non-existent/inaccessible paths.
- **Returns**: 
	- Dict with keys: `'abspath'`, `'access'`, `'created'`, `'dirname'`, `'exists'`, `'is_dir'`, `'is_file'`, `'is_link'`, `'extension'`, `'modified'`, `'name'`, `'name_without_extension'`, `'size'`.
  - Times: Str like "2025/11/10 19:48:00:123456".
  - Size: Str like "1.2 KB" (dirs: recursive total).
- **Raises**: `FileNotFoundError`, `PermissionError`.
- **Notes**: Uses `os.path.abspath`; extension from last `.` (empty for no ext); size via `file.get_size` helper.

#### `has_extension(file_path: str) → bool`

- **Description**: Checks if path has a non-empty extension (e.g., '.txt' → True; '/file' → False). String-based, no existence check.
- **Returns**: `bool`.
- **Raises**: None.
- **Notes**: Via `os.path.splitext`; case-sensitive.

## Examples

### Metadata Retrieval

```python
from filesystem import wrapper as wra
import filesystem as fs

# File metadata
file_path = f"{fs.desktop}/example.txt"
details = wra.get_object(file_path)
print(details)
# Output example:
# {
#   'abspath': '/home/user/Desktop/example.txt',
#   'access': '2025/11/10 19:48:00:000000',
#   'created': '2025/11/10 19:47:00:123456',
#   'dirname': '/home/user/Desktop',
#   'exists': True,
#   'is_dir': False,
#   'is_file': True,
#   'is_link': False,
#   'extension': 'txt',
#   'modified': '2025/11/10 19:48:00:000000',
#   'name': 'example.txt',
#   'name_without_extension': 'example',
#   'size': '12.0 bytes'
# }

# Directory metadata (recursive size)
dir_path = f"{fs.documents}/project"
dir_details = wra.get_object(dir_path)
print(f"Dir size: {dir_details['size']}")  # e.g., "2.5 MB"
print(f"Is dir: {dir_details['is_dir']}")  # True
```

### Extension Check

```python
from filesystem import wrapper as wra

print(wra.has_extension("/docs/report.pdf"))  # True
print(wra.has_extension("/docs/config"))      # False
print(wra.has_extension("archive.tar.gz"))    # True (last ext: 'gz')
```

### Integration with Other Modules

```python
from filesystem import wrapper as wra, file as fsfile

# Filter files by metadata
files = fsfile.get_files("/path/to/dir", fullpath=True)
for f in files:
    details = wra.get_object(f)
    if details['size'] > '1.0 MB' and details['extension'] == 'py':
        print(f"Large Python: {details['name']}")
```

## Best Practices

- **Batch Usage**: Call `get_object` once per path; cache dicts for repeated access (immutable post-call).
- **Error Handling**: Wrap in try-except for `FileNotFoundError` (e.g., user input validation).
- **Size Performance**: Recursive dir sizing scans all files—use for small/medium dirs; parallelize for large via threading.
- **Timestamp Locale**: Formatted for readability; parse back with `datetime.strptime` if needed.
- **Extension Edge Cases**: Handles multi-dot (e.g., 'tar.gz' → 'gz'); use `pathlib` for advanced parsing.
- **Cross-Platform**: Test sizes/timestamps on Windows (no true birthtime); use `exists` pre-call.
- **Logging/UI**: Dict keys are consistent—serialize to JSON for persistence.

## Limitations

- **No Raw Values**: Formatted strings only (no int timestamps/sizes)—access via `os.stat` if needed.
- **Recursive Size**: Includes all files (no hidden/symlink skips); may be slow for huge dirs (>10k files).
- **Unix Timestamps**: Creation uses `getctime` (change time); no birthtime.
- **Extension Simplicity**: Last dot only; no MIME/resolution (extend with `mimetypes`).
- **No Caching**: Fresh `os.walk` each call—memoize externally for perf.
- **Symlinks**: `is_link` detects; size follows (potential infinite recursion if cycles—add checks).
- **Microsecond Precision**: `%f` pads to 6 digits; sub-us not captured.

## Contributing

See the root [README.md](https://github.com/hbisneto/FileSystemPro/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., raw value options, async sizing) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE) for details.