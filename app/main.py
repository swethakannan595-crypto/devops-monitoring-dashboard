from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from prometheus_fastapi_instrumentator import Instrumentator

import psutil
import time

# ==========================================================
# Routers
# ==========================================================

from app.api.docker import router as docker_router

# ==========================================================
# Custom Prometheus Metrics
# ==========================================================

from app.monitoring import prometheus_metrics


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="DevOps Monitoring Dashboard",
    version="1.0.0"
)


# ==========================================================
# Prometheus Instrumentation
# ==========================================================

Instrumentator().instrument(app).expose(app)


# ==========================================================
# Templates
# ==========================================================

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================================
# Include Routers
# ==========================================================

app.include_router(
    docker_router
)


# ==========================================================
# Home
# ==========================================================

@app.get("/")
async def home():

    return {
        "message":
            "DevOps Monitoring Dashboard API Running",

        "status":
            "success"
    }


# ==========================================================
# Dashboard
# ==========================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ==========================================================
# System Monitoring
# ==========================================================

@app.get("/api/system")
async def system_monitor():

    # ------------------------------------------------------
    # CPU
    # ------------------------------------------------------

    cpu_usage = psutil.cpu_percent(
        interval=1
    )

    cpu_frequency = psutil.cpu_freq()

    # ------------------------------------------------------
    # Memory
    # ------------------------------------------------------

    memory = psutil.virtual_memory()

    # ------------------------------------------------------
    # Disk
    #
    # "/" works inside Linux/Docker.
    # "C:\\" is used when running directly on Windows.
    # ------------------------------------------------------

    try:

        disk_path = "/"

        if hasattr(psutil, "WINDOWS"):

            disk_path = "C:\\"

        disk = psutil.disk_usage(
            disk_path
        )

    except Exception:

        disk = psutil.disk_usage("/")


    # ------------------------------------------------------
    # Network
    # ------------------------------------------------------

    network = psutil.net_io_counters()


    # ------------------------------------------------------
    # Response
    # ------------------------------------------------------

    return {

        "cpu": {

            "usage":
                cpu_usage,

            "physical_cores":
                psutil.cpu_count(
                    logical=False
                ),

            "logical_cores":
                psutil.cpu_count(
                    logical=True
                ),

            "frequency_mhz":
                round(
                    cpu_frequency.current,
                    2
                )
                if cpu_frequency
                else None,

            "unit":
                "%"
        },


        "memory": {

            "total_gb":
                round(
                    memory.total /
                    (1024 ** 3),
                    2
                ),

            "used_gb":
                round(
                    memory.used /
                    (1024 ** 3),
                    2
                ),

            "available_gb":
                round(
                    memory.available /
                    (1024 ** 3),
                    2
                ),

            "percentage":
                memory.percent
        },


        "disk": {

            "total_gb":
                round(
                    disk.total /
                    (1024 ** 3),
                    2
                ),

            "used_gb":
                round(
                    disk.used /
                    (1024 ** 3),
                    2
                ),

            "free_gb":
                round(
                    disk.free /
                    (1024 ** 3),
                    2
                ),

            "percentage":
                disk.percent
        },


        "network": {

            "bytes_sent":
                network.bytes_sent,

            "bytes_received":
                network.bytes_recv,

            "packets_sent":
                network.packets_sent,

            "packets_received":
                network.packets_recv
        },


        "timestamp":
            time.time()
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }