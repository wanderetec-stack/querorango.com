import urllib.request, json, time

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCOUNT_ID = '75e47d7a5b78e2531cf4600007acd047'

req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/querorango/domains',
    headers={'Authorization': f'Bearer {TOKEN}'}
)
r = urllib.request.urlopen(req)
data = json.loads(r.read())
for d in data.get('result', []):
    print('Domain:', d['name'], '| Status:', d['status'])

# Test direct HTTPS access to querorango.pages.dev/feed.rss
req_rss = urllib.request.Request(
    'https://querorango.pages.dev/feed.rss',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    r_rss = urllib.request.urlopen(req_rss)
    print('feed.rss on Pages HTTP Status:', r_rss.getcode())
    print('feed.rss sample:', r_rss.read()[:200].decode('utf-8'))
except Exception as e:
    print('RSS error:', e)
