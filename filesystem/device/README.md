# Device Module

## Overview

The `device` module in **FileSystemPro** acts as a centralized gateway for system hardware and resource monitoring, exposing submodules for CPU, disk, memory, and network insights. It relies on the optional `psutil` library (install via `pip install psutil`) to deliver cross-platform metrics like CPU utilization, disk partitions/usage/I/O, virtual/swap memory stats, and network interface details (e.g., Wi-Fi/Ethernet traffic, IPs, connections). Without `psutil`, functions raise `ImportError` on access, encouraging graceful fallbacks in production code.

This module is designed for **programmers building system utilities, performance dashboards, or diagnostic tools**, where real-time hardware telemetry enhances logging or alerts (e.g., low memory warnings). Submodules provide granular access: `device.cpu` for processor stats, `device.disks` for storage, `device.memory` for RAM/swap, and `device.network` for connectivity. All functions are lightweight, returning dicts/objects for easy integration with `console` for colored output or `wrapper` for metadata enrichment.

**Key Design Principles**:

- **Optional Dependency**: Lazy-loads `psutil`; clear errors guide installation.
- **Platform-Agnostic**: Uses `psutil`'s abstractions; platform-specific tweaks (e.g., boot drive naming via subprocess).
- **Comprehensive Yet Simple**: Aggregates metrics (e.g., disk totals) while exposing raw `psutil` objects.
- **Error Resilience**: No exceptions on missing data (e.g., returns 0/None for absent interfaces).

**Compatibility**:

- Python 3.10+ (leverages `psutil`, `subprocess`, `datetime`).
- Platforms: Cross-platform (Linux/macOS/Windows; some metrics Unix-biased, e.g., slab memory).
- Dependencies: `psutil` (optional; core functions fail gracefully without it).

## Features

- **CPU Monitoring**: Usage %, time breakdowns (user/system/idle), logical core count.
- **Disk Management**: Partitions (filtered by device/FSTYPE/mount/options), usage metrics (total/used/free/%), I/O counters, boot time/drive/filesystem.
- **Memory Tracking**: Virtual (total/available/used/active/inactive/buffers/cached/shared/slab) and swap (total/used/free/%/sin/sout) stats.
- **Network Observation**: Wi-Fi/Ethernet interfaces (speed, bytes sent/recv, IP/MAC), system totals, active TCP connections (PID-filtered), all-interface summary.
- **Unified Access**: Import once via `device`; submodules as attributes (e.g., `device.disks.disk_info()`).
- **Filtering & Aggregation**: Disk partitions by criteria; comprehensive dicts for dashboards.

## Installation and Setup

As part of **FileSystemPro**, install via:

```bash
pip install filesystempro
```

For full functionality:

```bash
pip install psutil
```

No config needed—import and query. Test availability:

```python
from filesystem import device
try:
    device.cpu.cpu_percent()  # Raises ImportError if missing
except ImportError:
    print("Install psutil for device features")
```

## Usage

Import the module and access submodules:

```python
from filesystem import device
cpu = device.cpu      # CPU functions
disks = device.disks  # Disk functions
memory = device.memory  # Memory functions
network = device.network  # Network functions
```

Functions return `psutil` objects/dicts/lists for direct use or serialization.

### Submodule Reference

#### CPU (`device.cpu`)

| Function | Parameters | Returns | Raises/Notes |
|----------|------------|---------|--------------|
| `cpu_percent() → float` | None. | CPU % used. | `ImportError` (no psutil). |
| `cpu_times() → psutil.scputimes` | None. | Time dict (user/system/idle/etc.). | As above. |
| `cpu_count() → int` | None. | Logical cores. | As above. |

#### Disks (`device.disks`)

| Function | Parameters | Returns | Raises/Notes |
|----------|------------|---------|--------------|
| `get_disk_partitions() → list[dict]` | None. | Partition details (device/mount/fstype/opts). | `ImportError`. |
| `get_boot_drive_name() → str` | None. | Boot drive label (platform-specific). | `Exception` (subprocess fail). |
| `get_disk_partition_filteredby_device(filter: str) → list[dict]` | `filter` (str): Device name. | Matching partitions. | `ImportError`. |
| `get_disk_partition_filteredby_fstype(filter: str) → list[dict]` | `filter` (str): FSTYPE (e.g., 'ext4'). | Matching partitions. | As above. |
| `get_disk_partition_filteredby_mountpoint(filter: str) → list[dict]` | `filter` (str): Mount (e.g., '/'). | Matching partitions. | As above. |
| `get_disk_partition_filteredby_opts(filter: str) → list[dict]` | `filter` (str): Options (e.g., 'rw'). | Matching partitions. | As above. |
| `storage_metrics(mountpoint: str) → dict[int, float\|int]` | `mountpoint` (str): Path (e.g., '/'). | {0: total, 1: free, 2: used, 3: % free, 4: % used}. | `ImportError`. |
| `disk_info() → dict[int, tuple]` | None. | Aggregated partitions + metrics. | As above. |
| `disk_io_counters() → dict[str, psutil.diskio]` | None. | Per-disk I/O (reads/writes/bytes/time). | As above. |
| `boot_time() → str` | None. | Human-readable boot datetime (DD/MM/YYYY HH:MM:SS). | `ImportError`. |
| `current_disk_filesystem_name() → str` | None. | Boot FSTYPE (e.g., 'ntfs'). | `ImportError`. |

#### Memory (`device.memory`)

| Function | Parameters | Returns | Raises/Notes |
|----------|------------|---------|--------------|
| `virtual_memory() → psutil.svmem` | None. | Full VM stats. | `ImportError`. |
| `total_virtual_memory() → int` | None. | Total RAM bytes. | As above. |
| `available_virtual_memory() → int` | None. | Available bytes. | As above. |
| `percent_virtual_memory() → float` | None. | % used. | As above. |
| `used_virtual_memory() → int` | None. | Used bytes. | As above. |
| `free_virtual_memory() → int` | None. | Free bytes. | As above. |
| `active_virtual_memory() → int` | None. | Active bytes. | As above. |
| `inactive_virtual_memory() → int` | None. | Inactive bytes. | As above. |
| `buffers_virtual_memory() → int` | None. | Buffers bytes. | As above. |
| `cached_virtual_memory() → int` | None. | Cached bytes. | As above. |
| `shared_virtual_memory() → int` | None. | Shared bytes. | As above. |
| `slab_virtual_memory() → int` | None. | Slab bytes (Unix). | As above. |
| `swap_memory() → psutil.sswap` | None. | Full swap stats. | As above. |
| `total_swap_memory() → int` | None. | Total swap bytes. | As above. |
| `used_swap_memory() → int` | None. | Used swap bytes. | As above. |
| `free_swap_memory() → int` | None. | Free swap bytes. | As above. |
| `percent_swap_memory() → float` | None. | % swap used. | As above. |
| `sin_swap_memory() → int` | None. | Pages swapped in. | As above. |
| `sout_swap_memory() → int` | None. | Pages swapped out. | As above. |

#### Network (`device.network`)

| Function | Parameters | Returns | Raises/Notes |
|----------|------------|---------|--------------|
| `get_wifi_interface() → Optional[str]` | None. | Wi-Fi name (e.g., 'wlan0'). | `ImportError`; None if missing. |
| `get_wifi_dropped_packets() → int` | None. | Dropped in packets. | As above; 0 if missing. |
| `get_wifi_received_bytes() → int` | None. | Total recv bytes. | As above; 0 if missing. |
| `get_wifi_sent_bytes() → int` | None. | Total sent bytes. | As above; 0 if missing. |
| `get_wifi_speed_mbps() → int` | None. | Link speed Mbps. | As above; 0 if down. |
| `get_wifi_ip() → Optional[str]` | None. | IPv4 address. | As above; None if missing. |
| `get_wifi_mac() → Optional[str]` | None. | MAC address. | As above; None if missing. |
| `get_ethernet_interface() → Optional[str]` | None. | Ethernet name (e.g., 'eth0'). | As above. |
| `get_ethernet_received_bytes() → int` | None. | Ethernet recv bytes. | As above; 0 if missing. |
| `get_ethernet_sent_bytes() → int` | None. | Ethernet sent bytes. | As above; 0 if missing. |
| `get_ethernet_speed_mbps() → int` | None. | Ethernet speed Mbps. | As above; 0 if down. |
| `get_total_received_bytes() → int` | None. | System-wide recv bytes. | `ImportError`. |
| `get_total_sent_bytes() → int` | None. | System-wide sent bytes. | As above. |
| `get_active_tcp_connections() → list[dict]` | None. | TCP conns {'local_ip': str, 'local_port': int, 'remote_ip': str, 'remote_port': int, 'pid': int}. | `ImportError`; `AccessDenied` (rare). |
| `get_all_interfaces() → dict[str, dict]` | None. | Interfaces {name: {'ip': str, 'mac': str, 'is_up': bool, 'speed_mbps': int, 'bytes_sent': int, 'bytes_recv': int}}. | `ImportError`. |

## Examples

### CPU Monitoring

```python
from filesystem import device

cpu = device.cpu
usage = cpu.cpu_percent()
print(f"CPU: {usage}%")  # e.g., 23.5

times = cpu.cpu_times()
print(f"User time: {times.user}s")  # Breakdown

cores = cpu.cpu_count()
print(f"Cores: {cores}")  # e.g., 8
```

### Disk Usage and Partitions

```python
from filesystem import device

disks = device.disks
partitions = disks.get_disk_partitions()
print(partitions)  # List of dicts: [{'device': '/dev/sda1', 'mountpoint': '/', ...}]

info = disks.disk_info()
print(info[0])  # Tuple: (mount, device, fstype, opts, total, used, free, %used, %free)

root_metrics = disks.storage_metrics('/')
print(f"Root used: {root_metrics[2]} bytes ({root_metrics[4]}%)")

boot = disks.boot_time()
print(f"Booted: {boot}")  # e.g., "10/11/2025 08:14:00"
```

### Memory Stats

```python
from filesystem import device

memory = device.memory
vm = memory.virtual_memory()
print(f"RAM used: {vm.used / (1024**3):.1f} GB ({vm.percent}%)")

swap = memory.swap_memory()
print(f"Swap used: {swap.used / (1024**3):.1f} GB ({swap.percent}%)")
```

### Network Insights

```python
from filesystem import device

network = device.network
wifi = network.get_wifi_interface()
print(f"Wi-Fi: {wifi}")  # e.g., 'wlan0'

if wifi:
    ip = network.get_wifi_ip()
    speed = network.get_wifi_speed_mbps()
    print(f"IP: {ip}, Speed: {speed} Mbps")

conns = network.get_active_tcp_connections()
print(f"Active TCP: {len(conns)}")  # Filtered by user

all_if = network.get_all_interfaces()
print(all_if['lo'])  # {'ip': None, 'mac': None, 'is_up': True, ...}
```

## Best Practices

- **Dependency Check**: Wrap calls in `try-except ImportError` for optional `psutil`; fallback to OS commands (e.g., `free -h` for memory).
- **Polling**: For live monitoring, loop with `time.sleep(1)` (e.g., CPU % is interval-based).
- **Filtering**: Use disk filters (e.g., by FSTYPE) for targeted queries; cache `disk_info()` for dashboards.
- **Units**: Raw bytes from `psutil`; format via `wrapper.get_object` or manual (e.g., `/ 1024**3` for GB).
- **Security**: TCP conns filter by user—avoid root for privacy; don't expose IPs in logs.
- **Performance**: Avoid frequent full scans (e.g., `disk_io_counters()`); sample intervals.
- **Cross-Platform**: Test on all OS (e.g., Wi-Fi names vary); handle None gracefully.
- **Integration**: Colorize outputs with `console` (e.g., `console.red()(f"High CPU: {usage}%")`).

## Limitations

- **psutil Requirement**: Core dependency; no built-in fallbacks (e.g., no manual CPU polling).
- **Platform Variations**: Boot drive/FSTYPE platform-specific (subprocess may fail in restricted envs); some metrics Unix-only (e.g., slab).
- **Polling Overhead**: `psutil` scans system-wide—inefficient for high-freq (>1Hz); use signals for events.
- **Network Scope**: TCP only (no UDP); conns user-filtered (misses system processes).
- **No Historical Data**: Snapshots only; track deltas manually for trends.
- **Permissions**: I/O counters/conns may need elevated access (e.g., admin on Windows).
- **IPv6**: Defaults to IPv4; extend `get_*_ip()` for dual-stack.

## Contributing

See the root [README.md](../../README.md) and [CONTRIBUTING.md](https://github.com/hbisneto/FileSystemPro/blob/main/CONTRIBUTING.md) for guidelines. Report issues or suggest enhancements (e.g., GPU monitoring, historical averages) via GitHub.

## License

This module is part of **FileSystemPro**, licensed under the MIT License. See [LICENSE](../LICENSE) for details.