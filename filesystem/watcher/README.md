# Watcher Module

## Overview

The `watcher` module in **FileSystemPro** provides a flexible, polling-based file system monitoring system for detecting changes (file creation, updates, and deletions) in one or more directory roots. The core `Watcher` class supports multi-root observation, configurable filters (ignore patterns, file extensions, recursion depth), event-driven callbacks, change history with statistics, and non-blocking threaded polling. For simpler use cases, the `get_changes` function offers standalone monitoring with optional logging and notifications without class instantiation.

This module is optimized for **programmers developing real-time file sync tools, log analyzers, or automated build watchers**, where continuous directory scanning is required. It uses `os.walk` for state snapshots and diffs metadata (modification time, size) to detect events efficiently. Polling avoids platform-specific APIs (e.g., inotify/FSEvents), ensuring cross-platform reliability, though it trades some responsiveness for simplicity. History is capped to prevent memory bloat, and callbacks are invoked per event type or globally.

**Key Design Principles**:

- **Polling Efficiency**: Snapshots diff only changed paths; configurable delay balances CPU vs. latency.
- **Filter Granularity**: Pre-scan filtering reduces overhead; supports glob-like ignores.
- **Thread Safety**: Daemon thread for monitoring; queue for event dequeuing.
- **Extensibility**: Callbacks handle custom logic; history enables auditing.

**Compatibility**:

- Python 3.10+ (uses `threading.Queue`, `os.walk`, `datetime`).
- Platforms: Cross-platform (polling works everywhere; no native watchers).
- Dependencies: Standard library + `filesystem.file` for logging.

## Features

- **Multi-Root Support**: Monitor single or multiple directories concurrently.
- **Advanced Filtering**: Ignore basenames (e.g., `.git`), restrict extensions (e.g., `.py`), cap recursion depth.
- **Event Callbacks**: Register handlers for 'created', 'updated', 'removed', or 'all' events.
- **Change Detection**: Compares snapshots via modtime/size; detects adds/updates/deletes.
- **History & Analytics**: Tracks last N changes with timestamps; stats by event type.
- **Threaded Operation**: Background polling with customizable delay (default 5s).
- **Standalone Utility**: `get_changes` for quick setup with logging/notifications.
- **Metadata Integration**: Events include `abspath`, `modified`, `size`, `change`, `timestamp`.

## Installation and Setup

As part of **FileSystemPro**, install via:

```bash
pip install filesystempro
```

No additional setup—import and instantiate. For high-frequency polling, tune `delay` to avoid I/O thrashing.

## Usage

Import the module:

```python
from filesystem import watcher
```

### Watcher Class

Instantiate with roots and options:

```python
w = watcher.Watcher(
    roots='/path/to/monitor',  # Or list: ['/path1', '/path2']
    ignore_patterns=['.git', '__pycache__'],
    file_extensions=['.py', '.txt'],
    max_depth=3,
    history_size=100,
    event_handler=lambda change: print(f"Event: {change}")
)
```

Key methods:

- `register_handler(event_type: str, callback: callable)`: Add per-event or global handler.
- `diff() → list[dict]`: Manual scan/return changes (e.g., for on-demand checks).
- `get_stats() → dict`: Counts {'created': int, 'updated': int, 'removed': int}.
- Thread auto-starts in `__init__`; events queue for `while True: change = queue.get_nowait()`.

### Standalone Function

For fire-and-forget:

```python
watcher.get_changes(
    roots='/path/to/monitor',
    delay=10.0,
    create_log_file=True,
    log_filename='changes.log',
    notifier=lambda change: print(f"Alert: {change['change']} - {change['abspath']}")
)
```

Runs infinite loop; Ctrl+C to stop.

### Change Dict Format

Events yield dicts like:

```python
{
    'abspath': '/path/to/file.py',
    'modified': 1731342080.0,  # Timestamp
    'size': 1024,              # Bytes
    'change': 'updated',       # 'created'/'updated'/'removed'
    'timestamp': datetime(2025, 11, 10, 19, 48, 0)  # Detection time (history only)
}
```

## Function/Class Reference

#### Watcher Class Methods

| Method | Parameters | Returns | Raises/Notes |
|--------|------------|---------|--------------|
| `__init__(roots: str \| list, ignore_patterns: list = None, file_extensions: list = None, max_depth: int = None, history_size: int = 100, event_handler: callable = None)` | `roots` (str/list): Paths to watch.<br>`ignore_patterns` (list[str]): Basename ignores.<br>`file_extensions` (list[str]): Allowed exts (no dot).<br>`max_depth` (int): Recursion limit.<br>`history_size` (int): Max changes stored.<br>`event_handler` (callable): Global callback. | `Watcher`: Instance (starts thread). | Validates roots exist; thread daemon=True. |
| `register_handler(event_type: str, callback: callable)` | `event_type` (str): 'created'/'updated'/'removed'/'all'.<br>`callback` (callable): Takes change dict. | None. | Exceptions in callbacks swallowed. |
| `diff() → list[dict]` | None. | `list[dict]`: Changes (no timestamp). | Updates internal state; filters applied. |
| `get_stats() → dict` | None. | `dict`: {'created': int, ...}. | From history; empty → zeros. |
| `__monitor_loop__(delay: float = 5.0)` | Internal; `delay` (float): Poll interval. | None. | Infinite loop; puts to queue. |
| `__str__() → str` | None. | `str`: "filesystem.Watcher: [roots]". | Debug-friendly. |

#### Standalone Function

| Function | Parameters | Returns | Raises/Notes |
|----------|------------|---------|--------------|
| `get_changes(roots: str \| list, delay: float = 5.0, create_log_file: bool = False, log_filename: str = "FSWatcherLog.log", notifier: callable = None)` | `roots` (str/list): Paths.<br>`delay` (float): Seconds.<br>`create_log_file` (bool): Append to log.<br>`log_filename` (str): Log path.<br>`notifier` (callable): Per-change callback. | None (infinite loop). | Instantiates Watcher; prints/logs; Ctrl+C exit. Uses `file.append_text` for logs. |

**Notes**:

- Filters: Ignores via `in basename`; exts via `splitext`; depth via walk prune.
- Detection: 'updated' on modtime/size diff; no content hash (fast but may miss renames).
- Queue: Use `queue.get_nowait()` in loops; `Empty` on no events.

## Examples

### Basic Watcher with Callbacks

```python
from filesystem import watcher
import filesystem as fs

def on_created(change):
    print(f"New file: {change['abspath']} ({change['size']} bytes)")

def on_all(change):
    print(f"Change: {change['change']} at {change['abspath']}")

w = watcher.Watcher(
    roots=fs.documents,
    ignore_patterns=['.DS_Store'],
    file_extensions=['.txt', '.py'],
    max_depth=2,
    history_size=20
)

w.register_handler('created', on_created)
w.register_handler('all', on_all)

# Manual diff loop (non-threaded)
import time
while True:
    changes = w.diff()
    for change in changes:
        print(f"Detected: {change}")
    w.get_stats()  # Optional: print(w.get_stats())
    time.sleep(10)  # Poll every 10s
```

### Threaded Monitoring with Queue

```python
from filesystem import watcher
from queue import Empty

w = watcher.Watcher(roots='/path/to/project')

# In main thread: Dequeue events
while True:
    try:
        change = w.event_queue.get(timeout=1.0)  # Wait 1s
        print(f"Event: {change['change']} - {change['abspath']}")
    except Empty:
        pass  # No change; continue polling
```

### Standalone with Logging

```python
from filesystem import watcher
import filesystem as fs

def alert(change):
    if change['change'] == 'removed':
        print(f"⚠️ Critical: {change['abspath']} deleted!")

watcher.get_changes(
    roots=[fs.desktop, fs.documents],
    delay=2.0,  # Poll every 2s
    create_log_file=True,
    log_filename=f"{fs.documents}/fs_changes.log",
    notifier=alert
)
# Logs: "/path/to/file.txt was updated at 2025-11-10 19:48:00"
```

### Stats and History Inspection

```python
from filesystem import watcher

w = watcher.Watcher(roots='/tmp/test')
# Simulate changes... (touch files, etc.)

stats = w.get_stats()
print(stats)  # {'created': 3, 'updated': 1, 'removed': 0}

recent = w.change_history[-5:]  # Last 5 changes
for ch in recent:
    print(f"{ch['timestamp']}: {ch['change']} {ch['abspath']}")
```

## Best Practices

- **Polling Tuning**: Short delays (1-2s) for responsiveness; longer (10s+) for battery/CPU savings. Test with `timeit`.
- **Filter Early**: Use `ignore_patterns` for common skips (e.g., VCS dirs); exts for targeted watches.
- **Callback Safety**: Keep handlers lightweight; use queues for heavy processing.
- **Depth Control**: Set `max_depth` for shallow watches (e.g., 1 for top-level only).
- **Error Resilience**: Wrap `diff()` in try-except for transient I/O errors; monitor thread via `thread.is_alive()`.
- **Integration**: Pair with `file` for post-event actions (e.g., checksum on 'updated').
- **Testing**: Mock `os.walk`/`os.stat` in units; simulate changes with temp dirs.
- **Prod Deployment**: Daemonize loop; persist history to JSON via `file` module.

## Limitations

- **Polling Overhead**: Not real-time (misses sub-second changes); high-traffic dirs may lag/CPU-spike.
- **Rename Blindness**: Treats rename as 'removed' + 'created' (no tracking).
- **No Content Diff**: Modtime/size only—edits without changes undetected.
- **Unix Symlinks**: Follows links; potential cycles (no detection).
- **Threading**: Single thread; scales poorly for 100s of roots—extend with multiprocessing.
- **History Memory**: In-RAM only; large `history_size` bloats (serialize manually).
- **No Pause/Stop**: Thread daemon (exits on main); add `stop_event` for graceful shutdown.
- **Windows Paths**: Handles, but long paths (>260) may fail without manifest.

## Contributing

See the root [README.md](https://github.com/hbisneto/FileSystemPro/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., native watchers, debounce) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](https://github.com/hbisneto/FileSystemPro/blob/main/LICENSE) for details.