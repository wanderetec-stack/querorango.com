import urllib.request

for proto in ['https', 'http']:
    url = f'{proto}://n8n.querorango.com'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        r = urllib.request.urlopen(req, timeout=5)
        print(f'{url} -> HTTP {r.getcode()}')
    except Exception as e:
        print(f'{url} -> {e}')
