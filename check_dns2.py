import urllib.request, json

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ZONE_ID = 'b4fb41f79a12a97deb3a83cd0764d69d'

req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records',
    headers={'Authorization': f'Bearer {TOKEN}'}
)
r = urllib.request.urlopen(req)
data = json.loads(r.read())
for rec in data.get('result', []):
    if 'querorango.com' in rec['name']:
        print(rec['type'], rec['name'], '->', rec['content'], '(proxied:', rec['proxied'], ')')
