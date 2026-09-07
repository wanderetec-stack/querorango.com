import urllib.request

url = 'https://querorango.com/feed.rss'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    r = urllib.request.urlopen(req)
    print(url, '-> HTTP', r.getcode())
    print('Content length:', len(r.read()))
except Exception as e:
    print('Error:', e)
