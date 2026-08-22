from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.monitoring import router as monitoring_router
from app.api.docker import router as docker_router
from app.routers.processes import router as process_router
from app.routers.service_monitor import router as service_router

from app.monitoring.prometheus_metrics import initialize_metrics


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="DevOps Monitoring Dashboard",
    description=(
        "Real-time system, Docker, process, service "
        "and Prometheus monitoring"
    ),
    version="1.0.0",
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(monitoring_router)
print("Monitoring router loaded successfully")

app.include_router(docker_router)
print("Docker router loaded successfully")

app.router.routes.extend(process_router.routes)
print("Process router loaded successfully")


print("Service monitoring router loaded successfully")


# =========================================================
# PROMETHEUS METRICS INITIALIZATION
# =========================================================
app.router.routes.extend(service_router.routes)
initialize_metrics()

print("Prometheus metrics initialized")


# =========================================================
# ROOT
# =========================================================

@app.get(
    "/",
    include_in_schema=False
)
async def root():

    return RedirectResponse(
        url="/dashboard",
        status_code=307
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.get(
    "/dashboard",
    include_in_schema=False
)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get(
    "/health",
    include_in_schema=False
)
def health():

    return {
        "status": "healthy",
        "service": "devops-monitor-dashboard"
    }


# =========================================================
# APPLICATION INFORMATION
# =========================================================

@app.get(
    "/api/info"
)
def application_info():

    return {
        "name": "DevOps Monitoring Dashboard",
        "version": "1.0.0",
        "framework": "FastAPI",
        "monitoring": "Prometheus",
        "containerization": "Docker"
    }


# =========================================================
# PROMETHEUS METRICS
# =========================================================

@app.get(
    "/metrics",
    include_in_schema=False
)
def metrics():

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )