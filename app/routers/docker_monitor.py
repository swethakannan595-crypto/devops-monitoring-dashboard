from fastapi import APIRouter
import docker
from docker.errors import DockerException


router = APIRouter(
    prefix="/docker",
    tags=["Docker Monitoring"]
)


# Docker connection
try:
    client = docker.from_env()
    docker_available = True

except DockerException:
    client = None
    docker_available = False



# Check Docker status
@router.get("/status")
def docker_status():

    if not docker_available:
        return {
            "docker": "Not Running",
            "message": "Docker Desktop is not running"
        }


    return {
        "docker": "Running",
        "version": client.version()["Version"]
    }




# List all containers
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





# Running containers only
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






# Docker Images
@router.get("/images")
def docker_images():


    if not docker_available:

        return {

            "docker": "Not Running",

            "images": []

        }



    images=[]


    for image in client.images.list():

        images.append({

            "id": image.short_id,

            "tags": image.tags

        })



    return {

        "count":len(images),

        "images":images

    }





# Docker system information
@router.get("/info")
def docker_info():

    if not docker_available:

        return {

            "docker":"Not Running"

        }



    info = client.info()



    return {

        "containers":info["Containers"],

        "running":info["ContainersRunning"],

        "paused":info["ContainersPaused"],

        "stopped":info["ContainersStopped"],

        "images":info["Images"],

        "driver":info["Driver"],

        "operating_system":info["OperatingSystem"],

        "architecture":info["Architecture"],

        "cpus":info["NCPU"],

        "memory":info["MemTotal"]

    }