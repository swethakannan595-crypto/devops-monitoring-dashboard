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
                "service_name": service[0],
                "display_name": service[1],
                "status": status
            }
        )

    win32service.CloseServiceHandle(scm)

    return service_list



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