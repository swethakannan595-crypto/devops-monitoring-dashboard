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
# Docker Container CPU Metrics
# ==========================================================

CONTAINER_CPU_USAGE = Gauge(
    "docker_container_cpu_percent",
    "Docker Container CPU Usage Percentage",
    ["container"],
)


# ==========================================================
# Docker Container Memory Metrics
# ==========================================================

CONTAINER_MEMORY_USAGE = Gauge(
    "docker_container_memory_percent",
    "Docker Container Memory Usage Percentage",
    ["container"],
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
# Docker Container CPU Calculation
# ==========================================================

def calculate_container_cpu_percent(stats):

    try:

        cpu_stats = stats.get(
            "cpu_stats",
            {}
        )

        previous_cpu_stats = stats.get(
            "precpu_stats",
            {}
        )

        cpu_usage = cpu_stats.get(
            "cpu_usage",
            {}
        )

        previous_cpu_usage = (
            previous_cpu_stats.get(
                "cpu_usage",
                {}
            )
        )

        total_usage = cpu_usage.get(
            "total_usage",
            0
        )

        previous_total_usage = (
            previous_cpu_usage.get(
                "total_usage",
                0
            )
        )

        system_usage = cpu_stats.get(
            "system_cpu_usage",
            0
        )

        previous_system_usage = (
            previous_cpu_stats.get(
                "system_cpu_usage",
                0
            )
        )

        cpu_delta = (
            total_usage
            - previous_total_usage
        )

        system_delta = (
            system_usage
            - previous_system_usage
        )

        if (
            cpu_delta <= 0
            or system_delta <= 0
        ):

            return 0.0

        online_cpus = cpu_stats.get(
            "online_cpus"
        )

        if not online_cpus:

            percpu_usage = cpu_usage.get(
                "percpu_usage",
                []
            )

            online_cpus = (
                len(percpu_usage)
                if percpu_usage
                else 1
            )

        cpu_percent = (
            cpu_delta
            / system_delta
            * online_cpus
            * 100.0
        )

        return round(
            cpu_percent,
            2
        )

    except Exception as exc:

        print(
            "Docker CPU calculation error:",
            exc
        )

        return 0.0


# ==========================================================
# Docker Container Memory Calculation
# ==========================================================

def calculate_container_memory_percent(stats):

    try:

        memory_stats = stats.get(
            "memory_stats",
            {}
        )

        usage = memory_stats.get(
            "usage",
            0
        )

        limit = memory_stats.get(
            "limit",
            0
        )

        if limit <= 0:

            return 0.0

        memory_percent = (
            usage
            / limit
            * 100.0
        )

        return round(
            memory_percent,
            2
        )

    except Exception as exc:

        print(
            "Docker memory calculation error:",
            exc
        )

        return 0.0


# ==========================================================
# Update Docker Container Metrics
# ==========================================================

def update_docker_container_metrics(
    running_containers
):

    if not running_containers:

        return

    active_container_names = set()

    for container in running_containers:

        try:

            container_name = (
                container.name
            )

            active_container_names.add(
                container_name
            )

            stats = container.stats(
                stream=False
            )

            # ----------------------------------------------
            # CPU
            # ----------------------------------------------

            cpu_percent = (
                calculate_container_cpu_percent(
                    stats
                )
            )

            CONTAINER_CPU_USAGE.labels(
                container=container_name
            ).set(
                cpu_percent
            )

            # ----------------------------------------------
            # Memory
            # ----------------------------------------------

            memory_percent = (
                calculate_container_memory_percent(
                    stats
                )
            )

            CONTAINER_MEMORY_USAGE.labels(
                container=container_name
            ).set(
                memory_percent
            )

        except Exception as exc:

            print(
                "Docker container metric error "
                f"for {getattr(container, 'name', 'unknown')}:",
                exc
            )

    # ------------------------------------------------------
    # Remove metrics for containers that are no longer
    # running.
    # ------------------------------------------------------

    try:

        existing_cpu_labels = (
            list(
                CONTAINER_CPU_USAGE._metrics.keys()
            )
        )

        for labels in existing_cpu_labels:

            if labels[0] not in active_container_names:

                CONTAINER_CPU_USAGE.remove(
                    labels[0]
                )

    except Exception:

        pass

    try:

        existing_memory_labels = (
            list(
                CONTAINER_MEMORY_USAGE._metrics.keys()
            )
        )

        for labels in existing_memory_labels:

            if labels[0] not in active_container_names:

                CONTAINER_MEMORY_USAGE.remove(
                    labels[0]
                )

    except Exception:

        pass


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

            CPU_USAGE.set(
                cpu
            )


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

                    # ------------------------------------------
                    # Per-container CPU and Memory
                    # ------------------------------------------

                    update_docker_container_metrics(
                        running_containers
                    )

                except Exception as exc:

                    print(
                        "Docker metrics error:",
                        exc
                    )

                    TOTAL_CONTAINERS.set(
                        0
                    )

                    RUNNING_CONTAINERS.set(
                        0
                    )

            else:

                TOTAL_CONTAINERS.set(
                    0
                )

                RUNNING_CONTAINERS.set(
                    0
                )


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
                f"{DISK_USAGE._value.get():.1f}% | "
                f"Containers="
                f"{RUNNING_CONTAINERS._value.get():.0f}"
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