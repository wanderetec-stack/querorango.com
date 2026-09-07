import urllib.request, json

req = urllib.request.Request(
    'https://querorango.pages.dev',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
try:
    r = urllib.request.urlopen(req)
    print('querorango.pages.dev Status:', r.getcode())
    html = r.read().decode('utf-8', errors='ignore')
    print('Title:', html[:500])
except Exception as e:
    print('Error:', e)
