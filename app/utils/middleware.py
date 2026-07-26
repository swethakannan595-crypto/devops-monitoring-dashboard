import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.monitoring.prometheus_metrics import (
    HTTP_REQUESTS,
    REQUEST_DURATION
)

from app.utils.uptime import update_uptime


class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        update_uptime()

        response = await call_next(request)

        duration = time.time() - start_time

        HTTP_REQUESTS.labels(
            method=request.method,
            endpoint=request.url.path
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        return response