from fastapi import APIRouter
import win32service


router = APIRouter(
    prefix="/services",
    tags=["Service Monitoring"]
)


def get_all_services():

    scm = win32service.OpenSCManager(
        None,
        None,
        win32service.SC_MANAGER_ENUMERATE_SERVICE
    )

    try:
        services = win32service.EnumServicesStatus(scm)

        service_list = []

        for service in services:

            status_code = service[2][1]

            if status_code == 4:
                status = "running"

            elif status_code == 1:
                status = "stopped"

            else:
                status = "unknown"

            service_list.append(
                {
                    "service_name": service[0].strip(),
                    "display_name": service[1].strip(),
                    "status": status
                }
            )

        return service_list

    finally:
        win32service.CloseServiceHandle(scm)


# ---------------------------------------
# Get All Services
# ---------------------------------------

@router.get("/")
def list_services():

    services = get_all_services()

    return {
        "total_services": len(services),
        "services": services
    }


# ---------------------------------------
# Running Services
# ---------------------------------------

@router.get("/running")
def running_services():

    services = get_all_services()

    running = [
        service
        for service in services
        if service["status"] == "running"
    ]

    return {
        "running_count": len(running),
        "running_services": running
    }


# ---------------------------------------
# Stopped Services
# ---------------------------------------

@router.get("/stopped")
def stopped_services():

    services = get_all_services()

    stopped = [
        service
        for service in services
        if service["status"] == "stopped"
    ]

    return {
        "stopped_count": len(stopped),
        "stopped_services": stopped
    }


# ---------------------------------------
# Search Services
# ---------------------------------------

@router.get("/search")
def search_services(name: str):

    services = get_all_services()

    search_term = name.strip().lower()

    if not search_term:
        return {
            "count": 0,
            "services": []
        }

    matching_services = [
        service
        for service in services
        if search_term in service["service_name"].lower()
        or search_term in service["display_name"].lower()
    ]

    return {
        "count": len(matching_services),
        "services": matching_services
    }