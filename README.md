# FileSystemPro

[![PyPI](https://img.shields.io/pypi/v/FileSystemPro?logo=python&logoColor=white&color=blue)](https://pypi.org/project/FileSystemPro/)
[![Python](https://img.shields.io/badge/Python-%3E=3.10-blue)](https://python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/hbisneto/FileSystemPro)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

FileSystemPro is a powerful, cross-platform Python toolkit for file and directory management, system monitoring, compression, and enhanced console output. It provides seamless abstractions for OS-specific paths, resource tracking (CPU, disks, memory, network), archive handling (tar/zip), change detection, and colored terminal styling. Built for developers, it integrates standard library tools with optional `psutil` for hardware insights, ensuring portability across Linux, macOS, and Windows.

**Key Pillars**:

- **FileSystem Abstraction**: OS-agnostic paths to user folders (e.g., Desktop, Documents).
- **Resource Monitoring**: Track CPU/memory/disks/network via `device` submodule.
- **File/Directory Ops**: Creation, manipulation, enumeration, and integrity checks.
- **Compression & Watching**: Tar/zip handling and real-time filesystem change detection.
- **Console Enhancement**: ANSI colors/styles with Windows compatibility.

**Compatibility**: Python 3.10+; cross-platform (Linux/macOS/Windows).

---

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](https://github.com/hbisneto/FileSystemPro/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## Getting Started

### Requirements
- Python 3.10+ ([download](https://www.python.org/)).
- Optional: `psutil` for `device` module (`pip install psutil`).

### Installation

Upgrade pip first:

```bash
pip install --upgrade pip
```
Install FileSystemPro:

```bash
pip install FileSystemPro
```

### For Developers/Contributors

Clone the repo:

```bash
git clone https://github.com/hbisneto/FileSystemPro.git
cd FileSystemPro
```

Upgrade build tools:

```bash
pip install --upgrade setuptools wheel
```

> Note: Requires setuptools 69.5.1+; wheel for packaging.

Run tests or build: See [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md).

## Table of Contents

Jump to module documentation for detailed APIs, examples, and best practices:

- **[FileSystem Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/README.md)**: OS detection and standard folder paths (`desktop`, `documents`, etc.).
- **[Core Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/__core__/README.md)**: Config management, logging, performance tuning, and update checks.
- **[Compression Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/compression/README.md)**: Tar/zip creation, extraction, and reading.
- **[Directory Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/directory/README.md)**: Path operations, creation/deletion, enumeration, timestamps, and tree views.
- **[File Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/file/README.md)**: I/O, integrity (SHA-256), copy/move, splitting, and timestamps.
- **[Watcher Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/watcher/README.md)**: Polling-based filesystem change detection with callbacks.
- **[Wrapper Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/wrapper/README.md)**: Unified metadata dicts (paths, sizes, timestamps).
- **[Console Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/console/README.md)**: ANSI colors, backgrounds, and styles (chainable, Windows-compatible).
- **[Device Module](https://github.com/hbisneto/FileSystemPro/blob/main/filesystem/device/README.md)**: CPU/disks/memory/network monitoring (requires `psutil`).

## Quick Start

Import core modules:

```python
import filesystem as fs  # Paths
from filesystem import file, directory, compression  # Ops
from filesystem import device  # Monitoring (needs psutil)
from filesystem import console  # Colored output
```

Example: List Downloads files with colors:

```python
from filesystem import fs, file, console

files = file.get_files(fs.downloads)
for f in files:
    size = file.get_size(f, show_unit=True)
    print(console.green()(f) + f" ({size})")
```

Monitor CPU:

```python
import time
from filesystem import device

while True:
    usage = device.cpu.cpu_percent()
    print(console.red() if usage > 80 else console.green()(f"CPU: {usage}%"))
    time.sleep(1)
```

## Architecture

FileSystemPro follows a modular design:

- **Core (`__core__`)**: Config/logging/updates.
- **FileSystem**: Entry point for paths.
- **Ops (`file`/`directory`/`compression`)**: Manipulation.
- **Monitoring (`watcher`/`device`)**: Changes/resources.
- **Utilities (`wrapper`/`console`)**: Metadata/styling.

See submodule READMEs for internals.

## Contributing

1. Fork/clone the repo.
2. Install dev deps: `pip install -e .[dev]`.
3. Add tests in `tests/`.
4. Run: `pytest` / `black .` / `flake8`.
5. PR to `main`.

Guidelines: [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md).

## License

MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE).