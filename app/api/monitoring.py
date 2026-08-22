from fastapi import APIRouter

from app.monitoring.system_monitor import SystemMonitor
from app.monitoring.prometheus_metrics import (
    CPU_USAGE,
    MEMORY_USAGE,
)


router = APIRouter(
    prefix="/api",
    tags=["System Monitoring"],
)


# =========================================================
# COMPLETE SYSTEM INFORMATION
# =========================================================

@router.get("/system")
def system_info():
    """
    Complete real-time system monitoring information.

    Used by:
        /dashboard
        frontend JavaScript
        Prometheus-related monitoring
    """

    # -----------------------------------------------------
    # Collect REAL system values
    # -----------------------------------------------------

    cpu = SystemMonitor.get_cpu_usage()
    memory = SystemMonitor.get_memory_usage()
    disk = SystemMonitor.get_disk_usage()
    network = SystemMonitor.get_network_usage()
    system = SystemMonitor.get_system_info()

    # -----------------------------------------------------
    # Extract the CORRECT keys returned by SystemMonitor
    # -----------------------------------------------------

    cpu_usage = float(cpu.get("usage", 0))
    memory_percentage = float(memory.get("percentage", 0))
    disk_percentage = float(disk.get("percentage", 0))

    # -----------------------------------------------------
    # Update Prometheus
    # -----------------------------------------------------

    try:
        CPU_USAGE.set(cpu_usage)
        MEMORY_USAGE.set(memory_percentage)
    except Exception as exc:
        print(
            f"WARNING: Prometheus metric update failed: {exc}"
        )

    # -----------------------------------------------------
    # Return API response
    # -----------------------------------------------------

    return {
        "system": {
            "hostname": system.get(
                "hostname",
                "Unknown",
            ),
            "operating_system": system.get(
                "operating_system",
                "Unknown",
            ),
            "release": system.get(
                "release",
                "Unknown",
            ),
            "processor": system.get(
                "processor",
                "Unknown",
            ),
            "architecture": system.get(
                "architecture",
                "Unknown",
            ),
            "cpu_cores": system.get(
                "cpu_cores",
                0,
            ),
            "logical_processors": system.get(
                "logical_processors",
                0,
            ),
        },

        "cpu": {
            "usage": cpu_usage,
            "physical_cores": cpu.get(
                "physical_cores",
                0,
            ),
            "logical_cores": cpu.get(
                "logical_cores",
                0,
            ),
            "frequency_mhz": cpu.get(
                "frequency_mhz",
                0,
            ),
        },

        "memory": {
            "total_gb": memory.get(
                "total_gb",
                0,
            ),
            "used_gb": memory.get(
                "used_gb",
                0,
            ),
            "available_gb": memory.get(
                "available_gb",
                0,
            ),
            "percentage": memory_percentage,
        },

        "disk": {
            "total_gb": disk.get(
                "total_gb",
                0,
            ),
            "used_gb": disk.get(
                "used_gb",
                0,
            ),
            "free_gb": disk.get(
                "free_gb",
                0,
            ),
            "percentage": disk_percentage,
        },

        "network": {
            "bytes_sent": network.get(
                "bytes_sent",
                0,
            ),
            "bytes_received": network.get(
                "bytes_received",
                0,
            ),
            "packets_sent": network.get(
                "packets_sent",
                0,
            ),
            "packets_received": network.get(
                "packets_received",
                0,
            ),
        },
    }


# =========================================================
# CPU
# =========================================================

@router.get("/cpu")
def cpu_usage():

    data = SystemMonitor.get_cpu_usage()

    usage = float(
        data.get("usage", 0)
    )

    try:
        CPU_USAGE.set(usage)
    except Exception as exc:
        print(
            f"WARNING: CPU metric update failed: {exc}"
        )

    return data


# =========================================================
# MEMORY
# =========================================================

@router.get("/memory")
def memory_usage():

    data = SystemMonitor.get_memory_usage()

    percentage = float(
        data.get("percentage", 0)
    )

    try:
        MEMORY_USAGE.set(percentage)
    except Exception as exc:
        print(
            f"WARNING: Memory metric update failed: {exc}"
        )

    return data


# =========================================================
# DISK
# =========================================================

@router.get("/disk")
def disk_usage():

    return SystemMonitor.get_disk_usage()


# =========================================================
# NETWORK
# =========================================================

@router.get("/network")
def network_usage():

    return SystemMonitor.get_network_usage()


# =========================================================
# PROCESSES
# =========================================================

@router.get("/processes")
def processes():

    return SystemMonitor.get_running_processes()