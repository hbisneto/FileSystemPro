# File Module

## Overview

The `file` module in **FileSystemPro** offers an extensive, cross-platform API for file handling, covering I/O operations (create/append/read/write in text/binary modes), integrity verification (SHA-256 checksums, duplicate detection, batch checks), manipulation (copy/move/rename/delete, symlinks, splitting/reassembling), metadata extraction (size/extension/filename, timestamps in local/UTC), and batch reporting. It integrates seamlessly with `directory` for recursive ops, `wrapper` for metadata dicts (e.g., `{'abspath': '/path', 'size': '1.5 MB', 'modified': '2025-11-10 19:48:00'}`), and `filesystem` for paths. Functions emphasize safety (overwrite flags, existence checks), efficiency (chunked reads for large files), and error granularity (specific exceptions like `FileExistsError`).

This module empowers **programmers building data pipelines, backup systems, or forensics tools**, where reliable file ops and tamper detection are key. Timestamps use `os.stat()` (Unix: creation ≈ change time; setting via `utime()` approximates). Integrity tools log to files and support JSON hash references. Splitting uses `.fsp{i}` extensions (1 MB default chunks); reassemble deletes parts post-merge.

**Key Design Choices**:

- **Chunked Processing**: Hashing/I/O uses 4KB buffers for large files; split/reassemble handles partial parts.
- **Encoding Defaults**: UTF-8 for text; binary ops preserve bytes.
- **Batch Resilience**: Partial failures in multi-file ops continue without halting.
- **Unix Mode**: Exposed via `st_mode` (int/octal) for permissions.

**Compatibility**:

- Python 3.10+ (relies on `os`, `shutil`, `hashlib`, `codecs`, `json`, `logging`).
- Platforms: Cross-platform (symlinks Unix-favored; timestamps Unix-limited).
- Dependencies: Standard library only.

## Features

- **I/O Operations**: Append/create lines/text/bytes/binary (with encoding/buffer); enumerate with metadata.
- **Integrity Verification**: Compute/check SHA-256 hashes; batch verify dirs/files vs. references; find duplicates; generate/load/save reports.
- **Path & Metadata**: Get extension/filename/size (raw/formatted), Unix mode; list files (filtered by ext/fullpath).
- **Manipulation**: Copy/move/rename/delete (overwrite/rename options); create symlinks; split/reassemble (chunked).
- **Timestamps**: Get/set creation/access/write times (local/UTC, datetime/str input; str: "%Y-%m-%d %H:%M:%S").
- **Batch & Reporting**: Process multi-paths; log verification; JSON hash persistence; detailed reports.
- **Error Handling**: Specific raises (`FileNotFoundError`, `FileExistsError`, `IOError`); logs errors in batch ops.

## Installation and Setup

Included in **FileSystemPro**—install via:

```bash
pip install filesystempro
```

No extra config; uses `logging` for reports (INFO level default). For UTC, import `datetime.timezone.utc` if needed.

## Usage

Import the module (alias `fsfile` optional for brevity):

```python
from filesystem import file as fsfile  # Or: import filesystem.file as fsfile
```

Functions are standalone; use absolute paths with `filesystem` (e.g., `fs.documents`).

### Function Reference

Categorized tables with params, returns, raises. All raise `FileNotFoundError`/`PermissionError`/`IOError` unless noted.

#### I/O Operations

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `append_all_bytes(file: str, data: bytes)` | `file` (str), `data` (bytes). | None. | `IOError`, `PermissionError`. |
| `append_all_lines(file: str, lines: list[str], encoding: str = "utf-8")` | `file` (str), `lines` (list), `encoding` (str). | None. | `IOError`, `PermissionError`, `UnicodeEncodeError`. |
| `append_all_text(file: str, content: str, encoding: str = "utf-8")` | `file` (str), `content` (str), `encoding` (str). | None. | `IOError`, `PermissionError`, `UnicodeEncodeError`. |
| `append_text(file: str, text: str, encoding: str = "utf-8")` | `file` (str), `text` (str), `encoding` (str). | None. | `IOError`, `PermissionError`, `UnicodeEncodeError`. |
| `create(file: str, data: str, overwrite: bool = False, encoding: str = "utf-8")` | `file` (str), `data` (str), flags/encoding. | `dict`: Metadata. | `IOError`, `PermissionError`, `UnicodeEncodeError`. |
| `create_binary_file(filename: str, data: str \| bytes, buffer_size: int = 4096)` | `filename` (str), `data` (str/bytes), `buffer_size` (int). | None. | `IOError`, `PermissionError`, `UnicodeEncodeError`. |
| `enumerate_files(file: str)` | `file` (str; dir). | `list[dict]`: Metadata per entry. | `FileNotFoundError`, `PermissionError`. |
| `get_files(path: str, fullpath: bool = True, extension: str = None)` | `path` (str; dir), `fullpath` (bool), `extension` (str). | `list[str]`: Files (filtered). | `FileNotFoundError`, `PermissionError`. |

#### Integrity Tools

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `batch_check_integrity(paths: str \| list, reference_hashes: dict = None, log_file: str = "integrity_report.log")` | `paths` (str/list), `reference_hashes` (dict), `log_file` (str). | `dict`: Results (counts, details, errors). | `FileNotFoundError`, `PermissionError`, `IOError`. |
| `calculate_checksum(file: str)` | `file` (str). | `str`: SHA-256 hex. | `FileNotFoundError`, `IOError`. |
| `check_integrity(file: str, reference_file: str)` | `file` (str), `reference_file` (str). | `bool`: Match. | `FileNotFoundError`, `IOError`. |
| `find_duplicates(path: str)` | `path` (str; dir). | `tuple[list[str], list[str]]`: (originals, duplicates). | `FileNotFoundError`, `PermissionError`. |
| `generate_integrity_report(results: dict, output_file: str = None)` | `results` (dict), `output_file` (str). | `str`: Report text (saves if file). | `PermissionError`, `IOError`. |
| `load_reference_hashes(input_file: str)` | `input_file` (str; JSON). | `dict`: Path → hash. | `FileNotFoundError`, `PermissionError`, `IOError`. |
| `save_reference_hashes(paths: str \| list, output_file: str)` | `paths` (str/list), `output_file` (str). | None. | `FileNotFoundError`, `PermissionError`, `IOError`. |

#### Path & Metadata

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `exists(file: str)` | `file` (str). | `bool`: Exists. | `PermissionError`. |
| `get_extension(file: str, lower: bool = True)` | `file` (str), `lower` (bool). | `str`: Ext (e.g., '.txt'). | None. |
| `get_filename(file: str)` | `file` (str). | `str`: Basename. | None. |
| `get_size(file: str, show_unit: bool = False)` | `file` (str), `show_unit` (bool). | `int` or `str`: Size (bytes or formatted). | `FileNotFoundError`, `OSError`. |
| `get_unix_file_mode(file: str, octal: bool = False)` | `file` (str), `octal` (bool). | `int`: Mode (int/octal). | `FileNotFoundError`, `IOError`. |

#### Manipulation

| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `copy(source: str \| list, destination: str, overwrite: bool = False)` | `source` (str/list), `destination` (str), `overwrite` (bool). | None. | `FileNotFoundError`, `FileExistsError`, `PermissionError`, `Exception`. |
| `create_symbolic_link(file_target: str, file_link: str)` | Targets (str). | `dict`: Link metadata. | `FileNotFoundError`, `OSError`, `PermissionError`. |
| `delete(file: str)` | `file` (str). | None. | `FileNotFoundError`, `PermissionError`. |
| `move(source: str, destination: str, new_filename: str = None, replace_existing: bool = False)` | `source` (str), `destination` (str), `new_filename` (str), `replace_existing` (bool). | None. | `FileNotFoundError`, `FileExistsError`, `PermissionError`. |
| `rename(old_name: str, new_name: str)` | Names (str). | `bool`: Success. | `PermissionError`. |
| `reassemble_file(large_file: str, new_file: str)` | `large_file` (str; base), `new_file` (str). | None. | `IOError`, `PermissionError`. |
| `split_file(file: str, chunk_size: int = 1048576)` | `file` (str), `chunk_size` (int). | `bool`: Success. | `IOError`, `PermissionError`. |

#### Timestamps (Get)

Return `datetime`; UTC via `utcfromtimestamp()`. Unix: creation ≈ change.
| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `get_creation_time(file: str)` / `get_creation_time_utc(file: str)` | `file` (str). | `datetime`: Time. | `FileNotFoundError`, `IOError`. |
| `get_last_access_time(file: str)` / `get_last_access_time_utc(file: str)` | As above. | `datetime`: Access. | As above. |
| `get_last_write_time(file: str)` / `get_last_write_time_utc(file: str)` | As above. | `datetime`: Write. | As above. |

#### Timestamps (Set)

Accept `datetime` or str ("%Y-%m-%d %H:%M:%S"); approx via `utime()`. UTC converts to local timestamp.
| Function | Parameters | Returns | Raises |
|----------|------------|---------|--------|
| `set_creation_time(file: str, creation_time: datetime \| str)` / `set_creation_time_utc(...)` | `file` (str), time (datetime/str). | None. | `FileNotFoundError`, `OSError`, `ValueError`, `PermissionError`. |
| `set_last_access_time(file: str, last_access_time: datetime \| str)` / `set_last_access_time_utc(...)` | As above. | None. | As above. |
| `set_last_write_time(file: str, last_write_time: datetime \| str)` / `set_last_write_time_utc(...)` | As above. | None. | As above. |

## Examples

### Basic I/O and Metadata

```python
from filesystem import file as fsfile
import filesystem as fs
from datetime import datetime

# Create and append text
fsfile.create(f"{fs.desktop}/example.txt", "Initial content", overwrite=True)
fsfile.append_text(f"{fs.desktop}/example.txt", " Appended text")

# Get metadata
size = fsfile.get_size(f"{fs.desktop}/example.txt", show_unit=True)
ext = fsfile.get_extension(f"{fs.desktop}/example.txt")
print(f"Size: {size}, Ext: {ext}")  # e.g., "12.0 bytes", ".txt"

# Binary create
fsfile.create_binary_file(f"{fs.desktop}/example.bin", b"Binary data")
```

### Integrity and Batch Verification

```python
from filesystem import file as fsfile

# Single checksum
checksum = fsfile.calculate_checksum("example.txt")
print(f"SHA-256: {checksum}")

# Check vs. reference
is_match = fsfile.check_integrity("copy.txt", "original.txt")
print(f"Match: {is_match}")

# Batch with reference (save first)
fsfile.save_reference_hashes(["file1.txt", "file2.txt"], "hashes.json")
results = fsfile.batch_check_integrity(["file1.txt", "file2.txt"], fsfile.load_reference_hashes("hashes.json"))
report = fsfile.generate_integrity_report(results, "report.txt")
print(report)  # Formatted summary
```

### Manipulation and Splitting

```python
from filesystem import file as fsfile

# Copy/move with overwrite
fsfile.copy("source.txt", f"{fs.documents}/dest/", overwrite=True)
fsfile.move(f"{fs.documents}/dest/source.txt", f"{fs.desktop}/new_dest/", replace_existing=True)

# Symlink
fsfile.create_symbolic_link("target.txt", "link.txt")

# Split/reassemble (1 MB chunks)
success = fsfile.split_file("large.bin", chunk_size=1024*1024)
if success:
    fsfile.reassemble_file("large", "reassembled.bin")  # Deletes .fsp* parts
```

### Timestamps

```python
from filesystem import file as fsfile
from datetime import datetime

# Get times
write_time = fsfile.get_last_write_time("example.txt")
utc_access = fsfile.get_last_access_time_utc("example.txt")
print(f"Write: {write_time}, UTC Access: {utc_access}")

# Set (str input)
fsfile.set_last_write_time("example.txt", "2023-01-01 12:00:00")
fsfile.set_last_write_time_utc("example.txt", datetime(2023, 1, 1, 12, 0))
```

### Duplicates and Enumeration

```python
from filesystem import file as fsfile

# Find duplicates in dir
originals, dups = fsfile.find_duplicates("/path/to/dir")
print(f"Originals: {originals}, Duplicates: {dups}")

# Enumerate with metadata
entries = fsfile.enumerate_files("/path/to/dir")
for entry in entries:
    print(f"{entry['name']} ({entry['size']}) - Modified: {entry['modified']}")
```

## Best Practices

- **Paths**: Use `fs.OS_SEPARATOR` and `filesystem` constants; validate with `exists()` pre-op.
- **Large Files**: Leverage chunked funcs (checksum/split); monitor buffers for perf.
- **Integrity**: Save/load hashes pre/post-transfer; use batch for dirs (logs auto).
- **Timestamps**: Specify TZ for UTC; test on Unix (no true birthtime set).
- **Batch Ops**: Handle partial failures via try-except; filter exts in `get_files`.
- **Security**: Verify hashes before exec; avoid overwrite in prod without flags.
- **Error Handling**: Wrap in try-except for `IOError` (e.g., "Disk full"); log via `logging`.
- **Testing**: Mock `os.stat`/`open` for units; test splits on >1GB files.

## Limitations

- **Unix Timestamps**: Creation ≈ change (`st_ctime`); setting via modtime—no birthtime.
- **Symlinks**: Windows needs admin; dangling links not auto-resolved.
- **Splitting**: Sequential `.fsp{i}` only; ignores missing parts (no error); no compression.
- **Batch**: Continues on errors (no rollback); logs to fixed file (customize path).
- **Encoding**: UTF-8 default; non-ASCII may fail without explicit encoding.
- **Duplicates**: Hash-based (size-agnostic); false positives rare but possible (collision).
- **No Async**: Sync I/O; use `threading` for concurrency in apps.
- **Size Units**: Up to YB; floats for <1024 (e.g., "0.5 KB").

## Contributing

See the root [README.md](../../README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., async I/O, MD5 support) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](../LICENSE) for details.