from zesty.models.hf_interface import *


class DiskMonitor:
    filesystems = None
    unused_devices = None

    def __init__(self, disk_mon_data):
        self.filesystems = {}
        self.unused_devices = {}

        for fs in disk_mon_data.get('filesystems', {}):
            self.filesystems[fs] = FileSystem(disk_mon_data.get('filesystems', {}).get(fs, {}))

        for unused_dev in disk_mon_data.get('unused_devices', {}):
            self.unused_devices[unused_dev] = self.UnusedDevice(disk_mon_data.get('unused_devices', {}).get(unused_dev, {}))

    class UnusedDevice:
        size = None
        map = None

        def __init__(self, block_device_data):
            for k, v in block_device_data.items():
                exec('self.' + k + '=v')


class FileSystem:
    mount_path = None
    fs_type = None
    space = None
    inodes = None
    devices = None
    is_partition = None
    partition_number = None
    label = None
    LV = None
    VG = None
    lvm_path = None

    def __init__(self, fs_data):
        self.mount_path = fs_data.get('mount_path')
        self.fs_type = fs_data.get('fs_type')
        self.mount_path = fs_data.get('mount_path')
        self.space = self.Usage(fs_data.get('space'))
        self.inodes = self.Usage(fs_data.get('inodes'))
        self.partition_number = fs_data.get('partition_number')
        self.is_partition = fs_data.get('is_partition')
        self.label = fs_data.get('label')
        self.LV = fs_data.get('LV')
        self.VG = fs_data.get('VG')
        self.lvm_path = fs_data.get('lvm_path')
        self.devices = {}

        for dev in fs_data.get('devices'):
            self.devices[dev] = self.BlockDevice(fs_data.get('devices', {}).get(dev, {}))

    class BlockDevice(IDeviceHF):
        size: int = None
        btrfs_dev_id: str = None
        volume_id: str = None
        dev_usage: int = None
        iops_stats = None
        map = None

        def __init__(self, block_device_data):
            for k, v in block_device_data.items():
                exec('self.' + k + '=v')

        def get_dev_id(self) -> str:
            return self.btrfs_dev_id

        def get_size(self) -> int:
            return self.size

        def get_usage(self) -> int:
            return self.dev_usage

        def get_unlock_ts(self) -> int:
            # TODO => ONLY FOR DEBUG HAVE TO CHANGE THAT WHEN IMPLEMENTED!
            return 9999999999999
            # raise NotImplementedError(
            #     "Block Device 'get_unlock_ts' is not implemented yet")

        def get_iops_stats(self):
            return self.iops_stats

        def get_volume_id(self):
            return self.volume_id

    class Usage:
        total = None
        used = None
        free = None
        percent = None

        def __init__(self, usage_data):
            for k, v in usage_data.items():
                exec('self.' + k + '=v')
