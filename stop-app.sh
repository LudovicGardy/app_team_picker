#!/bin/bash
# Stops the app: removes the containers and the network of the compose project of
# compose.yaml, services of every profile included (a plain `down` leaves them running).
# The data stays: named volumes are never removed here (no `down -v`).
#
# This file is shared by every app: edit it in sotis_pj_template only, then copy it into every app (Apps/CLAUDE.md).
set -euo pipefail
cd "$(dirname "$0")"

if ! docker info >/dev/null 2>&1; then
    echo "Docker ne répond pas : rien à arrêter."
    exit 0
fi

docker compose --profile '*' down --remove-orphans
echo ""
if [ -n "$(docker compose config --volumes)" ]; then
    echo "App arrêtée. Les données restent dans les volumes Docker de l'app."
else
    echo "App arrêtée."
fi
echo "Redémarrer : ./start-app.sh"
