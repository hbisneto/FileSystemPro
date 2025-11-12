# Console Module

## Overview

The `console` module in **FileSystemPro** delivers a user-friendly, chainable interface for applying ANSI escape codes to enhance terminal output with colors, backgrounds, and text styles (e.g., bright, underline, strikethrough). Built on a customized extension of the Colorama library, it ensures cross-platform compatibility—automatically handling Windows console limitations via `AnsiToWin32` wrapping—while providing automatic style resets to prevent formatting bleed. The core `Console` class supports fluent method chaining for composing styles, and a global `console` instance enables immediate use without instantiation.

This module is tailored for **programmers enhancing CLI tools, logs, or debug outputs** in the FileSystemPro ecosystem, where colored feedback improves readability (e.g., green for success, red for errors). It supports standard ANSI colors (8 base + 8 light), backgrounds, and extended styles like underline/strikethrough with dedicated reset methods. Version: 3.0.0.0 (aligned with FileSystemPro core).

**Key Design Principles**:

- **Fluent API**: Chain methods like `console.red().bright().underline()` for concise styling.
- **Auto-Reset**: Invoking the instance (`console("text")`) appends `RESET_ALL` to clean up.
- **Windows Transparency**: Detects and enables VT processing; falls back to stripping on unsupported terminals.
- **Lightweight**: Stdlib + Colorama-inspired core; no heavy deps.

**Compatibility**:

- Python 3.10+ (leverages `re`, `sys`, `os`, `ctypes` for Windows).
- Platforms: Cross-platform (native ANSI on Unix; wrapped on Windows; strips on non-TTY).
- Dependencies: Internal (uses submodules: `ansi`, `ansitowin32`, `win32`, `winterm`, `initialise`).

## Features

- **Foreground Colors**: 8 base (black, red, green, yellow, blue, magenta, cyan, white) + 8 light variants (light_*_ex).
- **Background Colors**: Matching 8 base + 8 light (e.g., `red_bg()`, `light_blue_bg()`).
- **Text Styles**: Bright/dim, underline/strikethrough, with resets (reset, reset_underline, reset_strikethrough).
- **Method Chaining**: Build complex styles sequentially (e.g., color + style + background).
- **Global Instance**: Pre-built `console` for quick prototyping.
- **Automatic Reset**: Styles apply only to the wrapped text; no global state pollution.
- **TTY Detection**: Skips conversion on non-terminals (e.g., files, pipes).
- **Windows Support**: Enables virtual terminal processing; emulates styles via WinAPI calls.
- **Extensibility**: Subclass `Console` for custom palettes or add-ons.

## Installation and Setup

Included in **FileSystemPro**—install via:

```bash
pip install filesystempro
```

Auto-initializes on import (wraps `sys.stdout`/`stderr` if needed). For manual control:

```python
from filesystem.console import init, deinit
init(autoreset=True, convert=True)  # Enable wrapping
# ... use console ...
deinit()  # Restore original streams
```

Use `just_fix_windows_console()` for minimal Windows setup without full wrapping.

## Usage

Import and chain methods on the global `console` instance, then invoke with text:

```python
from filesystem import console
```

- **Basic**: `console.red()("Error!")` → Red text + reset.
- **Chained**: `console.blue().bright().yellow_bg()("Styled!")` → Blue bright text on yellow bg + reset.
- **Partial Reset**: `console.underline()("Underlined").reset_underline()(" plain")`.
- **Custom Instance**: `c = console.Console(); c.green()("Custom!")`.

For context managers: `with console.console_text(convert=True): print(colored_text)`.

### Color/Style Methods

#### Foregrounds

- `black()`, `blue()`, `cyan()`, `green()`, `magenta()`, `red()`, `yellow()`, `white()`.
- Light: `light_black()`, `light_blue()`, etc. (uses 90-97 ANSI).

#### Backgrounds

- `*_bg()` variants (e.g., `red_bg()`, `light_green_bg()`).

#### Styles

- `bright()`, `dim()`, `underline()`, `strikethrough()`.
- Resets: `reset()`, `reset_underline()`, `reset_strikethrough()`.

All return `self` for chaining; `RESET_ALL` auto-appended on call.

## Examples

### Simple Coloring

```python
from filesystem import console

# Single color
error = console.red()("Failed to load file!")
print(error)  # Red "Failed..." + reset

# Success message
success = console.green().bright()("Operation complete!")
print(success)  # Bright green + reset
```

### Chained Complex Styles

```python
from filesystem import console

# Multi-style with background
warning = console.yellow().bright().underline().red_bg()("Warning: High disk usage!")
print(warning)  # Yellow bright underlined on red bg + reset

# Partial reset in chain
mixed = console.magenta()("Magic").underline()(" under").reset_underline()("lined")
print(mixed)  # Magenta "Magic under" underlined, then plain "lined"
```

### Global vs. Custom Instance

```python
from filesystem import console

# Global
print(console.cyan()("Global cyan!"))

# Custom for reuse (though resets auto)
c = console.Console()
print(c.blue().dim()("Custom dim blue!"))
```

### Windows-Specific Setup

```python
from filesystem.console import just_fix_windows_console, console

just_fix_windows_console()  # Minimal enable VT
print(console.blue()("Works on Windows!"))
```

### Integration with FileSystemPro

```python
from filesystem import console, file as fsfile, wrapper as wra

# Colored file listing
files = fsfile.get_files("/path/to/dir")
for f in files:
    details = wra.get_object(f)
    color = console.green() if details['size'] < '1.0 MB' else console.red()
    print(color(f"{details['name']} ({details['size']})"))
```

## Best Practices

- **Chain Concisely**: Group related styles (e.g., `console.red().bright()`); avoid deep nests.
- **Reset Explicitly**: Use `reset()` for mid-text clears; rely on auto-reset for full phrases.
- **TTY Checks**: Test `console.stream.isatty()` before heavy use; strips on redirects.
- **Performance**: Chaining is cheap (string concat); for bulk output, build once and print.
- **Accessibility**: Offer `--no-color` flags (set `init(strip=True)`); dim for low-contrast.
- **Windows**: Call `init(convert=True)` early; use `just_fix_windows_console()` for apps.
- **Debugging**: Print raw ANSI (e.g., `console.red`) to verify sequences.
- **Extending**: Override `Console.__call__` for custom resets or logging.

## Limitations

- **ANSI Subset**: Supports 16 colors + basic styles; no 256/truecolor (extend `AnsiFore`).
- **Windows Quirks**: Older consoles (<Win10) may flicker; VT enable fails in some envs (e.g., Emacs).
- **No Dynamic Updates**: Static strings only; for live UIs, pair with `curses`/`rich`.
- **String Overhead**: Chaining builds temp strings; negligible for <1kB text.
- **Locale-Dependent**: Timestamps/dates use system TZ; format fixed (no i18n).
- **No Input Handling**: Output-only; for colored prompts, use `prompt_toolkit`.
- **Thread Safety**: Global `console` not thread-safe for concurrent writes—use instances.

## Contributing

See the root [README.md](https://github.com/hbisneto/FileSystemPro/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., 256-color support, bold italics) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE) for details. (Based on Colorama BSD 3-Clause.)