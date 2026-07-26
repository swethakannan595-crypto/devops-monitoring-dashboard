import time

from prometheus_client import (
    Gauge,
    Counter,
    Histogram
)

# ==========================================
# Application Start Time
# ==========================================

APP_START_TIME = time.time()

# ==========================================
# System Metrics
# ==========================================

CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "Current CPU Usage Percentage"
)

MEMORY_USAGE = Gauge(
    "system_memory_usage_percent",
    "Current Memory Usage Percentage"
)

DISK_USAGE = Gauge(
    "system_disk_usage_percent",
    "Current Disk Usage Percentage"
)

NETWORK_BYTES_SENT = Gauge(
    "system_network_bytes_sent",
    "Network Bytes Sent"
)

NETWORK_BYTES_RECEIVED = Gauge(
    "system_network_bytes_received",
    "Network Bytes Received"
)

RUNNING_PROCESSES = Gauge(
    "system_running_processes",
    "Total Running Processes"
)

# ==========================================
# API Metrics
# ==========================================

# ==========================================
# API Metrics
# ==========================================

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"]
)

# ==========================================
# Docker Metrics
# ==========================================

RUNNING_CONTAINERS = Gauge(
    "docker_running_containers",
    "Number of Running Docker Containers"
)

TOTAL_CONTAINERS = Gauge(
    "docker_total_containers",
    "Total Docker Containers"
)

# ==========================================
# Application Metrics
# ==========================================

APPLICATION_UPTIME = Gauge(
    "application_uptime_seconds",
    "Application Uptime in Seconds"
)