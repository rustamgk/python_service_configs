#!/usr/bin/env sh
set -eux

## man:python3
export PYTHONOPTIMIZE=1

SERVE_PORT=${SERVE_PORT:?SERVE_PORT MUST be defined}

echo "Starting service on 0.0.0.0:${SERVE_PORT}"
exec gunicorn \
  --bind=0.0.0.0:${SERVE_PORT} \
  --workers=2 \
  --log-level=info --capture-output \
  "webapp:create_app()"
