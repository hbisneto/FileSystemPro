# -*- coding: utf-8 -*-
#
# filesystem/device/network/__init__.py
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
# Network
##### Optional dependency: psutil (install via `pip install psutil` to use this module).

---

## Overview
This module provides functions to retrieve network interface information, including Wi-Fi and Ethernet statistics, IP addresses, MAC addresses, and active TCP connections. It leverages the `psutil` library to monitor network activity across interfaces and system-wide totals.

## Features
- **Wi-Fi Monitoring:** Retrieve interface details, traffic statistics, IP/MAC addresses, and link speed for Wi-Fi connections.
- **Ethernet Monitoring:** Similar monitoring capabilities for wired Ethernet interfaces.
- **System Totals:** Get cumulative sent and received bytes across all network interfaces.
- **Active TCP Connections:** List established TCP connections for the current user, including local/remote IPs, ports, and associated PIDs.
- **All Interfaces:** Comprehensive view of all network interfaces with IP, MAC, status, speed, and traffic data.

## Usage
To use these functions, simply import the module and call the desired function:

```python
from filesystem import device
network = device.network
```

### Examples:
- Get Wi-Fi interface name:

```python
wifi_iface = network.get_wifi_interface()
print(f"Wi-Fi Interface: {wifi_iface}")
```

- Get total received bytes
```python
total_recv = network.get_total_received_bytes()
print(f"Total Received: {total_recv} bytes")
```

- List active TCP connections
```python
connections = network.get_active_tcp_connections()
for conn in connections:
    print(f"PID {conn['pid']}: {conn['local_ip']}:{conn['local_port']} -> {conn['remote_ip']}:{conn['remote_port']}")
```
- Get all interfaces info
```python
all_ifaces = network.get_all_interfaces()
print(all_ifaces)
```
"""

import getpass
import socket
from typing import Dict, List, Optional

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
            "The module Network requires the 'psutil' library. "
            "Please install it via: pip install psutil"
        )

# ==============================================================
# Internal functions (private)
# ==============================================================
def __get_nic_io__() -> Dict[str, object]:
    return __psutil__.net_io_counters(pernic=True)

def __get_nic_stats__() -> Dict[str, object]:
    return __psutil__.net_if_stats()

def __get_nic_addrs__() -> Dict[str, List[object]]:
    return __psutil__.net_if_addrs()

def __find_interface__(patterns: List[str]) -> Optional[str]:
    stats = __get_nic_stats__()
    addrs = __get_nic_addrs__()
    interfaces = set(stats.keys()) & set(addrs.keys())
    for iface in interfaces:
        if any(pat in iface.lower() for pat in patterns):
            return iface
    return None

# ==============================================================
# Wi-Fi
# ==============================================================
def get_wifi_interface() -> Optional[str]:
    """
    # network.get_wifi_interface()
    
    ---
    
    ### Overview
    Identifies and returns the name of the active Wi-Fi network interface (e.g., 'wlan0', 'wlp3s0' on Linux, or 'en0' on macOS).
    
    ### Parameters:
    - **None**
    ### Returns:
    - **Optional[str]**: The Wi-Fi interface name if found, otherwise `None`.
    ### Raises:
    - **None**: This function does not raise exceptions; returns `None` on failure.
    ### Examples:
    - Retrieve the Wi-Fi interface name.
    ```python
    wifi_iface = get_wifi_interface()
    print(f"Wi-Fi Interface: {wifi_iface}")  # Output: e.g., 'wlan0'
    ```
    """
    __require_psutil__()
    return __find_interface__(['wlan', 'wi-fi', 'wlp', 'wl'])

def get_wifi_dropped_packets() -> int:
    """
    # network.get_wifi_dropped_packets()
    
    ---
    
    ### Overview
    Retrieves the number of dropped incoming packets on the Wi-Fi interface.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The count of dropped packets; returns 0 if the interface is not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get dropped packets on Wi-Fi.
    ```python
    dropped = get_wifi_dropped_packets()
    print(f"Dropped Packets: {dropped}")
    ```
    """
    __require_psutil__()
    iface = get_wifi_interface()
    if not iface: return 0
    io = __get_nic_io__().get(iface)
    return io.dropin if io else 0

def get_wifi_received_bytes() -> int:
    """
    # network.get_wifi_received_bytes()
    
    ---
    
    ### Overview
    Retrieves the total bytes received over the Wi-Fi interface since system boot.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The total received bytes; returns 0 if the interface is not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get received bytes on Wi-Fi.
    ```python
    recv_bytes = get_wifi_received_bytes()
    print(f"Received Bytes: {recv_bytes}")
    ```
    """
    __require_psutil__()
    iface = get_wifi_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_recv if io else 0

def get_wifi_sent_bytes() -> int:
    """
    # network.get_wifi_sent_bytes()
    
    ---
    
    ### Overview
    Retrieves the total bytes sent over the Wi-Fi interface since system boot.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The total sent bytes; returns 0 if the interface is not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get sent bytes on Wi-Fi.
    ```python
    sent_bytes = get_wifi_sent_bytes()
    print(f"Sent Bytes: {sent_bytes}")
    ```
    """
    __require_psutil__()
    iface = get_wifi_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_sent if io else 0

def get_wifi_speed_mbps() -> int:
    """
    # network.get_wifi_speed_mbps()
    
    ---
    
    ### Overview
    Retrieves the current link speed of the Wi-Fi interface in Mbps.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The link speed in Mbps; returns 0 if the interface is down or not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get Wi-Fi speed.
    ```python
    speed = get_wifi_speed_mbps()
    print(f"Wi-Fi Speed: {speed} Mbps")
    ```
    """
    __require_psutil__()
    iface = get_wifi_interface()
    if not iface:
        return 0
    stats = __get_nic_stats__().get(iface)
    return stats.speed if stats and stats.isup else 0

def get_wifi_ip() -> Optional[str]:
    """
    # network.get_wifi_ip()
    
    ---
    
    ### Overview
    Retrieves the IPv4 address assigned to the Wi-Fi interface.
    ### Parameters:
    - **None**
    ### Returns:
    - **Optional[str]**: The IPv4 address if found, otherwise `None`.
    ### Raises:
    - **None**: This function does not raise exceptions; returns `None` on failure.
    ### Examples:
    - Get Wi-Fi IP address.
    ```python
    ip = get_wifi_ip()
    print(f"Wi-Fi IP: {ip}")  # Output: e.g., '192.168.1.100'
    ```
    """
    __require_psutil__()
    iface = get_wifi_interface()
    if not iface:
        return None
    for addr in __get_nic_addrs__().get(iface, []):
        if addr.family == socket.AF_INET:
            return addr.address
    return None

def get_wifi_mac() -> Optional[str]:
    """
    # network.get_wifi_mac()
    
    ---
    
    ### Overview
    Retrieves the MAC address of the Wi-Fi interface.
    ### Parameters:
    - **None**
    ### Returns:
    - **Optional[str]**: The MAC address if found, otherwise `None`.
    ### Raises:
    - **None**: This function does not raise exceptions; returns `None` on failure.
    ### Examples:
    - Get Wi-Fi MAC address.
    ```python
    mac = get_wifi_mac()
    print(f"Wi-Fi MAC: {mac}")  # Output: e.g., 'aa:bb:cc:dd:ee:ff'
    ```
    """
    __require_psutil__()
    iface = get_wifi_interface()
    if not iface:
        return None
    for addr in __get_nic_addrs__().get(iface, []):
        if addr.family == socket.AF_LINK:
            return addr.address
    return None

# ==============================================================
# Ethernet
# ==============================================================
def get_ethernet_interface() -> Optional[str]:
    """
    # network.get_ethernet_interface()
    
    ---
    
    ### Overview
    Identifies and returns the name of the active Ethernet network interface (e.g., 'eth0', 'enp0s3').
    ### Parameters:
    - **None**
    ### Returns:
    - **Optional[str]**: The Ethernet interface name if found, otherwise `None`.
    ### Raises:
    - **None**: This function does not raise exceptions; returns `None` on failure.
    ### Examples:
    - Retrieve the Ethernet interface name.
    ```python
    eth_iface = get_ethernet_interface()
    print(f"Ethernet Interface: {eth_iface}")  # Output: e.g., 'eth0'
    ```
    """
    __require_psutil__()
    return __find_interface__(['eth', 'enp', 'eno', 'ens'])

def get_ethernet_received_bytes() -> int:
    """
    # network.get_ethernet_received_bytes()
    
    ---
    
    ### Overview
    Retrieves the total bytes received over the Ethernet interface since system boot.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The total received bytes; returns 0 if the interface is not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get received bytes on Ethernet.
    ```python
    recv_bytes = get_ethernet_received_bytes()
    print(f"Ethernet Received: {recv_bytes} bytes")
    ```
    """
    __require_psutil__()
    iface = get_ethernet_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_recv if io else 0

def get_ethernet_sent_bytes() -> int:
    """
    # network.get_ethernet_sent_bytes()
    
    ---
    
    ### Overview
    Retrieves the total bytes sent over the Ethernet interface since system boot.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The total sent bytes; returns 0 if the interface is not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get sent bytes on Ethernet.
    ```python
    sent_bytes = get_ethernet_sent_bytes()
    print(f"Ethernet Sent: {sent_bytes} bytes")
    ```
    """
    __require_psutil__()
    iface = get_ethernet_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_sent if io else 0

def get_ethernet_speed_mbps() -> int:
    """
    # network.get_ethernet_speed_mbps()
    
    ---
    
    ### Overview
    Retrieves the current link speed of the Ethernet interface in Mbps.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The link speed in Mbps; returns 0 if the interface is down or not found.
    ### Raises:
    - **None**: This function does not raise exceptions; returns 0 on failure.
    ### Examples:
    - Get Ethernet speed.
    ```python
    speed = get_ethernet_speed_mbps()
    print(f"Ethernet Speed: {speed} Mbps")
    ```
    """
    __require_psutil__()
    iface = get_ethernet_interface()
    if not iface:
        return 0
    stats = __get_nic_stats__().get(iface)
    return stats.speed if stats and stats.isup else 0

# ==============================================================
# Total from the machine
# ==============================================================
def get_total_received_bytes() -> int:
    """
    # network.get_total_received_bytes()
    
    ---
    
    ### Overview
    Retrieves the total bytes received across all network interfaces since system boot.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The cumulative received bytes.
    ### Raises:
    - **None**: This function does not raise exceptions.
    ### Examples:
    - Get system-wide received bytes.
    ```python
    total_recv = get_total_received_bytes()
    print(f"Total Received: {total_recv} bytes")
    ```
    """
    __require_psutil__()
    return __psutil__.net_io_counters(pernic=False).bytes_recv

def get_total_sent_bytes() -> int:
    """
    # network.get_total_sent_bytes()
    
    ---
    
    ### Overview
    Retrieves the total bytes sent across all network interfaces since system boot.
    ### Parameters:
    - **None**
    ### Returns:
    - **int**: The cumulative sent bytes.
    ### Raises:
    - **None**: This function does not raise exceptions.
    ### Examples:
    - Get system-wide sent bytes.
    ```python
    total_sent = get_total_sent_bytes()
    print(f"Total Sent: {total_sent} bytes")
    ```
    """
    __require_psutil__()
    return __psutil__.net_io_counters(pernic=False).bytes_sent

# ==============================================================
# Active TCP connections
# ==============================================================
def get_active_tcp_connections() -> List[Dict]:
    """
    # network.get_active_tcp_connections()
    
    ---
    
    ### Overview
    Lists all active (ESTABLISHED) TCP connections for the current user, including local and remote IP/port details and associated process IDs.
    ### Parameters:
    - **None**
    ### Returns:
    - **List[Dict]**: A list of dictionaries, each containing `'local_ip'`, `'local_port'`, `'remote_ip'`, `'remote_port'`, and `'pid'`. Empty list if no connections.
    ### Raises:
    - **psutil.AccessDenied**: If access to process information is denied (rare for own processes).
    - **psutil.NoSuchProcess**: If a process terminates during iteration.
    ### Examples:
    - List active TCP connections.
    ```python
    connections = get_active_tcp_connections()
    for conn in connections:
        print(f"PID {conn['pid']}: {conn['local_ip']}:{conn['local_port']} -> {conn['remote_ip']}:{conn['remote_port']}")
    ```
    """
    __require_psutil__()
    current_user = getpass.getuser()
    active = []
    for proc in __psutil__.process_iter(['pid', 'username']):
        try:
            if proc.info['username'] != current_user:
                continue
            p = __psutil__.Process(proc.info['pid'])
            conns = p.connections(kind='tcp')
            for c in conns:
                if c.status == 'ESTABLISHED' and c.raddr:
                    active.append({
                        'local_ip': c.laddr.ip if c.laddr else None,
                        'local_port': c.laddr.port if c.laddr else None,
                        'remote_ip': c.raddr.ip,
                        'remote_port': c.raddr.port,
                        'pid': proc.info['pid']
                    })
        except (__psutil__.NoSuchProcess, __psutil__.AccessDenied, __psutil__.ZombieProcess):
            pass
    return active

# ==============================================================
# All interfaces
# ==============================================================
def get_all_interfaces() -> Dict[str, Dict]:
    """
    # network.get_all_interfaces()
    
    ---
    
    ### Overview
    Retrieves comprehensive information for all network interfaces, including IP, MAC, status, speed, and traffic statistics.
    ### Parameters:
    - **None**
    ### Returns:
    - **Dict[str, Dict]**: A dictionary keyed by interface name, with values containing `'ip'`, `'mac'`, `'is_up'`, `'speed_mbps'`, `'bytes_sent'`, and `'bytes_recv'`.
    ### Raises:
    - **None**: This function does not raise exceptions.
    ### Examples:
    - Get details for all interfaces.
    ```python
    interfaces = get_all_interfaces()
    for iface, info in interfaces.items():
        print(f"{iface}: IP={info['ip']}, MAC={info['mac']}, Up={info['is_up']}, Speed={info['speed_mbps']} Mbps")
    ```
    """
    __require_psutil__()
    stats = __get_nic_stats__()
    addrs = __get_nic_addrs__()
    io = __get_nic_io__()
    result = {}
    for iface in stats:
        ip = mac = None
        for addr in addrs.get(iface, []):
            if addr.family == socket.AF_INET:
                ip = addr.address
            elif addr.family == __psutil__.AF_LINK:
                mac = addr.address
        nic_io = io.get(iface)
        result[iface] = {
            'ip': ip,
            'mac': mac,
            'is_up': stats[iface].isup,
            'speed_mbps': stats[iface].speed,
            'bytes_sent': nic_io.bytes_sent if nic_io else 0,
            'bytes_recv': nic_io.bytes_recv if nic_io else 0,
        }
    return result

# ==============================================================
# Explicit exports
# ==============================================================
__all__ = [
    'get_wifi_interface',
    'get_wifi_received_bytes',
    'get_wifi_sent_bytes',
    'get_wifi_speed_mbps',
    'get_wifi_ip',
    'get_wifi_mac',
    'get_ethernet_interface',
    'get_ethernet_received_bytes',
    'get_ethernet_sent_bytes',
    'get_ethernet_speed_mbps',
    'get_total_received_bytes',
    'get_total_sent_bytes',
    'get_active_tcp_connections',
    'get_all_interfaces',
]