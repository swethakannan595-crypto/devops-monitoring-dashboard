from fastapi import APIRouter, HTTPException
import win32serviceutil


router = APIRouter(
    prefix="/services",
    tags=["Service Control"]
)


# -------------------------------
# Start Service
# -------------------------------

@router.post("/start/{service_name}")
def start_service(service_name: str):

    try:

        win32serviceutil.StartService(service_name)

        return {
            "message": f"{service_name} started successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



# -------------------------------
# Stop Service
# -------------------------------

@router.post("/stop/{service_name}")
def stop_service(service_name: str):

    try:

        win32serviceutil.StopService(service_name)

        return {
            "message": f"{service_name} stopped successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



# -------------------------------
# Restart Service
# -------------------------------

@router.post("/restart/{service_name}")
def restart_service(service_name: str):

    try:

        win32serviceutil.RestartService(service_name)

        return {
            "message": f"{service_name} restarted successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 