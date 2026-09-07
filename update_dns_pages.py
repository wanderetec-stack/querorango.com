import urllib.request, json

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ZONE_ID = 'b4fb41f79a12a97deb3a83cd0764d69d'

# 1. Update apex querorango.com to CNAME querorango.pages.dev
payload_apex = json.dumps({
    'type': 'CNAME',
    'name': 'querorango.com',
    'content': 'querorango.pages.dev',
    'proxied': True,
    'ttl': 1
}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/1f72f9b96eca648774a8dc1945dc5ddc',
    data=payload_apex,
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    method='PUT'
)
try:
    r = urllib.request.urlopen(req)
    print('Updated querorango.com -> querorango.pages.dev:', json.loads(r.read())['success'])
except urllib.error.HTTPError as e:
    print('Apex error:', e.code, e.read().decode())

# 2. Update www.querorango.com to CNAME querorango.pages.dev
payload_www = json.dumps({
    'type': 'CNAME',
    'name': 'www.querorango.com',
    'content': 'querorango.pages.dev',
    'proxied': True,
    'ttl': 1
}).encode('utf-8')
req2 = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/6ed47b5975fd31c2bff0f53fceccc006',
    data=payload_www,
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    method='PUT'
)
try:
    r2 = urllib.request.urlopen(req2)
    print('Updated www.querorango.com -> querorango.pages.dev:', json.loads(r2.read())['success'])
except urllib.error.HTTPError as e:
    print('WWW error:', e.code, e.read().decode())
