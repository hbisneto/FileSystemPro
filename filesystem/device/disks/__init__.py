# -*- coding: utf-8 -*-
#
# filesystem/device/disks/__init__.py
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
# Disks
##### Optional dependency: psutil (install via `pip install psutil` to use this module).

---

## Overview
This module provides functions to retrieve disk-related information, including mounted partitions, storage usage metrics, I/O statistics, boot time, and boot drive details. It leverages the `psutil` library for cross-platform disk monitoring and platform-specific commands for boot drive naming.

## Features
- **Disk Partitions:** Retrieve all mounted partitions and filter them by device, filesystem type, mount point, or options.
- **Storage Metrics:** Get total, free, used space, and usage percentages for specific mount points.
- **Comprehensive Disk Info:** Aggregate partition details with storage usage across all disks.
- **Disk I/O Counters:** Monitor read/write operations, bytes transferred, and time spent on I/O for each disk.
- **System Boot Details:** Fetch boot time in human-readable format and the name of the boot drive.
- **Filesystem Detection:** Identify the filesystem type of the current boot disk.

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import device
disks = device.disks
```

### Examples:

- Get all disk partitions:

```python
partitions = disks.get_disk_partitions()
print(partitions)
```

- Get comprehensive disk information:

```python
disk_info = disks.disk_info()
print(disk_info)
```

- Get boot time:

```python
boot_time_str = disks.boot_time()
print(f"Boot Time: {boot_time_str}")
```

- Get disk I/O counters:

```python
io_counters = disks.disk_io_counters()
print(io_counters)
```

- Filter partitions by filesystem type:

```python
ext4_partitions = disks.get_disk_partition_filteredby_fstype('ext4')
print(ext4_partitions)
```

- Get storage metrics for a mount point:

```python
metrics = disks.storage_metrics('/')
print(f"Total: {metrics[0]} bytes, Used: {metrics[2]} bytes ({metrics[4]}%)")
```
"""

from datetime import datetime
import subprocess
from sys import platform as PLATFORM

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
            "The module Disks requires the 'psutil' library. "
            "Please install it via: pip install psutil"
        )

def current_disk_filesystem_name():
    """
    # disks.current_disk_filesystem_name()

    ---

    ### Overview

    Retrieves the filesystem type of the current disk. This function checks the disk partitions and returns the filesystem type of the partition mounted at 'C:/' (for Windows) or '/' (for Unix-like systems).

    ### Parameters:
    - **None**

    ### Returns:
    - **str:** The filesystem type of the current disk.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves the filesystem type of the current disk.

    ```python
    filesystem_type = current_disk_filesystem_name()
    print(filesystem_type)
    ```
    """
    __require_psutil__()
    dskpart = __psutil__.disk_partitions()
    fstypes = [part.fstype for part in dskpart if part.mountpoint in ['C:\\', '/']]
    
    return fstypes[0]

def boot_time():
    """
    # disks.boot_time()

    ---

    ### Overview

    Retrieves the system's boot time. This function uses the `psutil.boot_time()` method to get the boot time as a timestamp and then converts it to a human-readable format.

    ### Parameters:
    - **None**

    ### Returns:
    - **str:** The boot time in the format `day/month/year hour:minute:second`.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves the system's boot time.

    ```python
    boot_time_str = boot_time()
    print(boot_time_str)
    ```
    """
    __require_psutil__()
    boot_time_timestamp = __psutil__.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    return f'{bt.day}/{bt.month}/{bt.year} {bt.hour}:{bt.minute}:{bt.second}'

######################################## DISK INFORMATION ########################################

### DISK PARTITIONS
def get_disk_partitions():
    """
    # disks.get_disk_partitions()

    ---

    ### Overview

    Retrieves a list of all mounted disk partitions and their attributes. This function converts the partition details into dictionary format for easier access and manipulation.

    ### Parameters:
    - **None**

    ### Returns:
    - **list:** A list of dictionaries, each containing the attributes of a mounted disk partition.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves the list of all mounted disk partitions.

    ```python
    partitions = get_disk_partitions()
    print(partitions)
    ```
    """
    __require_psutil__()
    var = __psutil__.disk_partitions()
    output = [part._asdict() for part in var]
    return output

def get_boot_drive_name():
    """
    # disks.get_boot_drive_name()

    ---

    ### Overview

    Retrieves the name of the boot drive.

    ### Parameters:
    - **None**

    ### Returns:
    - **str:** The name of the boot drive.

    ### Raises:
    - **Exception:** If an error occurs during the subprocess call, it returns "Unsupported platform: _platform_name_".

    ### Examples:
    - Retrieves the name of the boot drive on macOS.

    ```python
    boot_drive_name = get_boot_drive_name()
    print(boot_drive_name)
    ```
    """
    if PLATFORM == "darwin":
        try:
            cmd = "python -c \"from Foundation import NSFileManager; print(NSFileManager.defaultManager().displayNameAtPath_('/'))\""
            startup_drive_name = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            return startup_drive_name
        except Exception as e:
            return str(e)
    elif PLATFORM == "win32" or PLATFORM == "win64":
        try:
            cmd = "wmic logicaldisk where \"DeviceID='C:'\" get VolumeName"
            startup_drive_name = subprocess.check_output(cmd, shell=True).decode("utf-8").strip().split("\n")[1].strip()
            return startup_drive_name
        except Exception as e:
            return str(e)
    elif PLATFORM == "linux" or PLATFORM == "linux2":
        try:
            cmd = "lsblk -o MOUNTPOINT,LABEL | grep -E '^/ +'"
            startup_drive_name = subprocess.check_output(cmd, shell=True).decode("utf-8").strip().split(" ")[-1]
            return startup_drive_name
        except Exception as e:
            return str(e)
    else:
        raise Exception(f"Unsupported platform: {PLATFORM}")

def get_disk_partition_filteredby_device(filter):
    """
    # disks.get_disk_partition_filteredby_device(filter)

    ---

    ### Overview

    Filters and retrieves disk partitions based on the specified device. This function compares the device attribute of each partition with the provided filter and returns a list of matching partitions.

    ### Parameters:
    - **filter (str):** The device name to filter the disk partitions by.

    ### Returns:
    - **list:** A list of dictionaries, each containing the attributes of a disk partition that matches the specified device filter.

    ### Raises:
    - **None**

    ### Examples:
    - Filters disk partitions by the device name `sda1`.

    ```python
    partitions = get_disk_partition_filteredby_device('sda1')
    print(partitions)
    ```
    """
    __require_psutil__()
    var = get_disk_partitions()
    out_filter = filter.lower()
    output = [d for d in var if d['device'] == out_filter]
    return output

def get_disk_partition_filteredby_fstype(filter):
    """
    # disks.get_disk_partition_filteredby_fstype(filter)

    ---

    ### Overview

    Filters and retrieves disk partitions based on the specified filesystem type. This function compares the filesystem type attribute of each partition with the provided filter and returns a list of matching partitions.

    ### Parameters:
    - **filter (str):** The filesystem type to filter the disk partitions by.

    ### Returns:
    - **list:** A list of dictionaries, each containing the attributes of a disk partition that matches the specified filesystem type filter.

    ### Raises:
    - **None**

    ### Examples:
    - Filters disk partitions by the filesystem type `ext4`.

    ```python
    partitions = get_disk_partition_filteredby_fstype('ext4')
    print(partitions)
    ```
    """
    __require_psutil__()
    var = get_disk_partitions()
    out_filter = filter.lower()
    output = [d for d in var if d['fstype'] == out_filter]
    return output

def get_disk_partition_filteredby_mountpoint(filter):
    """
    # disks.get_disk_partition_filteredby_mountpoint(filter)

    ---

    ### Overview

    Filters and retrieves disk partitions based on the specified mount point. This function compares the mount point attribute of each partition with the provided filter and returns a list of matching partitions.

    ### Parameters:
    - **filter (str):** The mount point to filter the disk partitions by.

    ### Returns:
    - **list:** A list of dictionaries, each containing the attributes of a disk partition that matches the specified mount point filter.

    ### Raises:
    - **None**

    ### Examples:
    - Filters disk partitions by the mount point `/mnt/data`.

    ```python
    partitions = get_disk_partition_filteredby_mountpoint('/mnt/data')
    print(partitions)
    ```
    """
    __require_psutil__()
    var = get_disk_partitions()
    output = [d for d in var if d['mountpoint'] == filter]
    return output

def get_disk_partition_filteredby_opts(filter):
    """
    # disks.get_disk_partition_filteredby_opts(filter)

    ---

    ### Overview

    Filters and retrieves disk partitions based on the specified options. This function compares the options attribute of each partition with the provided filter and returns a list of matching partitions.

    ### Parameters:
    - **filter (str):** The options to filter the disk partitions by.

    ### Returns:
    - **list:** A list of dictionaries, each containing the attributes of a disk partition that matches the specified options filter.

    ### Raises:
    - **None**

    ### Examples:
    - Filters disk partitions by the options `rw`.

    ```python
    partitions = get_disk_partition_filteredby_opts('rw')
    print(partitions)
    ```
    """
    __require_psutil__()
    var = get_disk_partitions()
    out_filter = filter.lower()
    output = [d for d in var if d['opts'] == out_filter]
    return output

######################################## DISK USAGE ########################################

def storage_metrics(mountpoint):
    """
    # disk.storage_metrics(mountpoint)

    ---

    ### Overview

    Returns storage metrics for a specific mount point, including total, free, and used storage, as well as the percentage of free and used storage.

    ### Parameters:
    - **mountpoint (str):** The path of the mount point to get storage metrics for.

    ### Returns:
    - **dict:** A dictionary containing storage metrics:
    - `0`: Total storage.
    - `1`: Free storage.
    - `2`: Used storage.
    - `3`: Percentage of free storage.
    - `4`: Percentage of used storage.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves storage metrics for the root mount point.

    ```python
    storage_metrics('/')
    ```
    """
    __require_psutil__()
    var = __psutil__.disk_usage(mountpoint)
    total = var.total
    free = var.free
    used = var.used
    percent_free = var.percent
    percent_used = 100 - float(var.percent)

    metrics_list = {
        0 : total,
        1 : free, 
        2 : used,
        3 : percent_free, 
        4 : percent_used
    }
    return metrics_list

def disk_info():
    """
    # disks.disk_info()

    ---

    ### Overview

    Retrieves comprehensive information about the system's disk partitions, including devices, filesystem types, mount points, options, and storage metrics. This function consolidates data from multiple helper functions to provide detailed disk information.

    ### Parameters:
    - **None**

    ### Returns:
    - **dict:** A dictionary where each key is an index and each value is a tuple containing the attributes of a disk partition:
    - Mount point
    - Device
    - Filesystem type
    - Options
    - Total storage
    - Used storage
    - Free storage
    - Percentage of used storage
    - Percentage of free storage

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves detailed information about the system's disk partitions.

    ```python
    disk_information = disk_info()
    print(disk_information)
    ```
    """
    def __get_disk_device_list__():
        """
        # disks.__get_disk_device_list__()

        ---

        ### Overview

        Retrieves a list of all disk devices from the system's disk partitions. This function processes the partitions and extracts the device attribute from each partition to create a list of disk devices.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of disk devices.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of all disk devices.

        ```python
        device_list = __get_disk_device_list__()
        print(device_list)
        ```
        """
        var = get_disk_partitions()
        data_list = []
        for data in var:
            data_list.append(data)
        devices = [item['device'] for item in data_list]
        return devices

    def __get_disk_filesystem_list__():
        """
        # disks.__get_disk_filesystem_list__()

        ---

        ### Overview

        Retrieves a list of all filesystem types from the system's disk partitions. This function processes the partitions and extracts the filesystem type attribute from each partition to create a list of filesystem types.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of filesystem types.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of all filesystem types.

        ```python
        fstypes = __get_disk_filesystem_list__()
        print(fstypes)
        ```
        """
        var = get_disk_partitions()
        data_list = []
        for data in var:
            data_list.append(data)
        fstype = [item['fstype'] for item in data_list]
        return fstype

    def __get_disk_mountpoint_list__():
        """
        # disks.__get_disk_mountpoint_list__()

        ---

        ### Overview

        Retrieves a list of all mount points from the system's disk partitions. This function processes the partitions and extracts the mount point attribute from each partition to create a list of mount points.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of mount points.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of all mount points.

        ```python
        mountpoints = __get_disk_mountpoint_list__()
        print(mountpoints)
        ```
        """
        var = get_disk_partitions()
        data_list = []
        for data in var:
            data_list.append(data)
        mountpoints = [item['mountpoint'] for item in data_list]
        return mountpoints

    def __get_disk_opts_list__():
        """
        # disks.__get_disk_opts_list__()

        ---

        ### Overview

        Retrieves a list of all options from the system's disk partitions. This function processes the partitions and extracts the options attribute from each partition to create a list of options.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of options.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of all options.

        ```python
        opts = __get_disk_opts_list__()
        print(opts)
        ```
        """
        var = get_disk_partitions()
        data_list = []
        for data in var:
            data_list.append(data)
        opts = [item['opts'] for item in data_list]
        return opts

    def __get_disk_total_usage_list__():
        """
        # disks.__get_disk_total_usage_list__()

        ---

        ### Overview

        Retrieves a list of total storage usage for all disk partitions. This function processes the list of mount points, calculates the total storage for each partition using the `storage_metrics` function, and returns a list of total storage values.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of total storage values for each disk partition.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of total storage usage for all disk partitions.

        ```python
        total_usage = __get_disk_total_usage_list__()
        print(total_usage)
        ```
        """
        var = __get_disk_mountpoint_list__()
        total_list = []
        for disk in var:
            metrics = storage_metrics(disk)
            total_list.append(metrics[0])
        return total_list

    def __get_disk_free_usage_list__():
        """
        # disks.__get_disk_free_usage_list__()

        ---

        ### Overview

        Retrieves a list of free storage usage for all disk partitions. This function processes the list of mount points, calculates the free storage for each partition using the `storage_metrics` function, and returns a list of free storage values.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of free storage values for each disk partition.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of free storage usage for all disk partitions.

        ```python
        free_usage = __get_disk_free_usage_list__()
        print(free_usage)
        ```
        """
        var = __get_disk_mountpoint_list__()
        free_list = []
        for disk in var:
            metrics = storage_metrics(disk)
            free_list.append(metrics[1])
        return free_list

    def __get_disk_used_usage_list__():
        """
        # disks.__get_disk_used_usage_list__()

        ---

        ### Overview

        Retrieves a list of used storage usage for all disk partitions. This function processes the list of mount points, calculates the used storage for each partition using the `storage_metrics` function, and returns a list of used storage values.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of used storage values for each disk partition.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of used storage usage for all disk partitions.

        ```python
        used_usage = __get_disk_used_usage_list__()
        print(used_usage)
        ```
        """
        var = __get_disk_mountpoint_list__()
        used_list = []
        for disk in var:
            metrics = storage_metrics(disk)
            used_list.append(metrics[2])
        return used_list

    def __get_disk_free_percent_usage_list__():
        """
        # disks.__get_disk_free_percent_usage_list__()

        ---

        ### Overview

        Retrieves a list of free storage percentage usage for all disk partitions. This function processes the list of mount points, calculates the percentage of free storage for each partition using the `storage_metrics` function, and returns a list of free storage percentages.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of free storage percentages for each disk partition.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of free storage percentage usage for all disk partitions.

        ```python
        free_percent_usage = __get_disk_free_percent_usage_list__()
        print(free_percent_usage)
        ```
        """
        var = __get_disk_mountpoint_list__()
        free_percent_list = []
        for disk in var:
            metrics = storage_metrics(disk)
            free_percent_list.append(metrics[3])
        return free_percent_list

    def __get_disk_used_percent_usage_list__():
        """
        # disks.__get_disk_used_percent_usage_list__()

        ---

        ### Overview

        Retrieves a list of used storage percentage usage for all disk partitions. This function processes the list of mount points, calculates the percentage of used storage for each partition using the `storage_metrics` function, and returns a list of used storage percentages.

        ### Parameters:
        - **None**

        ### Returns:
        - **list:** A list of used storage percentages for each disk partition.

        ### Raises:
        - **None**

        ### Examples:
        - Retrieves the list of used storage percentage usage for all disk partitions.

        ```python
        used_percent_usage = __get_disk_used_percent_usage_list__()
        print(used_percent_usage)
        ```
        """
        var = __get_disk_mountpoint_list__()
        used_percent_list = []
        for disk in var:
            metrics = storage_metrics(disk)
            used_percent_list.append(metrics[4])
        return used_percent_list

    __require_psutil__()
    devices = __get_disk_device_list__()
    filesystems = __get_disk_filesystem_list__()
    mountpoint = __get_disk_mountpoint_list__()
    opts = __get_disk_opts_list__()
    total = __get_disk_total_usage_list__()
    used = __get_disk_used_usage_list__()
    free = __get_disk_free_usage_list__()
    percent_used = __get_disk_used_percent_usage_list__()
    percent_free = __get_disk_free_percent_usage_list__()
    
    disk_info = {i: info for i, info in enumerate(
        zip(mountpoint, devices, filesystems,
            opts, total, used, free, percent_used, percent_free)
            )
    }
    return disk_info

def disk_io_counters():
    """
    # disks.disk_io_counters()

    ---

    ### Overview

    Retrieves disk I/O statistics for each disk in the system. This function utilizes the `psutil.disk_io_counters` method to gather I/O counters for each disk, including the number of read and write operations, the number of bytes read and written, and the time spent reading and writing.

    ### Parameters:
    - **None**

    ### Returns:
    - **dict:** A dictionary where each key is a disk name and each value is an object containing disk I/O statistics.

    ### Raises:
    - **None**

    ### Examples:
    - Retrieves disk I/O statistics for all disks.

    ```python
    io_counters = disk_io_counters()
    print(io_counters)
    ```
    """
    __require_psutil__()
    disk_io = __psutil__.disk_io_counters(perdisk=True)
    return disk_io

######################################## DISK INFORMATION ########################################

drive_name = get_boot_drive_name()
"""
This variable stores the name of the boot drive on the current platform.

- On macOS, the function uses a subprocess call to the Foundation framework to obtain the display name of the boot drive.
- On Windows, it returns the name of the boot drive.
- On Linux, it returns the name of the boot drive.

If the function is called on an unsupported platform, it returns "Unsupported platform: _platform_name_".
"""
