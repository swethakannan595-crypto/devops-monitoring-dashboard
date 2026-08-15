import docker
from fastapi import APIRouter

router = APIRouter(
    prefix="/docker",
    tags=["Docker Monitoring"]
)


def get_docker_client():
    """
    Create a Docker client using the Docker socket
    mounted inside the container.
    """
    return docker.from_env()


# ==========================================================
# Docker Status
# ==========================================================

@router.get("/status")
async def docker_status():

    try:
        client = get_docker_client()

        client.ping()
        version = client.version()

        return {
            "docker": "Running",
            "version": version.get("Version")
        }

    except Exception as e:
        return {
            "docker": "Unavailable",
            "error": str(e)
        }


# ==========================================================
# List All Containers
# ==========================================================

@router.get("/containers")
async def list_containers():

    try:
        client = get_docker_client()

        containers = client.containers.list(
            all=True
        )

        result = []

        for container in containers:
            result.append({
                "id": container.short_id,
                "name": container.name,
                "image": container.image.tags,
                "status": container.status
            })

        return {
            "count": len(result),
            "containers": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================================================
# Running Containers
# ==========================================================

@router.get("/running")
async def running_containers():

    try:
        client = get_docker_client()

        containers = client.containers.list()

        result = []

        for container in containers:
            result.append({
                "id": container.short_id,
                "name": container.name,
                "status": container.status
            })

        return {
            "count": len(result),
            "running_containers": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================================================
# Docker Images
# ==========================================================

@router.get("/images")
async def docker_images():

    try:
        client = get_docker_client()

        images = client.images.list()

        result = []

        for image in images:
            result.append({
                "id": image.short_id,
                "tags": image.tags
            })

        return {
            "count": len(result),
            "images": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================================================
# Docker Information
# ==========================================================

@router.get("/info")
async def docker_info():

    try:
        client = get_docker_client()

        info = client.info()

        memory_gb = round(
            info.get("MemTotal", 0) / (1024 ** 3),
            2
        )

        return {
            "containers": info.get("Containers"),
            "running": info.get("ContainersRunning"),
            "paused": info.get("ContainersPaused"),
            "stopped": info.get("ContainersStopped"),
            "images": info.get("Images"),
            "driver": info.get("Driver"),
            "operating_system": info.get("OperatingSystem"),
            "architecture": info.get("Architecture"),
            "cpus": info.get("NCPU"),
            "memory": memory_gb
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================================================
# Docker Container Statistics
# ==========================================================

@router.get("/stats")
async def docker_stats():

    try:
        client = get_docker_client()

        containers = client.containers.list()

        result = []

        for container in containers:

            stats = container.stats(
                stream=False
            )

            # --------------------------------------------------
            # CPU calculation
            # --------------------------------------------------

            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )

            system_delta = (
                stats["cpu_stats"]["system_cpu_usage"]
                - stats["precpu_stats"]["system_cpu_usage"]
            )

            cpu_percent = 0.0

            if system_delta > 0 and cpu_delta > 0:

                online_cpus = stats["cpu_stats"].get(
                    "online_cpus",
                    1
                )

                cpu_percent = (
                    cpu_delta
                    / system_delta
                    * online_cpus
                    * 100.0
                )

            # --------------------------------------------------
            # Memory
            # --------------------------------------------------

            memory_stats = stats.get(
                "memory_stats",
                {}
            )

            memory_usage = memory_stats.get(
                "usage",
                0
            )

            memory_limit = memory_stats.get(
                "limit",
                0
            )

            memory_usage_mb = round(
                memory_usage / (1024 ** 2),
                2
            )

            memory_limit_mb = round(
                memory_limit / (1024 ** 2),
                2
            )

            memory_percent = 0.0

            if memory_limit > 0:
                memory_percent = round(
                    (memory_usage / memory_limit) * 100,
                    2
                )

            # --------------------------------------------------
            # Network
            # --------------------------------------------------

            network_rx = 0
            network_tx = 0

            networks = stats.get(
                "networks",
                {}
            )

            for network in networks.values():

                network_rx += network.get(
                    "rx_bytes",
                    0
                )

                network_tx += network.get(
                    "tx_bytes",
                    0
                )

            # --------------------------------------------------
            # Result
            # --------------------------------------------------

            result.append({
                "id": container.short_id,
                "name": container.name,
                "image": container.image.tags,
                "status": container.status,

                "cpu_percent": round(
                    cpu_percent,
                    2
                ),

                "memory_usage_mb":
                    memory_usage_mb,

                "memory_limit_mb":
                    memory_limit_mb,

                "memory_percent":
                    memory_percent,

                "network_rx_mb":
                    round(
                        network_rx / (1024 ** 2),
                        2
                    ),

                "network_tx_mb":
                    round(
                        network_tx / (1024 ** 2),
                        2
                    ),

                "started_at":
                    container.attrs[
                        "State"
                    ].get("StartedAt")
            })

        return {
            "count": len(result),
            "containers": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }