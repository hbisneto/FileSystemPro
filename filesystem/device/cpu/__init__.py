# -*- coding: utf-8 -*-
#
# filesystem/device/cpu/__init__.py
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
# CPU
##### Optional dependency: psutil (install via `pip install psutil` to use this module).

---

## Overview
This module provides functions to retrieve CPU-related information, including current usage percentage, detailed time allocations across CPU states (e.g., user, system, idle), and the total number of logical CPU cores. It leverages the `psutil` library for cross-platform CPU monitoring.

## Features
- **CPU Usage Monitoring:** Retrieve the overall CPU utilization as a percentage of total capacity.
- **CPU Time Details:** Get comprehensive breakdowns of time spent in user mode, system mode, idle, I/O wait, and other states.
- **Core Count:** Determine the number of logical CPU cores available in the system.

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import device
cpu = device.cpu
```

### Examples:

- Get current CPU usage percentage:

```python
cpu_usage = cpu.cpu_percent()
print(f"CPU Usage: {cpu_usage}%")
```

- Get CPU times information:

```python
cpu_times_info = cpu.cpu_times()
print(cpu_times_info)
```

- Get number of logical CPU cores:

```python
num_cores = cpu.cpu_count()
print(f"Number of CPU Cores: {num_cores}")
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
            "The module CPU requires the 'psutil' library. "
            "Please install it via: pip install psutil"
        )

def cpu_percent():
    """
    # cpu.cpu_percent()

    ---

    ### Overview

    Retrieves the system's CPU usage percentage. This function uses the `psutil.cpu_percent()` method to get the current CPU usage as a percentage.

    ### Parameters:
    - **None**

    ### Returns:
    - **float:** The CPU usage percentage.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves the system's current CPU usage percentage.

    ```python
    cpu_usage = cpu_percent()
    print(cpu_usage)
    ```
    """
    __require_psutil__()
    return __psutil__.cpu_percent()

def cpu_times():
    """
    # cpu.cpu_times()

    ---

    ### Overview

    Retrieves CPU times for the system. This function uses the `psutil.cpu_times()` method to get the amount of time the CPU has spent in various states such as user, system, idle, etc.

    ### Parameters:
    - **None**

    ### Returns:
    - **psutil._pslinux.scputimes:** An object containing the CPU times for the various states.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves the system's CPU times.

    ```python
    cpu_times_info = cpu_times()
    print(cpu_times_info)
    ```
    """
    __require_psutil__()
    return __psutil__.cpu_times()

def cpu_count():
    """
    # cpu.cpu_count()

    ---

    ### Overview

    Retrieves the number of CPU cores in the system. This function uses the `psutil.cpu_count()` method to get the total number of logical CPU cores available.

    ### Parameters:
    - **None**

    ### Returns:
    - **int:** The number of logical CPU cores.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves the number of logical CPU cores in the system.

    ```python
    num_cores = cpu_count()
    print(num_cores)
    ```
    """
    __require_psutil__()
    return __psutil__.cpu_count()