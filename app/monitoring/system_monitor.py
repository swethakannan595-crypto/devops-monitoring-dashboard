import os
import platform
import socket

import psutil


class SystemMonitor:

    @staticmethod
    def get_cpu_usage():
        frequency = psutil.cpu_freq()

        return {
            "usage": round(psutil.cpu_percent(interval=0.5), 1),
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_cores": psutil.cpu_count(logical=True) or 0,
            "frequency_mhz": (
                round(frequency.current, 1)
                if frequency
                else 0
            ),
        }

    @staticmethod
    def get_memory_usage():
        memory = psutil.virtual_memory()

        return {
            "total_gb": round(
                memory.total / (1024 ** 3),
                2,
            ),
            "used_gb": round(
                memory.used / (1024 ** 3),
                2,
            ),
            "available_gb": round(
                memory.available / (1024 ** 3),
                2,
            ),
            "percentage": round(
                float(memory.percent),
                1,
            ),
        }

    @staticmethod
    def get_disk_usage():

        if os.name == "nt":
            drive = os.environ.get("SystemDrive", "C:")
            disk_path = drive + "\\"
        else:
            disk_path = "/"

        disk = psutil.disk_usage(disk_path)

        return {
            "total_gb": round(
                disk.total / (1024 ** 3),
                2,
            ),
            "used_gb": round(
                disk.used / (1024 ** 3),
                2,
            ),
            "free_gb": round(
                disk.free / (1024 ** 3),
                2,
            ),
            "percentage": round(
                float(disk.percent),
                1,
            ),
        }

    @staticmethod
    def get_network_usage():

        network = psutil.net_io_counters()

        if network is None:
            return {
                "bytes_sent": 0,
                "bytes_received": 0,
                "packets_sent": 0,
                "packets_received": 0,
            }

        return {
            "bytes_sent": int(network.bytes_sent),
            "bytes_received": int(network.bytes_recv),
            "packets_sent": int(network.packets_sent),
            "packets_received": int(network.packets_recv),
        }

    @staticmethod
    def get_system_info():

        return {
            "hostname": socket.gethostname(),
            "operating_system": platform.system(),
            "release": platform.release(),
            "processor": platform.processor(),
            "architecture": platform.machine(),
            "cpu_cores": psutil.cpu_count(
                logical=False
            ) or 0,
            "logical_processors": psutil.cpu_count(
                logical=True
            ) or 0,
        }

    @staticmethod
    def get_running_processes():

        processes = []

        for process in psutil.process_iter(
            [
                "pid",
                "name",
                "status",
                "memory_percent",
            ]
        ):
            try:
                processes.append(
                    {
                        "pid": process.info["pid"],
                        "name": (
                            process.info["name"]
                            or "Unknown"
                        ),
                        "status": process.info["status"],
                        "memory_percent": round(
                            process.info["memory_percent"]
                            or 0,
                            2,
                        ),
                    }
                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        return processes