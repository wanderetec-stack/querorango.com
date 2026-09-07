import urllib.request

for url in ['https://querorango.com', 'https://www.querorango.com', 'https://querorango.pages.dev']:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        r = urllib.request.urlopen(req, timeout=10)
        print(f'{url} -> HTTP {r.getcode()}')
    except Exception as e:
        print(f'{url} -> {e}')
