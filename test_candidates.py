import urllib.request

candidates = [
    'https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800&q=80', # torresmo
    'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800&q=80', # frango
    'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80', # petiscos
    'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80', # costelinha
    'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80', # churrasco
    'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=800&q=80', # asinhas
    'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&q=80', # batatas
    'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&q=80', # empanados
    'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&q=80', # tabua
    'https://images.unsplash.com/photo-1559847844-5315695dadae?w=800&q=80', # camarao
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80', # prato
    'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&q=80', # salada
    'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800&q=80', # queijos
    'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80', # molhos
    'https://images.unsplash.com/photo-1576107232684-1279f3908594?w=800&q=80', # frituras
    'https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=800&q=80', # batata frita
    'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80', # pastel/dumpling
    'https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=800&q=80', # costelinha
    'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800&q=80', # almondega
    'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80'  # lula/seafood
]

verified = []
for u in candidates:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=4)
        if res.getcode() == 200:
            verified.append(u)
    except:
        pass

print(f'Total de imagens 100% verificadas (HTTP 200): {len(verified)}')
