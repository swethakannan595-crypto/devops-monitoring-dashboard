from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

import psutil
import time

# IMPORTANT: Import custom Prometheus metrics
from app.monitoring import prometheus_metrics

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

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")
    network = psutil.net_io_counters()

    return {
        "cpu": {
            "usage": cpu,
            "unit": "%",
        },
        "memory": {
            "total": round(memory.total / (1024**3), 2),
            "used": round(memory.used / (1024**3), 2),
            "percentage": memory.percent,
        },
        "disk": {
            "total": round(disk.total / (1024**3), 2),
            "used": round(disk.used / (1024**3), 2),
            "percentage": disk.percent,
        },
        "network": {
            "sent": round(network.bytes_sent / (1024**2), 2),
            "received": round(network.bytes_recv / (1024**2), 2),
        },
        "timestamp": time.time(),
    }

# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }