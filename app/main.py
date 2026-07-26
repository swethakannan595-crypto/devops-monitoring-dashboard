from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from prometheus_fastapi_instrumentator import Instrumentator

# API Routers
from app.api.monitoring import router as monitoring_router
from app.api.prometheus import router as prometheus_router
from app.api.dashboard import router as dashboard_router
from app.api.process import router as process_router

# Monitoring Routers
from app.routers import docker_monitor
from app.routers import service_monitor
from app.routers import service_control
from app.routers import processes

# Middleware
from app.utils.middleware import MetricsMiddleware


# ==================================================
# Create FastAPI Application
# ==================================================

app = FastAPI(
    title="DevOps Monitoring Dashboard",
    version="1.0.0",
    description="A real-time DevOps monitoring dashboard built with FastAPI, Prometheus, and Grafana."
)


# ==================================================
# Middleware
# ==================================================

app.add_middleware(MetricsMiddleware)


# ==================================================
# Static Files
# ==================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ==================================================
# Templates
# ==================================================

templates = Jinja2Templates(
    directory="templates"
)


# ==================================================
# API Routers
# ==================================================

# System Monitoring
app.include_router(
    monitoring_router
)


# Docker Monitoring
app.include_router(
    docker_monitor.router
)


# Prometheus
app.include_router(
    prometheus_router
)


# Dashboard
app.include_router(
    dashboard_router
)


# Process Monitoring
app.include_router(
    process_router
)


# Service Monitoring
app.include_router(
    service_monitor.router
)

app.include_router(
    service_control.router
)

app.include_router(processes.router)

# ==================================================
# Prometheus Metrics Endpoint
# ==================================================

Instrumentator().instrument(app).expose(app)


# ==================================================
# Home API
# ==================================================

@app.get("/", tags=["Home"])
def home():

    return {
        "message": "Welcome to DevOps Monitoring Dashboard",
        "dashboard": "/dashboard",
        "docs": "/docs",
        "metrics": "/metrics",
        "health": "/health"
    }


# ==================================================
# Health Check
# ==================================================

@app.get("/health", tags=["Health"])
def health():

    return {
        "status": "Healthy",
        "application": "DevOps Monitoring Dashboard",
        "version": "1.0.0"
    }


# ==================================================
# Dashboard Page
# ==================================================

@app.get("/dashboard", tags=["Dashboard"])
def dashboard(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )