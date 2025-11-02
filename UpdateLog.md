# FileSystemPro 2.1.0.0

This update introduces enhanced cross-platform console styling with support for underline and strikethrough, a new asynchronous update checker in the core module, expanded compression capabilities with metadata returns and format options, and improved robustness in directory and file operations through better error handling and conflict resolution. This release also includes other features, bug fixes, and performance enhancements for more reliable file system management across Linux, macOS, and Windows.

## Console

### New Features
- Added support for underline and strikethrough styles in ANSI escape codes (UNDERLINE=4, STRIKETHROUGH=9) and Win32 attributes (UNDERSCORE=0x4000, STRIKEOUT=0x8000).
- Introduced the `Console` class for chained, intuitive text styling (e.g., `console.red().underline("Warning")`), with convenience methods like `light_green()`, `red_bg()`, and automatic reset on invocation.
- Version updated to 3.0.0.0, reflecting expanded style options and API improvements.

### Improvements
- Enhanced `WinTerm` class to track and apply underline/strikethrough flags independently, preventing conflicts with existing bright/light color emulation.
- Extended `AnsiStyle` with reset codes (RESET_UNDERLINE=24, RESET_STRIKETHROUGH=29) for precise style management.
- Improved OSC handling in `AnsiToWin32` for better title setting and cursor operations on Windows.

## Core

### New Features
- Added the `__core__` module for centralized configuration and update management.
- Implemented asynchronous update checking (`check_updates_async`) using GitHub API and threading, with daemon threads to avoid blocking; supports callbacks for notifications.
- Auto-runs async update checks on import, comparing versions via digit extraction (e.g., notifies on new releases with pip upgrade prompt).

## Compression

### New Features
- `create_tar` now supports compression modes ('gz', 'bz2') for flexible TAR variants (.tar.gz, .tar.bz2).
- Extraction functions (`extract_tar`, `extract_zip`) return metadata dictionaries via `wrapper.get_object(destination)` for post-operation insights.
- `read_tar` added for listing TAR contents, mirroring ZIP functionality.

### Improvements
- Full implementation of all functions with comprehensive try-except blocks for specific exceptions (e.g., KeyError for missing files, RuntimeError for extraction failures).
- Enhanced `extract_zip` flexibility: Supports None (all items), lists, or single strings for partial extraction.
- `read_zip` now filters system files (e.g., `__MACOSX/`, `.DS_Store`) by default, with an opt-in toggle.

## Directory

### Improvements
- `move` function enhanced with `force_overwrite` parameter and conflict checks (raises `FileExistsError` or `OSError` if destination exists and not a directory).
- `rename` now explicitly raises `FileExistsError` for existing destinations, improving predictability.
- Added `check_conflict` helper for safer path operations during recursive moves.

## File

### Improvements
- Refined `split_file` documentation and behavior: Clarifies original file preservation, specifies `.fsp{index}` naming, and adds explicit raises for `IOError` and `PermissionError`.
- `reassemble_file` optimized to delete parts only after successful concatenation, reducing partial failure risks.

---

### This update also includes the following enhancements and bug fixes:

#### New Features
- Integrated Console styling into core update notifications for colored, user-friendly messages (e.g., blue notices, green upgrade prompts).

#### Improvements
- Unified error propagation across modules with descriptive messages and consistent exception types for better debugging.
- Expanded docstrings in all updated modules with detailed parameters, returns, raises, and examples for improved developer experience.
- Performance tweak in `WinTerm.get_attrs()` to bitwise-OR new style flags without recalculating base attributes.

#### Bug Fixes
- Resolved potential attribute clobbering in Win32 console by separately tracking light, underline, and strikethrough flags in `WinTerm`.
- Fixed incomplete OSC regex handling in `AnsiToWin32.convert_osc` to properly process title changes without truncation.
- Addressed version comparison edge cases in `__checkupdates__` by filtering only digits, preventing non-numeric tag mismatches (though semver parsing recommended for future).