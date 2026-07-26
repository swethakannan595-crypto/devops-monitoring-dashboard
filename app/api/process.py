from fastapi import APIRouter

from app.monitoring.system_monitor import SystemMonitor

router = APIRouter(
    prefix="/process",
    tags=["Process Monitoring"]
)


@router.get("/")
def get_processes():
    return {
        "count": len(SystemMonitor.get_running_processes()),
        "processes": SystemMonitor.get_running_processes()
    }


@router.get("/top10")
def top_processes():

    processes = SystemMonitor.get_running_processes()

    return {
        "count": min(10, len(processes)),
        "processes": processes[:10]
    }