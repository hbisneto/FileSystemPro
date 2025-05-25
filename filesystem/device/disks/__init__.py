"""
# Disks

---

## Overview

The Disks module provides a comprehensive set of functionalities for managing and retrieving various disk-related information and metrics. This module is divided into two main parts: Disk Information and Disk Usage. It leverages the `psutil` library to gather details efficiently and offers filtering capabilities to narrow down the information based on specific criteria.

### Disk Information

The Disk Information part of the module provides functionalities for retrieving various disk-related information, such as disk partitions, boot drive names, and filesystem types. It offers filtering capabilities to narrow down the information based on specific criteria.

#### Functions:

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

### Disk Usage

The Disk Usage part of the module provides functionalities for retrieving various disk usage metrics, such as total, free, and used storage, as well as the percentage of free and used storage. It also includes functions for retrieving comprehensive information about the system's disk partitions and disk I/O counters.

#### Functions:

1. **storage_metrics**
   - **Returns:** dict - A dictionary containing storage metrics for a specific mount point.

2. **disk_info**
   - **Returns:** dict - A dictionary where each key is an index and each value is a tuple containing the attributes of a disk partition.

3. **disk_io_counters**
   - **Returns:** dict - A dictionary where each key is a disk name and each value is an object containing disk I/O statistics.

The Disks module is designed to provide essential disk-related information and usage metrics for system monitoring and management tasks. By utilizing the `psutil` library, it ensures accurate and efficient retrieval of disk metrics and attributes.
"""

import psutil
from datetime import datetime
import subprocess
from sys import platform as PLATFORM

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
    dskpart = psutil.disk_partitions()
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
    boot_time_timestamp = psutil.boot_time()
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
    var = psutil.disk_partitions()
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
            cmd = "lsblk -o MOUNTPOINT,LABEL | grep '/'"
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
    var = psutil.disk_usage(mountpoint)
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
    disk_io = psutil.disk_io_counters(perdisk=True)
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
