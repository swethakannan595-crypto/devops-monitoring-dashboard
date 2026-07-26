import psutil
import platform
from datetime import datetime


class SystemService:

    @staticmethod
    def get_cpu():
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True)
        }

    @staticmethod
    def get_memory():
        memory = psutil.virtual_memory()

        return {
            "total": round(memory.total / (1024 ** 3), 2),
            "used": round(memory.used / (1024 ** 3), 2),
            "available": round(memory.available / (1024 ** 3), 2),
            "percent": memory.percent
        }

    @staticmethod
    def get_disk():
        disk = psutil.disk_usage("/")

        return {
            "total": round(disk.total / (1024 ** 3), 2),
            "used": round(disk.used / (1024 ** 3), 2),
            "free": round(disk.free / (1024 ** 3), 2),
            "percent": disk.percent
        }

    @staticmethod
    def get_network():
        network = psutil.net_io_counters()

        return {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_received": network.packets_recv
        }

    @staticmethod
    def get_system():

        boot = datetime.fromtimestamp(psutil.boot_time())

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "boot_time": boot.strftime("%Y-%m-%d %H:%M:%S")
        }