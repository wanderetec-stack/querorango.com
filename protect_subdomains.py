import urllib.request, json

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ZONE_ID = 'b4fb41f79a12a97deb3a83cd0764d69d'
SERVER_IP = '44.198.159.221'

# Update admin, ftp, mail, n8n to direct A record to 44.198.159.221
subdomains_to_protect = [
    ('admin.querorango.com', 'a0e9d9f9471c771de46a1485e23cb275', True),
    ('ftp.querorango.com', '25480ecc64261a82ca0dfc2a1bb86276', False),
    ('mail.querorango.com', 'c0576969e89d5e711dae3e3200c5ba90', False),
    ('n8n.querorango.com', '94f7e7dca86782acbcd6101391d4394b', True)
]

for name, rec_id, proxied in subdomains_to_protect:
    payload = json.dumps({
        'type': 'A',
        'name': name,
        'content': SERVER_IP,
        'proxied': proxied,
        'ttl': 1
    }).encode('utf-8')
    req = urllib.request.Request(
        f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{rec_id}',
        data=payload,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
        method='PUT'
    )
    r = urllib.request.urlopen(req)
    print(f'Protected {name} -> A {SERVER_IP}:', json.loads(r.read())['success'])
