#!/usr/bin/env bash
#
# docker-all-down.sh — Tear down the full SDLC Intelligent App local stack.
#
# Usage:
#   cicd/Local/docker-all-down.sh                 # stop & remove containers/networks
#   cicd/Local/docker-all-down.sh --volumes       # also remove named volumes (DELETES DATA)
#   cicd/Local/docker-all-down.sh [extra args...]
#
# Environment overrides:
#   COMPOSE_FILE   Path to the compose file (default: infra/docker-compose.yml)
#   PROJECT_NAME   Compose project name (default: sdlc-intelligent-app)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

PROJECT_NAME="${PROJECT_NAME:-sdlc-intelligent-app}"
COMPOSE_FILE="${COMPOSE_FILE:-${REPO_ROOT}/infra/docker-compose.yml}"

if docker compose version >/dev/null 2>&1; then
  DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  DC=(docker-compose)
else
  echo "ERROR: Docker Compose not found. Install Docker Desktop or the compose plugin." >&2
  exit 1
fi

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "ERROR: Compose file not found at: ${COMPOSE_FILE}" >&2
  echo "       Add infra/docker-compose.yml, or set COMPOSE_FILE=/path/to/docker-compose.yml" >&2
  exit 1
fi

echo ">> Stopping stack '${PROJECT_NAME}'"
echo "   compose file: ${COMPOSE_FILE}"
"${DC[@]}" -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" down "$@"

echo ">> Stack stopped."
