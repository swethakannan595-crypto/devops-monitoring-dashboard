from fastapi import APIRouter

from app.monitoring.system_monitor import SystemMonitor

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def dashboard_stats():

    cpu = SystemMonitor.get_cpu_usage()
    memory = SystemMonitor.get_memory_usage()
    disk = SystemMonitor.get_disk_usage()
    network = SystemMonitor.get_network_usage()

    return {
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "network": network
    }


@router.get("/summary")
def dashboard_summary():

    system = SystemMonitor.get_system_info()

    return {
        "hostname": system["hostname"],
        "os": system["operating_system"],
        "processor": system["processor"],
        "cpu_cores": system["cpu_cores"],
        "logical_processors": system["logical_processors"]
    }