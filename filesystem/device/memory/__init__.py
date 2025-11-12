# -*- coding: utf-8 -*-
#
# filesystem/device/memory/__init__.py
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
# Memory
##### Optional dependency: psutil (install via `pip install psutil` to use this module).

---

## Overview
This module provides functions to retrieve detailed information about the system's virtual memory (RAM) and swap memory usage. It leverages the `psutil` library to access comprehensive memory statistics, including totals, usage breakdowns, percentages, and specific metrics like active/inactive pages for virtual memory, and swap-ins/outs for swap space.

## Features
- **Virtual Memory Details:** Retrieve full virtual memory stats or specific values like total, available, used, free, percent used, active, inactive, buffers, cached, shared, and slab.
- **Swap Memory Details:** Retrieve full swap memory stats or specific values like total, used, free, percent used, pages swapped in (sin), and pages swapped out (sout).

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import device
memory = device.memory
```

### Examples:

- Get virtual memory percentage used:

```python
percent_used = memory.percent_virtual_memory()
print(f"Virtual Memory Used: {percent_used}%")
```

- Get total virtual memory:

```python
total_vm = memory.total_virtual_memory()
print(f"Total Virtual Memory: {total_vm} bytes")
```

- Get swap memory details:

```python
swap_info = memory.swap_memory()
print(swap_info)
```

- Get used swap memory:

```python
used_swap = memory.used_swap_memory()
print(f"Used Swap: {used_swap} bytes")
```
"""

__PSUTIL_AVAILABLE__ = False
try:
    import psutil as __psutil__
    __PSUTIL_AVAILABLE__ = True
except ImportError:
    psutil = None

def __require_psutil__():
    """Internal helper function to check and raise error if psutil is not available."""
    if not __PSUTIL_AVAILABLE__:
        raise ImportError(
            "The module Memory requires the 'psutil' library. "
            "Please install it via: pip install psutil"
        )

# VIRTUAL MEMORY
def virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory()

def total_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().total

def available_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().available

def percent_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().percent

def used_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().used

def free_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().free

def active_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().active

def inactive_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().inactive

def buffers_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().buffers

def cached_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().cached

def shared_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().shared

def slab_virtual_memory():
    __require_psutil__()
    return __psutil__.virtual_memory().slab

# SWAP MEMORY
def swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory()

def total_swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory().total

def used_swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory().used

def free_swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory().free

def percent_swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory().percent

def sin_swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory().sin

def sout_swap_memory():
    __require_psutil__()
    return __psutil__.swap_memory().sout