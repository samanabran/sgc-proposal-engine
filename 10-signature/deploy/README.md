# Permanent hosting — signature.sgctech.ai

Replaces the `localhost.run` tunnel with a real, always-on service on `vps-root`
(the same box that runs `app.sgctech.ai`). Once this is live, the tunnel dance
in the rest of `10-signature/` is obsolete for day-to-day use.

## Prerequisites (do this first)

**Add a DNS A record:** `signature.sgctech.ai` → `80.241.218.108`

(Same registrar/DNS provider used for the other `*.sgctech.ai` subdomains.)
Wait for it to resolve (`nslookup signature.sgctech.ai`) before issuing a TLS
cert — Let's Encrypt's HTTP-01 challenge will fail otherwise.

## Deploy steps

1. **Copy this `deploy/` folder, the handler code, and the notification templates to the server:**
   ```bash
   ssh vps-root "mkdir -p /opt/signature-handler/handler /opt/signature-handler/notification-templates /opt/signature-handler/data"
   scp docker-compose.yml nginx-signature.sgctech.ai.conf .env.example healthcheck.sh \
       vps-root:/opt/signature-handler/
   scp ../handler/*.py vps-root:/opt/signature-handler/handler/
   scp ../notification-templates/*.md vps-root:/opt/signature-handler/notification-templates/
   ```
   (`notification-templates/` is mounted separately because `notifications.py` resolves it via a
   relative `../notification-templates` path from its own file location — inside the container
   that only resolves correctly if it's mounted at `/notification-templates`, one level above `/app`.)

2. **Create the real `.env` — on the server only, never through chat:**
   ```bash
   ssh vps-root
   cp /opt/signature-handler/.env.example /opt/signature-handler/.env
   nano /opt/signature-handler/.env   # fill in real, freshly rotated secrets here
   chmod 600 /opt/signature-handler/.env
   ```

3. **Install the nginx vhost and issue the cert:**
   ```bash
   ssh vps-root "cp /opt/signature-handler/nginx-signature.sgctech.ai.conf /etc/nginx/sites-available/signature.sgctech.ai"
   ssh vps-root "ln -s /etc/nginx/sites-available/signature.sgctech.ai /etc/nginx/sites-enabled/"
   ssh vps-root "nginx -t && systemctl reload nginx"
   ssh vps-root "certbot --nginx -d signature.sgctech.ai"
   ```

4. **Bring up the container:**
   ```bash
   ssh vps-root "cd /opt/signature-handler && docker compose up -d"
   ssh vps-root "docker logs signature-handler --tail 20"
   ```
   Expect: `Signature webhook listening on http://0.0.0.0:8765/...`

5. **Verify end-to-end:**
   ```bash
   curl https://signature.sgctech.ai/healthz
   ```
   Expect `{"status": "ok"}` — this time from a real domain that never rotates.

6. **Install the healthcheck cron:**
   ```bash
   ssh vps-root "chmod +x /opt/signature-handler/healthcheck.sh"
   ssh vps-root "(crontab -l 2>/dev/null; echo '*/5 * * * * /opt/signature-handler/healthcheck.sh') | crontab -"
   ```

7. **Update the webhook in Zoho Sign one final time:**
   ```
   https://signature.sgctech.ai/webhooks/signature/zoho_sign/
   ```
   This is the last URL update this integration should ever need.

## Redeploying after a code change

```bash
scp ../handler/*.py vps-root:/opt/signature-handler/handler/
ssh vps-root "docker restart signature-handler"
```

No env var re-typing needed — `.env` persists on the server across restarts.
