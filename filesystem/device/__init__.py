# -*- coding: utf-8 -*-
#
# filesystem/device/__init__.py
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
# Device
##### Optional dependency: psutil (install via `pip install psutil` to use this module).

---

## Overview
This module acts as the central hub for accessing system device monitoring functionalities, importing and exposing submodules for detailed insights into disks, CPU, memory, and network. It provides a unified interface to leverage the `psutil` library for cross-platform system resource monitoring.

## Features
- **Disk Management:** Access partition details, storage metrics, I/O counters, boot drive info, and filesystem types.
- **CPU Statistics:** Retrieve usage percentages, time allocations across states, and logical core counts.
- **Memory Monitoring:** Get virtual (RAM) and swap memory stats, including totals, usage, and percentages.
- **Network Insights:** Monitor interfaces, traffic statistics, IP/MAC addresses, and active connections.

## Usage
To use these functions, simply import the module and access the desired submodule:

```python
from filesystem import device
```

### Examples:

- Access disk partitions via the disks submodule:

```python
disks = device.disks
partitions = disks.get_disk_partitions()
print(partitions)
```

- Get CPU usage via the cpu submodule:

```python
cpu = device.cpu
usage = cpu.cpu_percent()
print(f"CPU Usage: {usage}%")
```

- Retrieve virtual memory details via the memory submodule:

```python
memory = device.memory
vm_info = memory.virtual_memory()
print(vm_info)
```

- Get Wi-Fi interface via the network submodule:

```python
network = device.network
wifi_iface = network.get_wifi_interface()
print(f"Wi-Fi Interface: {wifi_iface}")
```
"""

from . import disks
from . import cpu
from . import memory
from . import network