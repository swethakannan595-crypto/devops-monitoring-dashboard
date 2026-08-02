import threading
import time

import docker
import psutil
from prometheus_client import Counter, Gauge, Histogram

# ==========================================================
# Application Start Time
# ==========================================================

APP_START_TIME = time.time()

# ==========================================================
# System Metrics
# ==========================================================

CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "Current CPU Usage Percentage",
)

MEMORY_USAGE = Gauge(
    "system_memory_usage_percent",
    "Current Memory Usage Percentage",
)

DISK_USAGE = Gauge(
    "system_disk_usage_percent",
    "Current Disk Usage Percentage",
)

NETWORK_BYTES_SENT = Gauge(
    "system_network_bytes_sent",
    "Network Bytes Sent",
)

NETWORK_BYTES_RECEIVED = Gauge(
    "system_network_bytes_received",
    "Network Bytes Received",
)

RUNNING_PROCESSES = Gauge(
    "system_running_processes",
    "Total Running Processes",
)

# ==========================================================
# API Metrics
# ==========================================================

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"],
)

# ==========================================================
# Docker Metrics
# ==========================================================

RUNNING_CONTAINERS = Gauge(
    "docker_running_containers",
    "Running Docker Containers",
)

TOTAL_CONTAINERS = Gauge(
    "docker_total_containers",
    "Total Docker Containers",
)

# ==========================================================
# Application Metrics
# ==========================================================

APPLICATION_UPTIME = Gauge(
    "application_uptime_seconds",
    "Application Uptime",
)

# ==========================================================
# Docker Client
# ==========================================================

try:
    docker_client = docker.from_env()
except Exception:
    docker_client = None


# ==========================================================
# Update Metrics
# ==========================================================

def update_metrics():
    while True:
        try:
            # CPU
            CPU_USAGE.set(psutil.cpu_percent(interval=1))

            # Memory
            MEMORY_USAGE.set(psutil.virtual_memory().percent)

            # Disk
            DISK_USAGE.set(psutil.disk_usage("C:\\").percent)

            # Network
            net = psutil.net_io_counters()

            NETWORK_BYTES_SENT.set(net.bytes_sent)
            NETWORK_BYTES_RECEIVED.set(net.bytes_recv)

            # Processes
            RUNNING_PROCESSES.set(len(psutil.pids()))

            # Docker
            if docker_client:
                TOTAL_CONTAINERS.set(
                    len(docker_client.containers.list(all=True))
                )

                RUNNING_CONTAINERS.set(
                    len(docker_client.containers.list())
                )
            else:
                TOTAL_CONTAINERS.set(0)
                RUNNING_CONTAINERS.set(0)

            # Uptime
            APPLICATION_UPTIME.set(
                time.time() - APP_START_TIME
            )

        except Exception as e:
            print("Metrics Error:", e)

        time.sleep(5)


# ==========================================================
# Start Background Thread
# ==========================================================

thread = threading.Thread(
    target=update_metrics,
    daemon=True,
)

thread.start()