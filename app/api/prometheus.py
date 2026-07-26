from fastapi import APIRouter
from fastapi.responses import Response

from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST
)

router = APIRouter(
    prefix="/metrics",
    tags=["Prometheus"]
)


@router.get("")
def metrics():

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@router.get("/status")
def status():

    return {
        "status": "Running",
        "metrics": "Enabled",
        "dashboard": "Grafana Ready"
    }