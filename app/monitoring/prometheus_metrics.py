# app/monitoring/prometheus_metrics.py

import threading
import time
from pathlib import Path

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
    "Number of Running Docker Containers",
)

TOTAL_CONTAINERS = Gauge(
    "docker_total_containers",
    "Total Number of Docker Containers",
)


# ==========================================================
# Application Metrics
# ==========================================================

APPLICATION_UPTIME = Gauge(
    "application_uptime_seconds",
    "Application Uptime in Seconds",
)


# ==========================================================
# Docker Client
# ==========================================================

try:

    docker_client = docker.from_env()

    docker_client.ping()

    print(
        "Prometheus Metrics: "
        "Docker connection successful"
    )

except Exception as exc:

    docker_client = None

    print(
        "Prometheus Metrics: "
        f"Docker connection failed: {exc}"
    )


# ==========================================================
# Container Memory Detection
# ==========================================================

def get_container_memory_percent():

    try:

        # --------------------------------------------------
        # Docker / Linux cgroup v2
        # --------------------------------------------------

        memory_current = Path(
            "/sys/fs/cgroup/memory.current"
        )

        memory_max = Path(
            "/sys/fs/cgroup/memory.max"
        )

        if (
            memory_current.exists()
            and memory_max.exists()
        ):

            current = int(
                memory_current.read_text().strip()
            )

            maximum_text = (
                memory_max.read_text().strip()
            )

            if maximum_text != "max":

                maximum = int(maximum_text)

                if maximum > 0:

                    return (
                        current
                        / maximum
                        * 100
                    )

        # --------------------------------------------------
        # Docker / Linux cgroup v1
        # --------------------------------------------------

        memory_usage = Path(
            "/sys/fs/cgroup/memory/"
            "memory.usage_in_bytes"
        )

        memory_limit = Path(
            "/sys/fs/cgroup/memory/"
            "memory.limit_in_bytes"
        )

        if (
            memory_usage.exists()
            and memory_limit.exists()
        ):

            current = int(
                memory_usage.read_text().strip()
            )

            maximum = int(
                memory_limit.read_text().strip()
            )

            if maximum > 0:

                return (
                    current
                    / maximum
                    * 100
                )

    except Exception as exc:

        print(
            "Container memory detection error:",
            exc
        )

    return None


# ==========================================================
# Update Metrics
# ==========================================================

def update_metrics():

    while True:

        try:

            # --------------------------------------------------
            # CPU
            # --------------------------------------------------

            cpu = psutil.cpu_percent(
                interval=1
            )

            CPU_USAGE.set(cpu)


            # --------------------------------------------------
            # Memory
            # --------------------------------------------------

            container_memory = (
                get_container_memory_percent()
            )

            if container_memory is not None:

                MEMORY_USAGE.set(
                    container_memory
                )

            else:

                MEMORY_USAGE.set(
                    psutil.virtual_memory().percent
                )


            # --------------------------------------------------
            # Disk
            # --------------------------------------------------

            if psutil.WINDOWS:

                disk = psutil.disk_usage(
                    "C:\\"
                )

            else:

                disk = psutil.disk_usage(
                    "/"
                )

            DISK_USAGE.set(
                disk.percent
            )


            # --------------------------------------------------
            # Network
            # --------------------------------------------------

            network = psutil.net_io_counters()

            if network:

                NETWORK_BYTES_SENT.set(
                    network.bytes_sent
                )

                NETWORK_BYTES_RECEIVED.set(
                    network.bytes_recv
                )


            # --------------------------------------------------
            # Running Processes
            # --------------------------------------------------

            RUNNING_PROCESSES.set(
                len(psutil.pids())
            )


            # --------------------------------------------------
            # Docker Containers
            # --------------------------------------------------

            if docker_client:

                try:

                    all_containers = (
                        docker_client
                        .containers
                        .list(all=True)
                    )

                    running_containers = (
                        docker_client
                        .containers
                        .list()
                    )

                    TOTAL_CONTAINERS.set(
                        len(all_containers)
                    )

                    RUNNING_CONTAINERS.set(
                        len(running_containers)
                    )

                except Exception as exc:

                    print(
                        "Docker metrics error:",
                        exc
                    )

                    TOTAL_CONTAINERS.set(0)

                    RUNNING_CONTAINERS.set(0)

            else:

                TOTAL_CONTAINERS.set(0)

                RUNNING_CONTAINERS.set(0)


            # --------------------------------------------------
            # Application Uptime
            # --------------------------------------------------

            APPLICATION_UPTIME.set(
                time.time()
                - APP_START_TIME
            )


            # --------------------------------------------------
            # Debug Output
            # --------------------------------------------------

            print(
                "Metrics updated | "
                f"CPU={cpu:.1f}% | "
                f"Memory="
                f"{MEMORY_USAGE._value.get():.1f}% | "
                f"Disk="
                f"{DISK_USAGE._value.get():.1f}%"
            )

        except Exception as exc:

            print(
                "Metrics Error:",
                exc
            )

        # --------------------------------------------------
        # Update every 5 seconds
        # --------------------------------------------------

        time.sleep(5)


# ==========================================================
# Initialize Metrics
# ==========================================================

_metrics_started = False


def initialize_metrics():

    global _metrics_started

    if _metrics_started:

        return

    _metrics_started = True

    thread = threading.Thread(
        target=update_metrics,
        daemon=True,
        name="prometheus-metrics",
    )

    thread.start()

    print(
        "Prometheus Metrics: "
        "Background metrics thread started"
    )