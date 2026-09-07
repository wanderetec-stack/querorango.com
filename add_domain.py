import urllib.request, json

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCOUNT_ID = '75e47d7a5b78e2531cf4600007acd047'

payload = json.dumps({'name': 'querorango.com'}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/querorango/domains',
    data=payload,
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    method='POST'
)
try:
    r = urllib.request.urlopen(req)
    data = json.loads(r.read())
    print('Result:', data)
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code, e.read().decode('utf-8'))
