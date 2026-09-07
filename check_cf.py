import urllib.request, json

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCOUNT_ID = '75e47d7a5b78e2531cf4600007acd047'
ZONE_ID = 'b4fb41f79a12a97deb3a83cd0764d69d'

try:
    r = urllib.request.urlopen('https://querorango.pages.dev')
    print('Pages Dev Status:', r.getcode())
except Exception as e:
    print('Pages Dev Error:', e)

req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records',
    headers={'Authorization': 'Bearer ' + TOKEN}
)
r = urllib.request.urlopen(req)
data = json.loads(r.read())
print('DNS Records:')
for rec in data.get('result', []):
    print(rec['type'], rec['name'], '->', rec['content'], 'ID:', rec['id'])
