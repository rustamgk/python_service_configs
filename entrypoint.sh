#!/usr/bin/env sh
set -eux

SERVE_PORT=${SERVE_PORT:?SERVE_PORT MUST be defined}

echo "Starting service on 0.0.0.0:${SERVE_PORT}"
exec gunicorn \
  --bind=0.0.0.0:${SERVE_PORT} \
  --workers=2 \
  "webapp:create_app()"
