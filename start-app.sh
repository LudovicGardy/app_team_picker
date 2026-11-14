#!/bin/bash
# Starts the app on the Mac: the compose project of compose.yaml is built, started, and
# waited for until every service is healthy (running, for a service without healthcheck);
# then the published URLs are printed. Apps born from the template mount their code: a
# change to a .py file or a template reloads the app without rebuild.
#
# This file is shared by every app: edit it in sotis_pj_template only, then copy it into every app (Apps/CLAUDE.md).
# It names no app and reads everything from compose.yaml: the main URL is the one of the
# `frontend` service when there is one (Django, with its admin), otherwise the first service
# that publishes a port; the database line only shows when a `db` service exists.
# Option: --profile <name> (repeatable) also starts the services of that compose profile.
set -euo pipefail
cd "$(dirname "$0")"

profiles=()
while [ $# -gt 0 ]; do
    case "$1" in
        --profile)
            if [ -z "${2:-}" ]; then echo "--profile attend un nom de profil"; exit 1; fi
            profiles+=("$2")
            shift 2
            ;;
        *) echo "Option inconnue : $1 (seule option : --profile <nom>)"; exit 1 ;;
    esac
done
if [ ${#profiles[@]} -gt 0 ]; then
    COMPOSE_PROFILES="$(IFS=,; echo "${profiles[*]}")"
    export COMPOSE_PROFILES
fi

if ! docker info >/dev/null 2>&1; then
    echo "Docker ne répond pas : démarrez Docker Desktop, puis relancez ./start-app.sh"
    exit 1
fi

echo "Construction et démarrage de l'app (compose.yaml)..."
if ! docker compose up --build --detach --remove-orphans --wait --wait-timeout 900; then
    echo ""
    echo "L'app n'est pas prête. État des services et derniers logs :"
    docker compose ps --all
    docker compose logs --tail 40
    exit 1
fi

SERVICES="$(docker compose config --services | sort | paste -sd ' ' -)"
has_service() { case " ${SERVICES} " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# Published host ports of the running services, one "<service> <port>" line per port,
# sorted by service (an IPv4 and an IPv6 binding of the same port make one line).
PUBLISHED="$(docker compose ps --format '{{.Service}}{{range .Publishers}}{{if .PublishedPort}} {{.PublishedPort}}{{end}}{{end}}' \
    | awk '{ for (i = 2; i <= NF; i++) print $1, $i }' | sort -u)"

if has_service frontend; then
    MAIN=frontend
else
    MAIN="$(echo "$PUBLISHED" | awk 'NR == 1 { print $1 }')"
fi
MAIN_PORT="$(echo "$PUBLISHED" | awk -v service="$MAIN" '$1 == service { print $2; exit }')"

echo ""
if [ -n "$MAIN_PORT" ]; then
    APP_URL="http://localhost:${MAIN_PORT}"
    echo "App prête : ${APP_URL}"
    if [ "$MAIN" = frontend ]; then echo "Admin     : ${APP_URL}/admin/"; fi
else
    echo "App prête (aucun port publié)"
fi
# Every other published port, one line per port (backend, APIs, services of a profile).
echo "$PUBLISHED" | while read -r service host_port; do
    case "$service" in "" | "$MAIN" | db) continue ;; esac
    printf '%-10s: http://localhost:%s\n' "$service" "$host_port"
done
echo ""
echo "Logs      : docker compose logs -f ${MAIN}    (services : ${SERVICES}; sans nom : tous)"
if has_service db; then
    echo "Base      : psql postgresql://app:app@$(docker compose port db 5432)/app"
fi
echo "Arrêt     : ./stop-app.sh (les données restent)"
