import urllib.request, json

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCOUNT_ID = '75e47d7a5b78e2531cf4600007acd047'

req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/querorango/domains',
    headers={'Authorization': f'Bearer {TOKEN}'}
)
r = urllib.request.urlopen(req)
data = json.loads(r.read())
for d in data.get('result', []):
    print('Domain:', d['name'], '| Status:', d['status'], '| Validation:', d.get('validation_data'))
