import docker
from docker.errors import DockerException


class DockerMonitor:

    def get_client(self):
        try:
            return docker.from_env()
        except DockerException:
            return None

    def get_all_containers(self):
        client = self.get_client()

        if client is None:
            return {
                "status": "error",
                "message": "Docker Desktop is not running or not installed."
            }

        containers = client.containers.list(all=True)

        return [
            {
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags
            }
            for c in containers
        ]

    def get_running_containers(self):
        client = self.get_client()

        if client is None:
            return {
                "status": "error",
                "message": "Docker Desktop is not running or not installed."
            }

        containers = client.containers.list()

        return [
            {
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags
            }
            for c in containers
        ]

    def docker_info(self):
        client = self.get_client()

        if client is None:
            return {
                "status": "error",
                "message": "Docker Desktop is not running or not installed."
            }

        return client.info()