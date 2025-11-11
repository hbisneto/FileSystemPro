# Compression Module

## Overview

The `compression` module in **FileSystemPro** offers a comprehensive suite of utilities for handling tar and zip archives, enabling seamless creation, extraction, and inspection of compressed files and directories. It abstracts away low-level details from `tarfile` and `zipfile` modules, providing cross-platform functions that preserve directory structures, support optional compression levels, and include selective operations (e.g., extracting specific files). All functions integrate with the `wrapper` module for metadata retrieval, returning dictionaries with details like file size, absolute path, and modification time—ideal for logging or UI feedback.

This module is tailored for **programmers developing backup tools, deployment scripts, or data packaging applications**, where reliable archive management is essential. It handles single or multi-item inputs, auto-appends extensions, and filters out system artifacts (e.g., macOS `__MACOSX` folders) during reads. Operations are synchronous and efficient, using recursive walks for directories without unnecessary overhead.

**Key Design Choices**:

- **Structure Preservation**: Relative paths are maintained per item, but multi-item archives root entries separately (no forced common base).
- **Error Granularity**: Specific exceptions for common issues (e.g., `FileNotFoundError`, `KeyError` for missing entries).
- **Compression Support**: Tar-specific (none/gz/bz2); Zip uses built-in DEFLATE.
- **Stdlib Reliance**: No external dependencies beyond the standard library and `filesystem.wrapper`.

**Compatibility**:

- Python 3.10+ (leverages `os.walk`, `pathlib` indirectly via wrapper).
- Platforms: Cross-platform (tested on Linux, macOS, Windows).
- File Systems: Handles Unicode paths and large files.

## Features

- **Tar Operations**:
  - Create archives from files/directories with optional gzip/bzip2 compression.
  - Extract full archives or selective files/directories.
  - List all contents without extraction.
- **Zip Operations**:
  - Create archives from files/directories (preserves structure).
  - Extract full archives, specific files, or single files.
  - List contents, with optional exclusion of OS-specific system files (e.g., `.DS_Store`, `Thumbs.db`).
- **Input Flexibility**: Accepts single paths (str) or lists for batch operations.
- **Metadata Integration**: Returns `wrapper.get_object()` dicts for created/extracted items (e.g., `{'size': '1.2 MB', 'abspath': '/path/to/archive.tar.gz'}`).
- **Auto-Detection**: Tar extraction auto-handles compressed formats; zip appends `.zip` if missing.
- **Helper Functions**: Internal `add_to_tar`/`add_to_zip` for recursive addition (exposed in docstrings for advanced use).
- **Robust Error Handling**: Propagates OS errors; custom messages for archive-specific issues.

## Installation and Setup

As part of **FileSystemPro**, install via pip:

```bash
pip install filesystempro
```

No additional setup required—functions use standard library modules. Ensure write permissions for destinations and read access for sources.

## Usage

Import the module directly:

```python
from filesystem import compression
```

Functions are standalone; pass paths as strings or lists. Use absolute paths for reliability, or combine with `filesystem` module constants (e.g., `fs.documents`).

### Function Reference

#### Tar Functions

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `create_tar(fullpath_files: str \| list, destination: str, compression: str = 'none')` | - `fullpath_files`: Path(s) to compress.<br>- `destination`: Output path (auto-extends).<br>- `compression`: `'none'`, `'gz'`, or `'bz2'`. | `dict`: Archive metadata. | `FileNotFoundError`, `PermissionError`, `ValueError`. |
| `extract_tar(tar_filename: str, destination: str, extraction_list: list = [])` | - `tar_filename`: Input archive.<br>- `destination`: Extract dir.<br>- `extraction_list`: Optional files to extract. | `dict`: Destination metadata. | `FileNotFoundError`, `KeyError`, `PermissionError`, `Exception`. |
| `read_tar(tar_filename: str)` | - `tar_filename`: Input archive. | `list[str]`: File names. | `FileNotFoundError`, `Exception`. |

#### Zip Functions

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `create_zip(fullpath_files: str \| list, destination: str)` | - `fullpath_files`: Path(s) to compress.<br>- `destination`: Output path (auto-`.zip`). | `dict`: Archive metadata. | `FileNotFoundError`, `PermissionError`, `ValueError`. |
| `extract_zip(zip_path: str, destination: str, extraction_list: None \| list \| str = None)` | - `zip_path`: Input archive.<br>- `destination`: Extract dir.<br>- `extraction_list`: None (all), list (multi), or str (single). | `dict`: Destination metadata. | `FileNotFoundError`, `KeyError`, `PermissionError`, `ValueError`, `RuntimeError`. |
| `read_zip(zip_filename: str, show_compression_system_files: bool = True)` | - `zip_filename`: Input archive.<br>- `show_compression_system_files`: Include/exclude OS artifacts. | `list[str]`: File names (filtered if False). | `FileNotFoundError`, `Exception`. |

**Notes**:

- Directories are recursed; only files are added (empty dirs ignored).
- Extraction creates destination dir if missing (`os.makedirs(..., exist_ok=True)`).
- System files filtered in `read_zip`: `__MACOSX/`, `.DS_Store`, `Thumbs.db`.

## Examples

### Tar Archive Creation and Extraction

```python
from filesystem import compression
import filesystem as fs  # For paths

# Create gzip tar from files in Documents
source_files = [f"{fs.documents}/file1.txt", f"{fs.documents}/my_dir"]
archive_path = f"{fs.desktop}/backup.tar.gz"
result = compression.create_tar(source_files, archive_path, compression='gz')
print(f"Created: {result['abspath']} (Size: {result['size']})")

# Extract specific files
extraction_list = ["file1.txt", "my_dir/subfile.txt"]
extract_result = compression.extract_tar(archive_path, f"{fs.desktop}/extracted", extraction_list)
print(f"Extracted to: {extract_result['abspath']}")

# List contents
contents = compression.read_tar(archive_path)
print(f"Contents: {contents}")
```

### Zip Archive Operations

```python
from filesystem import compression
import filesystem as fs

# Create zip from directory
dir_path = f"{fs.documents}/project"
zip_path = f"{fs.desktop}/project.zip"
zip_result = compression.create_zip(dir_path, zip_path)
print(f"Zip created: {zip_result['size']}")

# Extract single file
single_extract = compression.extract_zip(zip_path, f"{fs.desktop}/single_out", extraction_list="src/main.py")
print(f"Single file extracted: {single_extract['size']}")

# Read with system files excluded
zip_contents = compression.read_zip(zip_path, show_compression_system_files=False)
print(f"Clean contents: {zip_contents}")
```

### Batch Multi-Item Compression

```python
from filesystem import compression

# Compress mixed files/dirs
items = ["/home/user/docs/report.pdf", "/home/user/images", "/home/user/scripts/backup.py"]
tar_result = compression.create_tar(items, "/backups/full.tar.bz2", 'bz2')
zip_result = compression.create_zip(items, "/backups/full.zip")

print(f"Tar: {tar_result['size']}, Zip: {zip_result['size']}")
```

### Error Handling Example

```python
from filesystem import compression
import logging

try:
    compression.extract_tar("/nonexistent.tar", "/out", ["missing.txt"])
except FileNotFoundError as e:
    logging.error(f"Archive missing: {e}")
except KeyError as e:
    logging.warning(f"Item not in archive: {e}")
```

## Best Practices

- **Path Management**: Use `filesystem` constants (e.g., `fs.downloads`) and `OS_SEPARATOR` for cross-platform safety.
- **Selective Extraction**: Always specify `extraction_list` for large archives to avoid overwriting unrelated files.
- **Compression Choice**: Use `'gz'` for speed/balance; `'bz2'` for max compression (slower). Test with your data.
- **Metadata Usage**: Leverage returned dicts for progress bars or summaries (e.g., `result['modified']`).
- **Permissions**: Run with sufficient privileges; wrap in try-except for user-facing apps.
- **Performance**: For very large dirs, consider async wrappers (future enhancement); current ops are I/O-bound.
- **Validation**: Pre-check paths with `os.path.exists()` if batching user inputs.
- **Cleanup**: Delete temp archives post-extraction to save space.

## Limitations

- **No Streaming**: Full in-memory for small/medium archives; very large files (>GB) may consume RAM—use external tools like `tar` CLI for streaming.
- **No Passwords**: Unsupported (zip/tar encryption); extend via `zipfile` params if needed.
- **Multi-Root Archives**: Items from different dirs appear as separate roots—use a staging dir for unified structure.
- **System File Filtering**: Zip-only; tar reads include all (customize `read_tar` if needed).
- **No Progress Callbacks**: Synchronous; add threading for UIs.
- **Windows Paths**: Handles backslashes, but test with long paths (>260 chars).

## Contributing

See the root [README.md](../README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., RAR support) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](../LICENSE) for details.