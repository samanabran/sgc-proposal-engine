#!/bin/bash
docker exec odoo-prod odoo -c /etc/odoo/odoo.conf -d odoo19-sgc -i sgc_crm_fields --stop-after-init --no-http > /tmp/install_out.log 2>&1
echo "EXIT:$?"
