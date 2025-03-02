from filesystem.device import disks

print(disks.drive_name)

print(disks.current_disk_filesystem_name())
print(disks.storage_metrics("/"))