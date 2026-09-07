import urllib.request

urls = [
    'https://querorango.com/',
    'https://querorango.com/receitas/boteco/',
    'https://querorango.com/css/style.css'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req, timeout=10)
    print(u, '-> Status', res.getcode())
