import docker
import os
import tomli

from pathlib import Path

cwd = Path(os.getcwd()).resolve()

MODEL_DIR = cwd.parent / "flask_backend/models"
PREDICTMOD_HOME_DIR = cwd.parent

os.chdir(MODEL_DIR)

docker_config_names = {"docker_config.toml"}


def get_parent_directories(dir_path):
    parents = dict()
    for parent, dirnames, filenames in os.walk(dir_path):
        if set(filenames).intersection(docker_config_names):
            parents[parent] = sorted(
                list(set(filenames).intersection(docker_config_names))
            )
    return parents


def start_docker(client, image_name, container_name):
    os.chdir(PREDICTMOD_HOME_DIR)
    client.containers.run(
        image_name,
        name=container_name,
        volumes={
            str(PREDICTMOD_HOME_DIR / "user_data"): {"bind": "/user_data", "mode": "rw"}
        },
        network="predictmod",
        detach=True,
    )
    os.chdir(MODEL_DIR)


def remove_container(client, container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass
    except Exception as e:
        print(f"WARNING: Docker error: {e}")
        raise


# Get the custom backends
docker_targets = get_parent_directories(os.getcwd())
client = docker.from_env()

print(f"Found backend targets: {docker_targets}")
for docker_path, docker_config in docker_targets.items():
    assert len(docker_config) == 1, f"Broken config in {docker_path}. Aborting"
    with open(os.path.join(docker_path, docker_config[0]), "rb") as config_p:
        config = tomli.load(config_p)
    image_name = config["basename"]
    container_name = image_name  # Modify in future as needed
    remove_container(client, container_name)
    start_docker(client, image_name, container_name)

os.chdir(cwd)
