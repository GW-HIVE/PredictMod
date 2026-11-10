#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_DIR="$SCRIPT_DIR/../flask_backend/models"

# Parse a bare string value from a TOML file: key = "value"
toml_get() {
    local file="$1" key="$2"
    grep "^${key}" "$file" | sed 's/^[^=]*= *"\(.*\)"/\1/'
}

# Find all docker host directories (those containing docker_config.toml),
# excluding the new_model_examples tree.
while IFS= read -r docker_config; do
    docker_path="$(dirname "$docker_config")"

    image_name="$(toml_get "$docker_config" basename)"
    if [[ -z "$image_name" ]]; then
        echo "WARNING: No 'basename' found in $docker_config — skipping"
        continue
    fi
    base_image_name="${image_name}.base"
    container_name="$image_name"

    echo "=== $docker_path ==="

    # List contained models (subdirs with model.toml), excluding 'example' dirs.
    while IFS= read -r model_toml; do
        model_name="$(basename "$(dirname "$model_toml")")"
        echo "  model: $model_name"
    done < <(find "$docker_path" -name "model.toml" -not -path "*/example/*")

    # Remove any existing container.
    if docker ps -a --format '{{.Names}}' | grep -qx "$container_name"; then
        echo "  Stopping and removing container: $container_name"
        docker stop "$container_name"
        docker rm   "$container_name"
    fi

    # Build base image only if it is absent (non-destructive).
    if [[ -f "$docker_path/dockerfile.base" ]]; then
        if docker image inspect "$base_image_name" &>/dev/null; then
            echo "  Found base image: $base_image_name"
        else
            echo "  Building base image: $base_image_name"
            docker build -t "$base_image_name" -f "$docker_path/dockerfile.base" "$docker_path"
        fi
    fi

    # Remove old image and do a fresh build.
    if docker image inspect "$image_name" &>/dev/null; then
        echo "  Removing old image: $image_name"
        docker rmi "$image_name"
    fi

    if [[ -f "$docker_path/dockerfile" ]]; then
        echo "  Building image: $image_name"
        docker build -t "$image_name" -f "$docker_path/dockerfile" "$docker_path"
        echo "  --> build complete for $image_name <--"
    else
        echo "  WARNING: No dockerfile in $docker_path — skipping build"
    fi

done < <(find "$MODELS_DIR" -name "docker_config.toml" -not -path "*/new_model_examples/*")
