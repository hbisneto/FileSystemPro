"""
# Network
Provides functions to get network interface information such as Wi-Fi and Ethernet statistics, IP addresses, MAC addresses, and active TCP connections.
"""

import psutil as __psutil__
import socket
from typing import Dict, List, Optional


# ==============================================================
# Internal functions (private)
# ==============================================================

def __get_nic_io__() -> Dict[str, object]:
    return __psutil__.net_io_counters(pernic=True)


def __get_nic_stats__() -> Dict[str, object]:
    return __psutil__.net_if_stats()


def __get_nic_addrs__() -> Dict[str, List[object]]:
    return __psutil__.net_if_addrs()


def _find_interface(patterns: List[str]) -> Optional[str]:
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
    """ Return the name of the Wi-Fi interface (e.g., wlan0, wlp3s0) """
    return _find_interface(['wlan', 'wi-fi', 'wlp', 'wl'])

def get_wifi_dropped_packets() -> int:
    """ Dropped packets by the Wi-Fi interface (incoming) """
    iface = get_wifi_interface()
    if not iface: return 0
    io = __get_nic_io__().get(iface)
    return io.dropin if io else 0


def get_wifi_received_bytes() -> int:
    """Received bytes by the Wi-Fi interface"""
    iface = get_wifi_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_recv if io else 0


def get_wifi_sent_bytes() -> int:
    """Sent bytes by the Wi-Fi interface"""
    iface = get_wifi_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_sent if io else 0


def get_wifi_speed_mbps() -> int:
    """Current speed of the Wi-Fi in Mbps"""
    iface = get_wifi_interface()
    if not iface:
        return 0
    stats = __get_nic_stats__().get(iface)
    return stats.speed if stats and stats.isup else 0


def get_wifi_ip() -> Optional[str]:
    """IPv4 address of the Wi-Fi interface"""
    iface = get_wifi_interface()
    if not iface:
        return None
    for addr in __get_nic_addrs__().get(iface, []):
        if addr.family == socket.AF_INET:  # ← CORRIGIDO: socket.AF_INET
            return addr.address
    return None


def get_wifi_mac() -> Optional[str]:
    """MAC address of the Wi-Fi interface"""
    iface = get_wifi_interface()
    if not iface:
        return None
    for addr in __get_nic_addrs__().get(iface, []):
        if addr.family == socket.AF_LINK:  # ← CORRIGIDO: socket.AF_LINK
            return addr.address
    return None


# ==============================================================
# Ethernet
# ==============================================================

def get_ethernet_interface() -> Optional[str]:
    """Return the active Ethernet interface (e.g., eth0, enp0s3)"""
    return _find_interface(['eth', 'enp', 'eno', 'ens'])


def get_ethernet_received_bytes() -> int:
    iface = get_ethernet_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_recv if io else 0


def get_ethernet_sent_bytes() -> int:
    iface = get_ethernet_interface()
    if not iface:
        return 0
    io = __get_nic_io__().get(iface)
    return io.bytes_sent if io else 0


def get_ethernet_speed_mbps() -> int:
    iface = get_ethernet_interface()
    if not iface:
        return 0
    stats = __get_nic_stats__().get(iface)
    return stats.speed if stats and stats.isup else 0


# ==============================================================
# Total from the machine
# ==============================================================

def get_total_received_bytes() -> int:
    return __psutil__.net_io_counters(pernic=False).bytes_recv


def get_total_sent_bytes() -> int:
    return __psutil__.net_io_counters(pernic=False).bytes_sent


# ==============================================================
# Active TCP connections
# ==============================================================

def get_active_tcp_connections() -> List[Dict]:
    """List active TCP ESTABLISHED connections with remote IP"""
    conns = __psutil__.net_connections(kind='tcp')
    active = []
    for c in conns:
        if c.status == 'ESTABLISHED' and c.raddr:
            active.append({
                'local_ip': c.laddr.ip,
                'local_port': c.laddr.port,
                'remote_ip': c.raddr.ip,
                'remote_port': c.raddr.port,
                'pid': c.pid
            })
    return active


# ==============================================================
# All interfaces
# ==============================================================

def get_all_interfaces() -> Dict[str, Dict]:
    """Return IP, MAC, status, speed, and traffic of all interfaces"""
    stats = __get_nic_stats__()
    addrs = __get_nic_addrs__()
    io = __get_nic_io__()

    result = {}
    for iface in stats:
        ip = mac = None
        for addr in addrs.get(iface, []):
            if addr.family == socket.AF_INET:      # ← CORRIGIDO
                ip = addr.address
            elif addr.family == __psutil__.AF_LINK:
            # elif addr.family == socket.AF_LINK:    # ← CORRIGIDO
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