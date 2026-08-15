from fastapi import APIRouter
import psutil

router = APIRouter(
    prefix="/api/processes",
    tags=["Process Monitoring"]
)


@router.get("")
async def get_processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "status", "memory_percent", "cpu_percent"]
    ):
        try:
            processes.append({
                "pid": process.info["pid"],
                "name": process.info["name"],
                "status": process.info["status"],
                "cpu_percent": round(
                    process.info["cpu_percent"] or 0, 2
                ),
                "memory_percent": round(
                    process.info["memory_percent"] or 0, 2
                )
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return {
        "count": len(processes),
        "processes": processes
    }