"""
# Device

---

## Overview

The Device module provides a comprehensive set of functionalities for managing and retrieving various device-related information and metrics. This module is divided into two main parts: CPU Information and Disks Information. It leverages the `psutil` library to gather details efficiently and offers a wide range of functionalities for system monitoring and management tasks.

## Features

### CPU Information

The CPU Information part of the module provides functionalities for retrieving various CPU-related information, such as CPU usage percentage, CPU times, and the number of CPU cores. It offers essential metrics for monitoring CPU performance.

#### Functions:

1. **cpu_percent**
   - **Returns:** float - The CPU usage percentage.

2. **cpu_times**
   - **Returns:** psutil._pslinux.scputimes - An object containing the CPU times for the various states.

3. **cpu_count**
   - **Returns:** int - The number of logical CPU cores.

### Disks Information

The Disks Information part of the module provides functionalities for retrieving various disk-related information and metrics, such as disk partitions, boot drive names, filesystem types, and storage metrics. It also includes filtering capabilities to narrow down the information based on specific criteria.

#### Disk Information

1. **current_disk_filesystem_name**
   - **Returns:** str - The filesystem type of the current disk.

2. **boot_time**
   - **Returns:** str - The boot time in the format `day/month/year hour:minute:second`.

3. **get_disk_partitions**
   - **Returns:** list - A list of dictionaries, each containing the attributes of a mounted disk partition.

4. **get_boot_drive_name**
   - **Returns:** str - The name of the boot drive on macOS. If the function is called on a non-macOS platform, it returns "NOT IMPLEMENTED".

5. **get_disk_partition_filteredby_device**
   - **Returns:** list - A list of dictionaries, each containing the attributes of a disk partition that matches the specified device filter.

6. **get_disk_partition_filteredby_fstype**
   - **Returns:** list - A list of dictionaries, each containing the attributes of a disk partition that matches the specified filesystem type filter.

7. **get_disk_partition_filteredby_mountpoint**
   - **Returns:** list - A list of dictionaries, each containing the attributes of a disk partition that matches the specified mount point filter.

8. **get_disk_partition_filteredby_opts**
   - **Returns:** list - A list of dictionaries, each containing the attributes of a disk partition that matches the specified options filter.

#### Disk Usage

1. **storage_metrics**
   - **Returns:** dict - A dictionary containing storage metrics for a specific mount point.

2. **disk_info**
   - **Returns:** dict - A dictionary where each key is an index and each value is a tuple containing the attributes of a disk partition.

3. **disk_io_counters**
   - **Returns:** dict - A dictionary where each key is a disk name and each value is an object containing disk I/O statistics.

## Detailed Functionality

The module's functions are designed to be robust and easy to use, providing a high level of abstraction from the underlying device operations.

### CPU Information

The CPU Information part of the module provides essential metrics for monitoring CPU performance, including CPU usage percentage, CPU times for various states, and the number of logical CPU cores.

### Disks Information

The Disks Information part of the module provides comprehensive details about disk partitions, including devices, filesystem types, mount points, and options. It also offers storage metrics and disk I/O statistics, with filtering capabilities to narrow down the information based on specific criteria.

## Usage

To use the functions provided by this module, import the module and call the desired function with the appropriate parameters:

```python
from filesystem import device
```
"""

from . import disks
from . import cpu