"""
# CPU

---

## Overview

The CPU module provides functionalities for retrieving CPU-related information such as CPU usage percentage, CPU times, and the number of CPU cores. It leverages the `psutil` library to gather these details efficiently.

The CPU module is designed to provide essential CPU-related information for system monitoring and management tasks. 
By utilizing the `psutil` library, it ensures accurate and efficient retrieval of CPU metrics.
"""

import psutil

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
    return psutil.cpu_percent()

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
    return psutil.cpu_times()

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
    return psutil.cpu_count()