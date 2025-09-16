#!/bin/sh
set -e  # Exit on any error

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting Django project initialization"

log "Running database migrations"
uv run manage.py migrate --noinput

log "Collecting static files"
uv run manage.py collectstatic --noinput --clear

log "Starting Django"
uv run manage.py runserver 0.0.0.0:8000
