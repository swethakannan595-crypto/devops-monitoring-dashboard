from fastapi import APIRouter
import psutil


router = APIRouter(
    prefix="/processes",
    tags=["Process Monitoring"]
)


@router.get("/")
def get_processes():

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):

        try:
            processes.append(
                {
                    "pid": process.info["pid"],
                    "name": process.info["name"],
                    "cpu": process.info["cpu_percent"],
                    "memory": round(
                        process.info["memory_percent"],2
                    )
                }
            )

        except:
            pass


    return {
        "total_processes": len(processes),
        "processes": processes
    }