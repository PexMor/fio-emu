#!/bin/bash
#
# Generate and inject statement via API (equivalent to r01_make_inject.sh)
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

SDATE=$($DATE +%Y-%m-%d -d "30 days ago")
EDATE=$($DATE +%Y-%m-%d -d "today")

# Generate and inject via single API call
curl -X POST "${API_URL}/emu/v1/generate" \
     -H "Content-Type: application/json" \
     -d "{
       \"min_amount\": 0,
       \"max_amount\": 8000,
       \"date_from\": \"${SDATE}\",
       \"date_to\": \"${EDATE}\",
       \"num_transactions\": 100
     }" \
     -o tmp/statements.json

echo ""
echo "Statement generated and injected. Saved to tmp/statements.json"

