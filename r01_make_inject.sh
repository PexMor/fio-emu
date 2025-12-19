#!/bin/bash
#
# docker run --rm alpine nslookup host.docker.internal
#

set -euo pipefail

mkdir -p tmp

# Use environment variables for API URL, with defaults
API_HOST=${API_HOST:-localhost}
API_PORT=${API_PORT:-8080}
API_URL=${API_URL:-http://${API_HOST}:${API_PORT}}

if [[ "$(uname)" == "Darwin" ]]; then
  DATE=gdate
else
  DATE=date
fi

SDATE=`$DATE +%Y-%m-%d -d "30 days ago"`
EDATE=`$DATE +%Y-%m-%d -d "today"`

uv run fiocli \
  --min-amount 0 \
  --max-amount 8000 \
  --date-from $SDATE \
  --date-to $EDATE \
  --num-transactions 100 \
  --output tmp/statements.json \
  --pretty

curl -X POST ${API_URL}/emu/v1/periods \
     -H "Content-Type: application/json" \
     -d @tmp/statements.json
