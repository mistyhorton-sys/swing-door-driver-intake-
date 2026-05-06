#!/usr/bin/env bash
set -euo pipefail

PORT_VALUE="${PORT:-${WEBSITES_PORT:-8000}}"

echo "Starting Swing Door Driver Intake on port ${PORT_VALUE}"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT_VALUE}" --proxy-headers
