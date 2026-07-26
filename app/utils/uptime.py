import time

from app.monitoring.prometheus_metrics import (
    APPLICATION_UPTIME,
    APP_START_TIME
)


def update_uptime():
    uptime = time.time() - APP_START_TIME
    APPLICATION_UPTIME.set(uptime)