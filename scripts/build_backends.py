import docker
import os
import docker.errors
import tomli

cwd = os.getcwd()

os.chdir("../flask_backend/models")

model_config_names = {
    "model.toml",
}
docker_config_names = {"dockerfile", "dockerfile.base", "docker_config.toml"}


def get_parent_directories(dir_path):
    parents = dict()
    for parent, dirnames, filenames in os.walk(dir_path):
        if set(filenames).intersection(docker_config_names):
            parents[parent] = sorted(
                list(set(filenames).intersection(docker_config_names))
            )
    return parents


def get_child_model_configs(dir_path):
    model_configs = dict()
    for parent, dirnames, filenames in os.walk(dir_path):
        if set(filenames).intersection(model_config_names):
            model_configs[os.path.basename(parent)] = sorted(
                list(set(filenames).intersection(model_config_names))
            )
    return model_configs


docker_host_locations = get_parent_directories(os.getcwd())


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


def remove_image(client, image_name):
    try:
        image = client.images.get(image_name)
        if image:
            client.images.remove(image_name)
    except docker.errors.ImageNotFound:
        pass
    except Exception as e:
        print(f"WARNING: Docker error: {e}")
        raise


def check_or_build_image(client, image_name, context_path):
    # Don't blow up old image if present
    tmp_cwd = os.getcwd()
    os.chdir(context_path)
    try:
        image = client.images.get(image_name)
    except docker.errors.ImageNotFound:
        image = False
    except Exception as e:
        print(f"WARNING: Docker returned exception: {e}")
    if image:
        print(f"Found base image {image_name}")
    else:
        print(f"Did not find base image name {image_name} - building")
        if os.path.isfile("./dockerfile.base"):
            client.images.build(
                path=".", dockerfile="./dockerfile.base", tag=image_name
            )
        else:
            # Not using old-style build descriptions, ignore this result
            pass
    os.chdir(tmp_cwd)


def build_image(client, image_name, context_path):
    # Blow up old image, then rebuild
    tmp_cwd = os.getcwd()
    os.chdir(context_path)
    try:
        built_image = client.images.get(image_name)
    except docker.errors.ImageNotFound:
        built_image = False
    except Exception as e:
        print(f"WARNING: Docker returned exception: {e}")
    if built_image:
        # Tear down the old image?
        client.images.remove(image_name)
    client.images.build(path=".", dockerfile="./dockerfile", tag=image_name)

    os.chdir(tmp_cwd)


client = docker.from_env()

for docker_path, docker_files in docker_host_locations.items():
    print(f"{docker_path}: {docker_files}")
    os.chdir(docker_path)
    contained_models = get_child_model_configs(docker_path)
    print(f"---> Contained models: {contained_models}")
    for model, config in contained_models.items():
        print(f"\t{model}: {config}")
        # Original definition
        config_path = os.path.join(docker_path, model, config[0])
        # Failover to automated pipeline
        if not os.path.isfile(config_path):
            config_path = os.path.join(docker_path, config[0])
        with open(config_path, "rb") as config_p:
            details = tomli.load(config_p)
        # print(f"\t=====\n{details}\n\t====")
    with open(os.path.join(docker_path, "docker_config.toml"), "rb") as docker_config_p:
        docker_config = tomli.load(docker_config_p)
    image_name = docker_config["basename"]
    base_image_name = image_name + ".base"
    container_name = image_name

    print(f"Now building docker images for {image_name}")
    remove_container(client, container_name)
    check_or_build_image(client, base_image_name, docker_path)
    build_image(client, image_name, docker_path)
    print(f"---> Docker build complete for {image_name} images <---")


os.chdir(cwd)
