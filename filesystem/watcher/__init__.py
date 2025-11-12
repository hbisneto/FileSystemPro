# -*- coding: utf-8 -*-
#
# filesystem/watcher/__init__.py
# FileSystemPro
#
# Created by Heitor Bisneto on 12/11/2025.
# Copyright © 2023–2025 hbisneto. All rights reserved.
#
# This file is part of FileSystemPro.
# FileSystemPro is free software: you can redistribute it and/or modify
# it under the terms of the MIT License. See LICENSE for more details.
#

"""
# Watcher

---

## Overview
This module implements a polling-based file system watcher class (`Watcher`) for detecting changes (created, updated, removed) in specified directory roots. It supports multi-root monitoring, customizable filters (ignore patterns, file extensions, recursion depth), event callbacks, change history tracking, and threaded operation for non-blocking polling. A standalone `get_changes` function is also provided for simple logging and notification without instantiating the class.

## Features
- **Multi-Root Monitoring:** Watch single or multiple directory paths simultaneously.
- **Filtering Options:** Ignore files by basename patterns, restrict to specific extensions, and limit recursion depth.
- **Event Handling:** Register callbacks for specific events ('created', 'updated', 'removed') or 'all' changes.
- **Change Detection:** Polling-based diffing of file metadata (modified time, size) to identify changes.
- **History & Stats:** Maintain a configurable history of changes and retrieve statistics (counts per event type).
- **Threaded Polling:** Background monitoring loop with configurable delay to avoid blocking the main thread.
- **Standalone Mode:** Simple function for logging changes to file or notifying via callback without class setup.

## Usage
To use this module, import it and instantiate the `Watcher` class or call the `get_changes` function:

```python
from filesystem import watcher
```

### Examples:

- Initialize and start monitoring a directory with filters:
```python
watcher_instance = watcher.Watcher(
    roots='/path/to/monitor',
    ignore_patterns=['.git', '__pycache__'],
    file_extensions=['py', 'txt'],
    max_depth=3,
    history_size=50
)
```

- Register a callback for updates:

```python
def on_update(change):
    print(f"File updated: {change['abspath']}")

watcher_instance.register_handler('updated', on_update)
```

- Get change statistics:

```python
stats = watcher_instance.get_stats()
print(f"Changes: {stats}")  # e.g., {'created': 2, 'updated': 5, 'removed': 1}
```

- Use standalone monitoring with logging:

```python
watcher.get_changes(
    roots='/path/to/monitor',
    delay=10.0,
    create_log_file=True,
    log_filename='changes.log',
    notifier=lambda change: print(f"Alert: {change['change']} on {change['abspath']}")
)
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
        - roots: Single path or list of paths to monitor.
        - ignore_patterns: List of strings to ignore in basenames.
        - file_extensions: List of allowed extensions (without dot).
        - max_depth: Maximum recursion depth (None for unlimited).
        - history_size: Maximum number of changes to keep in history.
        - event_handler: Optional callback for all events.
        """
        self.roots = roots if isinstance(roots, list) else [roots]
        self.ignore_patterns = ignore_patterns or []
        self.file_extensions = file_extensions or []
        self.max_depth = max_depth
        self.history_size = history_size
        self.change_history = []
        self.handlers = defaultdict(list)
        self.event_queue = Queue()
        self.saved_state = {root: self.__get_state__(root) for root in self.roots}
        if event_handler:
            self.register_handler('all', event_handler)
        self.monitor_thread = threading.Thread(target=self.__monitor_loop__, daemon=True)
        self.monitor_thread.start()

    def __get_metadata__(self, abspath):
        """
        Get file metadata including modified time and size.
        """
        stat = os.stat(abspath)
        return {
            "abspath": abspath,
            "modified": stat.st_mtime,
            "size": stat.st_size,
        }

    def __should_watch__(self, abspath):
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

    def __get_state__(self, path):
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
                if self.__should_watch__(abspath):
                    state[abspath] = self.__get_metadata__(abspath)
        return state

    def register_handler(self, event_type, callback):
        """
        Register a callback for specific event types ('created', 'updated', 'removed') or 'all'.

        ### Parameters:
        - **event_type**: str, the event type.
        - **callback**: callable that takes a change dict.
        """
        self.handlers[event_type].append(callback)

    def __monitor_loop__(self, delay=5.0):
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
        current_states = {root: self.__get_state__(root) for root in self.roots}
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
    - roots: Single path or list of paths.
    - delay: Polling delay in seconds.
    - create_log_file: If True, append changes to log file.
    - log_filename: Log file name.
    - notifier: Optional callback for each change.
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