import platform
import socket
import psutil


class SystemMonitor:

    @staticmethod
    def get_cpu_usage():
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "cpu_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
    }

    @staticmethod
    def get_memory_usage():
        memory = psutil.virtual_memory()

        return {
            "total": round(memory.total / (1024 ** 3), 2),
            "used": round(memory.used / (1024 ** 3), 2),
            "available": round(memory.available / (1024 ** 3), 2),
            "percent": memory.percent
        }

    @staticmethod
    def get_disk_usage():
        disk = psutil.disk_usage('/')

        return {
            "total": round(disk.total / (1024 ** 3), 2),
            "used": round(disk.used / (1024 ** 3), 2),
            "free": round(disk.free / (1024 ** 3), 2),
            "percent": disk.percent
        }

    @staticmethod
    def get_network_usage():
        network = psutil.net_io_counters()

        return {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_received": network.packets_recv
    }

    @staticmethod
    def get_system_info():
        return {
            "hostname": socket.gethostname(),
            "operating_system": platform.system(),
            "release": platform.release(),
            "processor": platform.processor(),
            "architecture": platform.machine(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "logical_processors": psutil.cpu_count(logical=True)
        }

    @staticmethod
    def get_running_processes():

        processes = []

        for process in psutil.process_iter(
    ['pid', 'name', 'status', 'memory_percent']
):
            try:
                processes.append({
    "pid": process.info["pid"],
    "name": process.info["name"],
    "status": process.info["status"],
    "memory_percent": round(process.info["memory_percent"], 2)
})
            except Exception:
                pass

        return processes