#!/bin/bash
# Alerts if the signature webhook handler stops responding.
# Install: crontab -e  ->  */5 * * * * /opt/signature-handler/healthcheck.sh
set -u

URL="https://signature.sgctech.ai/healthz"
ALERT_EMAIL="sgc-admin@sgctech.ai"
STATE_FILE="/tmp/signature-handler-healthcheck.state"

status=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "$URL")

if [ "$status" != "200" ]; then
    if [ ! -f "$STATE_FILE" ]; then
        echo "DOWN since $(date -u +%FT%TZ)" > "$STATE_FILE"
        if command -v mail >/dev/null 2>&1; then
            echo "signature-handler at $URL returned HTTP $status at $(date -u +%FT%TZ). Check: docker logs signature-handler" \
                | mail -s "ALERT: signature webhook handler is down" "$ALERT_EMAIL"
        else
            echo "$(date -u +%FT%TZ) ALERT: signature-handler down (HTTP $status) and no local 'mail' command to notify $ALERT_EMAIL" >> /var/log/signature-handler-healthcheck.log
        fi
    fi
else
    rm -f "$STATE_FILE"
fi
