#!/bin/bash
#
# docker run --rm alpine nslookup host.docker.internal
#

set -euo pipefail

mkdir -p tmp

if [[ "$(uname)" == "Darwin" ]]; then
  DATE=gdate
else
  DATE=date
fi

SDATE=`$DATE +%Y-%m-%d -d "10 days ago"`
EDATE=`$DATE +%Y-%m-%d -d "today"`

uv run fiocli \
  --min-amount 0 \
  --max-amount 50000 \
  --date-from $SDATE \
  --date-to $EDATE \
  --num-transactions 30 \
  --output tmp/statements.json \
  --pretty

curl -X POST http://localhost:8000/emu/v1/periods \
     -H "Content-Type: application/json" \
     -d @tmp/statements.json
