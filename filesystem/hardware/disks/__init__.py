import psutil
from datetime import datetime
import subprocess

def current_disk_filesystem_name():
    dskpart = psutil.disk_partitions()
    fstypes = [part.fstype for part in dskpart if part.mountpoint in ['C:/', '/']]
    
    return fstypes[0]


# def get_boot_drive_name():
#     try:
#         cmd = "python -c \"from Foundation import NSFileManager; print(NSFileManager.defaultManager().displayNameAtPath_('/'))\""
#         startup_drive_name = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

#         return startup_drive_name
    
#     except Exception as e:
#         return str(e)

def boot_time():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    return f'{bt.day}/{bt.month}/{bt.year} {bt.hour}:{bt.minute}:{bt.second}'

######################################## DISK INFORMATION ########################################

### DISK PARTITIONS
def get_disk_partitions():
    var = psutil.disk_partitions()
    # Convert the output to a list of dictionaries
    output = [part._asdict() for part in var]
    
    return output

def get_boot_drive_name():
    try:
        cmd = "python -c \"from Foundation import NSFileManager; print(NSFileManager.defaultManager().displayNameAtPath_('/'))\""
        startup_drive_name = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

        return startup_drive_name
    
    except Exception as e:
        return str(e)

def __get_disk_device_list__():
    var = get_disk_partitions()
    data_list = []
    for data in var:
        # print(data)
        data_list.append(data)
    devices = [item['device'] for item in data_list]
    
    return devices

def __get_disk_filesystem_list__():
    var = get_disk_partitions()
    data_list = []
    for data in var:
        # print(data)
        data_list.append(data)
    fstype = [item['fstype'] for item in data_list]
    
    return fstype

def __get_disk_maxfile_list__():
    var = get_disk_partitions()
    data_list = []
    for data in var:
        # print(data)
        data_list.append(data)
    maxfile = [item['maxfile'] for item in data_list]
    
    return maxfile

def __get_disk_maxpath_list__():
    var = get_disk_partitions()
    data_list = []
    for data in var:
        # print(data)
        data_list.append(data)
    maxpath = [item['maxpath'] for item in data_list]
    
    return maxpath

def __get_disk_mountpoint_list__():
    var = get_disk_partitions()
    data_list = []
    for data in var:
        # print(data)
        data_list.append(data)
    mountpoints = [item['mountpoint'] for item in data_list]
    
    return mountpoints

def __get_disk_opts_list__():
    var = get_disk_partitions()
    data_list = []
    for data in var:
        # print(data)
        data_list.append(data)
    opts = [item['opts'] for item in data_list]
    
    return opts

def get_disk_partition_filteredby_device(filter):
    var = get_disk_partitions()
    out_filter = filter.lower()
    output = [d for d in var if d['device'] == out_filter]

    return output

def get_disk_partition_filteredby_fstype(filter):
    var = get_disk_partitions()
    out_filter = filter.lower()
    output = [d for d in var if d['fstype'] == out_filter]
    
    return output

def get_disk_partition_filteredby_maxfile(filter):
    var = get_disk_partitions()
    output = [d for d in var if d['maxfile'] == filter]

    return output

def get_disk_partition_filteredby_maxpath(filter):
    var = get_disk_partitions()
    output = [d for d in var if d['maxpath'] == filter]

    return output

def get_disk_partition_filteredby_mountpoint(filter):
    var = get_disk_partitions()
    output = [d for d in var if d['mountpoint'] == filter]

    return output

def get_disk_partition_filteredby_opts(filter):
    var = get_disk_partitions()
    out_filter = filter.lower()
    output = [d for d in var if d['opts'] == out_filter]

    return output

######################################## DISK USAGE ########################################

def storage_metrics(mountpoint):
    """
     This function returns storage metrics for a given mount point.
    
     Parameters:
     mountpoint (str): The mount point for which storage metrics are required.

     Returns:
     `metrics_list (dict)`: A dictionary containing the following storage metrics:
         0 : total - The total storage space on the mount point.
         1 : free - The free storage space on the mount point.
         2 : used - The storage space used on the mount point.
         3: percent_free - The percentage of free space at the mount point.
         4: percent_used - The percentage of space used at the mount point.
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
    
    # return psutil.disk_usage(mountpoint)

def __get_disk_total_usage_list__():
    var = __get_disk_mountpoint_list__()
    total_list = []
    for disk in var:
        metrics = storage_metrics(disk)
        total_list.append(metrics[0])

    return total_list

def __get_disk_free_usage_list__():
    var = __get_disk_mountpoint_list__()
    free_list = []
    for disk in var:
        metrics = storage_metrics(disk)
        free_list.append(metrics[1])

    return free_list

def __get_disk_used_usage_list__():
    var = __get_disk_mountpoint_list__()
    used_list = []
    for disk in var:
        metrics = storage_metrics(disk)
        used_list.append(metrics[2])

    return used_list

def __get_disk_free_percent_usage_list__():
    var = __get_disk_mountpoint_list__()
    free_percent_list = []
    for disk in var:
        metrics = storage_metrics(disk)
        free_percent_list.append(metrics[3])

    return free_percent_list

def __get_disk_used_percent_usage_list__():
    var = __get_disk_mountpoint_list__()
    used_percent_list = []
    for disk in var:
        metrics = storage_metrics(disk)
        used_percent_list.append(metrics[4])

    return used_percent_list

def disk_info():
    devices = __get_disk_device_list__()
    filesystems = __get_disk_filesystem_list__()
    maxfile = __get_disk_maxfile_list__()
    maxpath = __get_disk_maxpath_list__()
    mountpoint = __get_disk_mountpoint_list__()
    opts = __get_disk_opts_list__()

    total = __get_disk_total_usage_list__()
    used = __get_disk_used_usage_list__()
    free = __get_disk_free_usage_list__()
    percent_free = __get_disk_free_percent_usage_list__()
    percent_used = __get_disk_used_percent_usage_list__()
    # Cria um dicionário combinando as listas
    disk_info = {i: info for i, info in enumerate(
        zip(mountpoint, devices, filesystems, maxfile, maxpath,
            opts, total, used, free, percent_free, percent_used)
            )
    }

    return disk_info




# def current_disk_filesystem_name():
#     dskpart = psutil.disk_partitions()
#     fstypes = [part.fstype for part in dskpart if part.mountpoint in ['C:/', '/']]
    
#     return fstypes[0]

# def get_disk_filesystem_name_list():
#     dskpart = psutil.disk_partitions()
#     fstypes = [part.fstype for part in dskpart if part.mountpoint in ['C:/', '/']]
    
#     return fstypes


# def disk_filesystem_name():
#     dskpart = psutil.disk_partitions()
#     fstypes = [part.fstype for part in dskpart if part.mountpoint in ['C:/', '/']]
    
#     return fstypes[0]

# def disk_usage(mountpoint):
    
#     return psutil.disk_usage(mountpoint)

def disk_io_counters():
    # Get disk I/O counters
    disk_io = psutil.disk_io_counters(perdisk=True)

    # Convert the named tuple to a dictionary
    # disk_io_dict = disk_io._asdict()

    # Now disk_io_dict is a dictionary with the items of the function
    
    # return disk_io_dict
    return disk_io
    # return psutil.disk_io_counters()

######################################## DISK INFORMATION ########################################

boot_drive_name = get_boot_drive_name()