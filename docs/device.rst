.. _device-module:

Device Module
=============

The Device module includes powerful tools for managing and retrieving detailed information about your system's disks and CPU, enhancing productivity and ensuring efficient system management in applications.

Features
--------

- **Boot Time**: Provides the system's boot time.
- **Current Disk Filesystem Name**: Returns the name of the current disk filesystem.
- **Disk Info**: Displays detailed information about the disks.
- **Disk I/O Counters**: Returns disk I/O counters.
- **Disk Partitions**: Retrieves disk partitions.
- **Boot Drive Name**: Returns the name of the boot drive.
- **Filter by Device**: Filters disk partitions based on the device.
- **Filter by Filesystem Type**: Filters disk partitions based on filesystem type.
- **Filter by Mount Point**: Filters disk partitions based on the mount point.
- **Filter by Options**: Filters disk partitions based on options.
- **Storage Metrics**: Provides storage metrics for a specific mount point.
- **CPU Usage Percentage**: Returns the CPU usage percentage.
- **CPU Usage Times**: Provides CPU usage times.
- **CPU Count**: Returns the number of CPUs (logical cores) available in the system.

Disks
-----

The Disks section of the Device module provides powerful tools for managing and retrieving detailed information about disk partitions, boot drive names, filesystem types, and storage metrics. It enhances productivity by simplifying disk management and ensuring efficient retrieval of disk-related information.

.. automodule:: filesystem.device.disks
   :members:
   :undoc-members:
   :show-inheritance:

CPU
---

The CPU section of the Device module offers essential metrics and functionalities for monitoring CPU performance, including CPU usage percentage, CPU times, and the number of CPU cores. It empowers developers to efficiently manage and optimize CPU usage within their applications.

.. automodule:: filesystem.device.cpu
   :members:
   :undoc-members:
   :show-inheritance: