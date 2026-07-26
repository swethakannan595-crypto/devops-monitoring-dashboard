from fastapi import APIRouter

from app.monitoring.system_monitor import SystemMonitor
from app.monitoring.prometheus_metrics import CPU_USAGE, MEMORY_USAGE

router = APIRouter(
    prefix="/monitor",
    tags=["System Monitoring"]
)


@router.get("/cpu")
def cpu_usage():
    data = SystemMonitor.get_cpu_usage()

    CPU_USAGE.set(data["cpu_usage"])

    return data


@router.get("/memory")
def memory_usage():
    data = SystemMonitor.get_memory_usage()

    MEMORY_USAGE.set(data["percent"])

    return data


@router.get("/disk")
def disk_usage():
    return SystemMonitor.get_disk_usage()


@router.get("/network")
def network_usage():
    return SystemMonitor.get_network_usage()


@router.get("/system")
def system_info():
    return SystemMonitor.get_system_info()


@router.get("/processes")
def processes():
    return SystemMonitor.get_running_processes()