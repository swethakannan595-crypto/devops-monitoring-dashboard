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

    # Verify Docker connection
    docker_client.ping()

    print("Prometheus Metrics: Docker connection successful")

except Exception as e:
    docker_client = None

    print(
        "Prometheus Metrics: Docker connection failed:",
        e
    )


# ==========================================================
# Container Memory Detection
# ==========================================================

def get_container_memory_percent():
    """
    Return the current Docker container memory usage
    as a percentage of its configured memory limit.

    Uses Linux cgroup information available inside Docker.
    """

    try:

        # --------------------------------------------------
        # cgroup v2
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
                        current /
                        maximum *
                        100
                    )


        # --------------------------------------------------
        # cgroup v1
        # --------------------------------------------------

        memory_usage = Path(
            "/sys/fs/cgroup/memory/memory.usage_in_bytes"
        )

        memory_limit = Path(
            "/sys/fs/cgroup/memory/memory.limit_in_bytes"
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
                    current /
                    maximum *
                    100
                )

    except Exception as e:

        print(
            "Container memory detection error:",
            e
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

                # Fallback for non-Docker execution
                MEMORY_USAGE.set(
                    psutil.virtual_memory().percent
                )


            # --------------------------------------------------
            # Disk
            # --------------------------------------------------

            try:

                disk = psutil.disk_usage(
                    "/"
                )

            except Exception:

                disk = psutil.disk_usage(
                    "C:\\"
                )

            DISK_USAGE.set(
                disk.percent
            )


            # --------------------------------------------------
            # Network
            # --------------------------------------------------

            network = psutil.net_io_counters()

            NETWORK_BYTES_SENT.set(
                network.bytes_sent
            )

            NETWORK_BYTES_RECEIVED.set(
                network.bytes_recv
            )


            # --------------------------------------------------
            # Processes
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
                        docker_client.containers.list(
                            all=True
                        )
                    )

                    running_containers = (
                        docker_client.containers.list()
                    )

                    TOTAL_CONTAINERS.set(
                        len(all_containers)
                    )

                    RUNNING_CONTAINERS.set(
                        len(running_containers)
                    )

                except Exception as e:

                    print(
                        "Docker metrics error:",
                        e
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
                time.time() -
                APP_START_TIME
            )


            # --------------------------------------------------
            # Debug Output
            # --------------------------------------------------

            print(
                f"Metrics updated | "
                f"CPU={cpu:.1f}% | "
                f"Memory={MEMORY_USAGE._value.get():.1f}% | "
                f"Disk={DISK_USAGE._value.get():.1f}%"
            )


        except Exception as e:

            print(
                "Metrics Error:",
                e
            )


        # Update every 5 seconds

        time.sleep(5)


# ==========================================================
# Start Background Metrics Thread
# ==========================================================

thread = threading.Thread(
    target=update_metrics,
    daemon=True
)

thread.start()

print(
    "Prometheus Metrics: "
    "Background metrics thread started"
)