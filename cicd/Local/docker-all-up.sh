#!/usr/bin/env bash
#
# docker-all-up.sh — Bring up the full SDLC Intelligent App local stack.
#
# Usage:
#   cicd/Local/docker-all-up.sh [extra docker-compose args...]
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

# Detect Docker Compose: v2 plugin ("docker compose") or v1 ("docker-compose").
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

echo ">> Starting stack '${PROJECT_NAME}'"
echo "   compose file: ${COMPOSE_FILE}"
"${DC[@]}" -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" up -d --build "$@"

echo ">> Stack is starting. Check status with:"
echo "   cicd/Local/docker-all-status.sh"
