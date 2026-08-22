from fastapi import APIRouter, Query
import psutil


router = APIRouter(
    prefix="/processes",
    tags=["Process Monitoring"]
)


# =========================================================
# GET ALL PROCESSES
# =========================================================

@router.get("/")
def get_processes():

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent",
            "cpu_percent"
        ]
    ):

        try:

            processes.append(
                {
                    "pid": process.info["pid"],

                    "name": process.info["name"] or "Unknown",

                    "status": process.info["status"],

                    "cpu_percent": round(
                        process.info["cpu_percent"] or 0,
                        2
                    ),

                    "memory_percent": round(
                        process.info["memory_percent"] or 0,
                        2
                    )
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return {
        "total_processes": len(processes),
        "processes": processes
    }


# =========================================================
# SEARCH PROCESSES
# =========================================================

@router.get("/search")
def search_processes(
    name: str = Query(
        ...,
        min_length=1,
        description="Process name to search for"
    )
):

    results = []

    search_name = name.lower()

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent",
            "cpu_percent"
        ]
    ):

        try:

            process_name = process.info["name"] or "Unknown"

            if search_name in process_name.lower():

                results.append(
                    {
                        "pid": process.info["pid"],

                        "name": process_name,

                        "status": process.info["status"],

                        "cpu_percent": round(
                            process.info["cpu_percent"] or 0,
                            2
                        ),

                        "memory_percent": round(
                            process.info["memory_percent"] or 0,
                            2
                        )
                    }
                )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return {
        "query": name,
        "count": len(results),
        "processes": results
    }


# =========================================================
# TOP CPU PROCESSES
# =========================================================

@router.get("/top/cpu")
def top_cpu_processes(
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of processes to return"
    )
):

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent",
            "cpu_percent"
        ]
    ):

        try:

            processes.append(
                {
                    "pid": process.info["pid"],

                    "name": process.info["name"] or "Unknown",

                    "status": process.info["status"],

                    "cpu_percent": round(
                        process.info["cpu_percent"] or 0,
                        2
                    ),

                    "memory_percent": round(
                        process.info["memory_percent"] or 0,
                        2
                    )
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    processes.sort(
        key=lambda process: process["cpu_percent"],
        reverse=True
    )

    return {
        "sort_by": "cpu_percent",
        "limit": limit,
        "processes": processes[:limit]
    }


# =========================================================
# TOP MEMORY PROCESSES
# =========================================================

@router.get("/top/memory")
def top_memory_processes(
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of processes to return"
    )
):

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent",
            "cpu_percent"
        ]
    ):

        try:

            processes.append(
                {
                    "pid": process.info["pid"],

                    "name": process.info["name"] or "Unknown",

                    "status": process.info["status"],

                    "cpu_percent": round(
                        process.info["cpu_percent"] or 0,
                        2
                    ),

                    "memory_percent": round(
                        process.info["memory_percent"] or 0,
                        2
                    )
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    processes.sort(
        key=lambda process: process["memory_percent"],
        reverse=True
    )

    return {
        "sort_by": "memory_percent",
        "limit": limit,
        "processes": processes[:limit]
    }

@router.get("/top/cpu")
def top_cpu_processes(
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of processes to return"
    )
):

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent"
        ]
    ):

        try:
            cpu_percent = process.cpu_percent(interval=0.1)

            processes.append(
                {
                    "pid": process.info["pid"],
                    "name": process.info["name"] or "Unknown",
                    "status": process.info["status"],
                    "cpu_percent": round(cpu_percent, 2),
                    "memory_percent": round(
                        process.info["memory_percent"] or 0,
                        2
                    )
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    processes.sort(
        key=lambda process: process["cpu_percent"],
        reverse=True
    )

    return {
        "sort_by": "cpu_percent",
        "limit": limit,
        "processes": processes[:limit]
    }