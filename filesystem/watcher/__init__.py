"""
# Watcher

---

## Overview
The Watcher module is a part of the FileSystemPro library that provides file monitoring capabilities.
It is designed to track changes within a specified directory, 
alerting users to any modifications, creations, or deletions of files.

## Features
- `Real-Time Monitoring:` Continuously monitors a directory for any file changes.
- `Change Detection:` Identifies updated, created, or removed files since the last check.
- `State Preservation:` Maintains a record of the directory's state for comparison.

## How It Works
The `Watcher` class within the module is initialized with a root directory to monitor. 
It uses the `get_state` method to create a snapshot of the current state of the directory, 
mapping absolute file paths to their metadata.

### State Tracking
Upon initialization, `Watcher` stores the state of the directory. 
The `diff` method compares the current state with the saved state to detect any changes. 
It categorizes changes into three types:
- `Updated:` Files that have been modified since the last state.
- `Created:` New files that have been added to the directory.
- `Removed:` Files that have been deleted from the directory.

### Results
The `diff` method returns a list of changes,
with each entry containing the file's path and the type of change. 
This allows for easy integration with other systems that may need to respond to file system events.

## Usage
To use the `Watcher` module, instantiate the `Watcher` class with the directory you wish to monitor:

```python
from filesystem import watcher as wat
watcher = wat('/path/to/directory')
```
"""
import time
from datetime import datetime
import os
import threading
from queue import Queue, Empty
from collections import defaultdict
from filesystem import file as fsfile

class Watcher(object):
    """
    Watcher Class - Advanced Version with multi-root support, filters, history, callbacks, and threaded polling.
    """
    def __init__(self, roots, ignore_patterns=None, file_extensions=None, max_depth=None, history_size=100, event_handler=None):
        """
        Initialize Watcher with multiple roots, filters, etc.
        :param roots: Single path or list of paths to monitor.
        :param ignore_patterns: List of strings to ignore in basenames.
        :param file_extensions: List of allowed extensions (without dot).
        :param max_depth: Maximum recursion depth (None for unlimited).
        :param history_size: Maximum number of changes to keep in history.
        :param event_handler: Optional callback for all events.
        """
        self.roots = roots if isinstance(roots, list) else [roots]
        self.ignore_patterns = ignore_patterns or []
        self.file_extensions = file_extensions or []
        self.max_depth = max_depth
        self.history_size = history_size
        self.change_history = []
        self.handlers = defaultdict(list)
        self.event_queue = Queue()
        self.saved_state = {root: self._get_state(root) for root in self.roots}
        if event_handler:
            self.register_handler('all', event_handler)
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def _get_metadata(self, abspath):
        """
        Get file metadata including modified time and size.
        """
        stat = os.stat(abspath)
        return {
            "abspath": abspath,
            "modified": stat.st_mtime,
            "size": stat.st_size,
        }

    def _should_watch(self, abspath):
        """
        Check if file should be monitored based on filters.
        """
        basename = os.path.basename(abspath)
        if any(pat in basename for pat in self.ignore_patterns):
            return False
        _, ext = os.path.splitext(abspath)
        ext = ext.lstrip('.')
        if self.file_extensions and ext not in self.file_extensions:
            return False
        return True

    def _get_state(self, path):
        """
        Get dictionary of file paths to metadata, respecting filters and depth.
        """
        state = {}
        for root_dir, dirs, files in os.walk(path):
            depth = root_dir.replace(path, '').count(os.sep)
            if self.max_depth is not None and depth > self.max_depth:
                dirs[:] = []
                continue
            for filename in files:
                abspath = os.path.join(root_dir, filename)
                if self._should_watch(abspath):
                    state[abspath] = self._get_metadata(abspath)
        return state

    def register_handler(self, event_type, callback):
        """
        Register a callback for specific event types ('created', 'updated', 'removed') or 'all'.

        ### Parameters:
        - **event_type**: str, the event type.
        - **callback**: callable that takes a change dict.
        """
        self.handlers[event_type].append(callback)

    def _monitor_loop(self, delay=5.0):
        """
        Internal threaded loop for polling changes.
        """
        while True:
            changes = self.diff()
            if changes:
                for change in changes:
                    self.event_queue.put(change)
                    for cb in self.handlers.get(change['change'], []):
                        try:
                            cb(change)
                        except Exception:
                            pass
                    for cb in self.handlers.get('all', []):
                        try:
                            cb(change)
                        except Exception:
                            pass
            time.sleep(delay)

    def diff(self):
        """
        Detect changes across all roots and update state.
        Returns list of change dicts.
        """
        current_states = {root: self._get_state(root) for root in self.roots}
        all_changes = []
        now = datetime.now()
        for root in self.roots:
            current_state = current_states[root]
            saved_state = self.saved_state[root]
            changed_paths = [k for k, v1 in current_state.items() 
                             if k in saved_state and v1["modified"] != saved_state[k]["modified"]]
            current_set = set(current_state.keys())
            stored_set = set(saved_state.keys())
            created = current_set - stored_set
            removed = stored_set - current_set
            results = []
            for x in changed_paths:
                i = current_state[x].copy()
                i["change"] = "updated"
                results.append(i)
            for x in created:
                i = current_state[x].copy()
                i["change"] = "created"
                results.append(i)
            for x in removed:
                i = saved_state[x].copy()
                i["change"] = "removed"
                results.append(i)
            all_changes.extend(results)
            self.saved_state[root] = current_state
        # Update history
        for change in all_changes:
            change_copy = change.copy()
            change_copy['timestamp'] = now
            self.change_history.append(change_copy)
            if len(self.change_history) > self.history_size:
                self.change_history.pop(0)
        return all_changes

    def get_stats(self):
        """
        Get change statistics from history.
        Returns dict with counts for each change type.
        """
        if not self.change_history:
            return {'created': 0, 'updated': 0, 'removed': 0}
        return {t: sum(1 for c in self.change_history if c['change'] == t) 
                for t in ['created', 'updated', 'removed']}

    def __str__(self):
        """
        String representation.
        """
        return f"filesystem.Watcher: {self.roots}"

def get_changes(roots, delay=5.0, create_log_file=False, log_filename="FSWatcherLog.log", notifier=None):
    """
    Standalone monitoring function using the watcher's event queue.
    :param roots: Single path or list of paths.
    :param delay: Polling delay in seconds.
    :param create_log_file: If True, append changes to log file.
    :param log_filename: Log file name.
    :param notifier: Optional callback for each change.
    """
    if isinstance(roots, str):
        roots = [roots]
    watcher = Watcher(roots)
    while True:
        try:
            while True:
                change = watcher.event_queue.get_nowait()
                print(f"Change detected at: {change['timestamp']}: {change['abspath']} was {change['change']}")
                if create_log_file:
                    fsfile.append_text(log_filename, text=f"{change['abspath']} was {change['change']} at {change['timestamp']}")
                if notifier:
                    notifier(change)
        except Empty:
            pass
        time.sleep(delay)