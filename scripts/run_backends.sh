#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREDICTMOD_HOME_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MODELS_DIR="$PREDICTMOD_HOME_DIR/flask_backend/models"

# Parse a bare string value from a TOML file: key = "value"
toml_get() {
    local file="$1" key="$2"
    grep "^${key}" "$file" | sed 's/^[^=]*= *"\(.*\)"/\1/'
}

while IFS= read -r docker_config; do
    image_name="$(toml_get "$docker_config" basename)"
    if [[ -z "$image_name" ]]; then
        echo "WARNING: No 'basename' found in $docker_config — skipping"
        continue
    fi
    container_name="$image_name"

    echo "=== $(dirname "$docker_config") ==="

    # Stop and remove any existing container with this name.
    if docker ps -a --format '{{.Names}}' | grep -qx "$container_name"; then
        echo "  Stopping and removing container: $container_name"
        docker stop "$container_name" >/dev/null
        docker rm   "$container_name" >/dev/null
    fi

    echo "  Starting container: $container_name (image: $image_name)"
    docker run \
        --name "$container_name" \
        --network predictmod \
        --volume "$PREDICTMOD_HOME_DIR/user_data:/user_data:rw" \
        --restart always \
        --detach \
        "$image_name"
    echo "  --> started $container_name <--"

done < <(find "$MODELS_DIR" -name "docker_config.toml" -not -path "*/new_model_examples/*")
