

#!/usr/bin/env bash
set -euo pipefail

# Determine project root (assuming this script is in web/)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/docker-compose.yml"
OVERRIDE_FILE="${ROOT_DIR}/web/docker-compose.override.yml"

cd "$ROOT_DIR"

docker compose -f "$COMPOSE_FILE" -f "$OVERRIDE_FILE" "$@"