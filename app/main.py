from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

from app.monitoring import prometheus_metrics
from app.monitoring.system_monitor import SystemMonitor
from app.api.docker import router as docker_router

import time


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="DevOps Monitoring Dashboard",
    version="1.0.0",
)


# ==========================================================
# Prometheus Metrics
# ==========================================================

Instrumentator().instrument(app).expose(app)


# ==========================================================
# Templates
# ==========================================================

templates = Jinja2Templates(directory="templates")


# ==========================================================
# Docker Monitoring Routes
# ==========================================================

app.include_router(
    docker_router,
    prefix="/docker",
    tags=["Docker Monitoring"],
)


# ==========================================================
# Home
# ==========================================================

@app.get("/")
async def home():
    return {
        "message": "DevOps Monitoring Dashboard API Running",
        "status": "success",
    }


# ==========================================================
# Dashboard
# ==========================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# ==========================================================
# System Monitoring API
# ==========================================================

@app.get("/api/system")
async def system_monitor():

    cpu = SystemMonitor.get_cpu_usage()
    memory = SystemMonitor.get_memory_usage()
    disk = SystemMonitor.get_disk_usage()
    network = SystemMonitor.get_network_usage()

    return {
        "cpu": {
            "usage": cpu["cpu_usage"],
            "physical_cores": cpu["physical_cores"],
            "logical_cores": cpu["logical_cores"],
            "frequency_mhz": cpu["cpu_frequency"],
            "unit": "%",
        },

        "memory": {
            "total_gb": memory["total"],
            "used_gb": memory["used"],
            "available_gb": memory["available"],
            "percentage": memory["percent"],
        },

        "disk": {
            "total_gb": disk["total"],
            "used_gb": disk["used"],
            "free_gb": disk["free"],
            "percentage": disk["percent"],
        },

        "network": {
            "bytes_sent": network["bytes_sent"],
            "bytes_received": network["bytes_received"],
            "packets_sent": network["packets_sent"],
            "packets_received": network["packets_received"],
        },

        "timestamp": time.time(),
    }


# ==========================================================
# System Information
# ==========================================================

@app.get("/api/system/info")
async def system_info():
    return SystemMonitor.get_system_info()


# ==========================================================
# Running Processes
# ==========================================================

@app.get("/api/system/processes")
async def running_processes():
    processes = SystemMonitor.get_running_processes()

    return {
        "count": len(processes),
        "processes": processes,
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }