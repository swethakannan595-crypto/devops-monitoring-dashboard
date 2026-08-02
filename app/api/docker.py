from fastapi import APIRouter
import docker
from docker.errors import DockerException

router = APIRouter(
    prefix="/docker",
    tags=["Docker Monitoring"]
)

# ---------------------------------------
# Connect to Docker safely
# ---------------------------------------

try:
    client = docker.from_env()
    docker_available = True
except DockerException:
    client = None
    docker_available = False


# ---------------------------------------
# Docker Status
# ---------------------------------------

@router.get("/status")
def docker_status():
    if not docker_available:
        return {
            "docker": "Not Running",
            "message": "Docker Desktop is not running."
        }

    return {
        "docker": "Running",
        "version": client.version()["Version"]
    }


# ---------------------------------------
# List All Containers
# ---------------------------------------

@router.get("/containers")
def list_containers():

    if not docker_available:
        return {
            "docker": "Not Running",
            "containers": []
        }

    containers = []

    for container in client.containers.list(all=True):

        containers.append({
            "id": container.short_id,
            "name": container.name,
            "image": container.image.tags,
            "status": container.status
        })

    return {
        "count": len(containers),
        "containers": containers
    }


# ---------------------------------------
# Running Containers
# ---------------------------------------

@router.get("/running")
def running_containers():

    if not docker_available:
        return {
            "docker": "Not Running",
            "running_containers": []
        }

    data = []

    for container in client.containers.list():

        data.append({
            "id": container.short_id,
            "name": container.name,
            "status": container.status
        })

    return {
        "count": len(data),
        "running_containers": data
    }


# ---------------------------------------
# Docker Images
# ---------------------------------------

@router.get("/images")
def docker_images():

    if not docker_available:
        return {
            "docker": "Not Running",
            "images": []
        }

    images = []

    for image in client.images.list():

        images.append({
            "id": image.short_id,
            "tags": image.tags
        })

    return {
        "count": len(images),
        "images": images
    }


# ---------------------------------------
# Docker Information
# ---------------------------------------

@router.get("/info")
def docker_info():

    if not docker_available:
        return {
            "docker": "Not Running"
        }

    info = client.info()

    return {
        "containers": info["Containers"],
        "running": info["ContainersRunning"],
        "paused": info["ContainersPaused"],
        "stopped": info["ContainersStopped"],
        "images": info["Images"],
        "driver": info["Driver"],
        "operating_system": info["OperatingSystem"],
        "architecture": info["Architecture"],
        "cpus": info["NCPU"],
        "memory": round(info["MemTotal"] / (1024 ** 3), 2)
    }


# ---------------------------------------
# Docker Container Statistics
# ---------------------------------------

@router.get("/stats")
def docker_stats():

    if not docker_available:
        return {
            "docker": "Not Running",
            "containers": []
        }

    stats_data = []

    for container in client.containers.list():

        try:

            stats = container.stats(stream=False)

            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )

            system_delta = (
                stats["cpu_stats"]["system_cpu_usage"]
                - stats["precpu_stats"]["system_cpu_usage"]
            )

            cpu_percent = 0.0

            if (
                system_delta > 0
                and "percpu_usage"
                in stats["cpu_stats"]["cpu_usage"]
            ):

                cpu_percent = (
                    cpu_delta
                    / system_delta
                ) * len(
                    stats["cpu_stats"]["cpu_usage"]["percpu_usage"]
                ) * 100

            memory_usage = (
                stats["memory_stats"]["usage"]
                / (1024 * 1024)
            )

            memory_limit = (
                stats["memory_stats"]["limit"]
                / (1024 * 1024)
            )

            memory_percent = (
                memory_usage
                / memory_limit
            ) * 100

            network_rx = 0
            network_tx = 0

            if "networks" in stats:

                for net in stats["networks"].values():

                    network_rx += net.get("rx_bytes", 0)
                    network_tx += net.get("tx_bytes", 0)

            stats_data.append({

                "id": container.short_id,

                "name": container.name,

                "image": container.image.tags,

                "status": container.status,

                "cpu_percent": round(cpu_percent, 2),

                "memory_usage_mb": round(memory_usage, 2),

                "memory_limit_mb": round(memory_limit, 2),

                "memory_percent": round(memory_percent, 2),

                "network_rx_mb": round(
                    network_rx / (1024 * 1024), 2
                ),

                "network_tx_mb": round(
                    network_tx / (1024 * 1024), 2
                ),

                "started_at": container.attrs["State"]["StartedAt"]

            })

        except Exception as e:

            stats_data.append({

                "name": container.name,

                "error": str(e)

            })

    return {

        "count": len(stats_data),

        "containers": stats_data

    }