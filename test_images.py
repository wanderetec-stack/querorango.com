import urllib.request

BOTECO_IMAGES = [
    'https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=1200&q=80',
    'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=1200&q=80',
    'https://images.unsplash.com/photo-1527477378370-13f639ee8861?w=1200&q=80',
    'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=1200&q=80',
    'https://images.unsplash.com/photo-1544025162-d76694265947?w=1200&q=80',
    'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1200&q=80',
    'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=1200&q=80',
    'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=1200&q=80',
    'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=1200&q=80',
    'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=1200&q=80',
    'https://images.unsplash.com/photo-1559847844-5315695dadae?w=1200&q=80',
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&q=80',
    'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&q=80',
    'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=1200&q=80',
    'https://images.unsplash.com/photo-1499028344343-cd173efc68a9?w=1200&q=80',
    'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200&q=80'
]

for idx, url in enumerate(BOTECO_IMAGES):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        print(f'[{idx}] Status: {res.getcode()} -> OK')
    except Exception as e:
        print(f'[{idx}] FALHOU: {url} -> {e}')
