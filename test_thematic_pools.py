import urllib.request

pools = {
    'torresmos': [
        'https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800&q=80',
        'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80',
        'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800&q=80',
        'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80'
    ],
    'queijos': [
        'https://images.unsplash.com/photo-1548946526-f69e2424cf45?w=800&q=80',
        'https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?w=800&q=80',
        'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&q=80',
        'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800&q=80'
    ],
    'bolinhos': [
        'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&q=80',
        'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800&q=80',
        'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800&q=80',
        'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80'
    ],
    'frangos': [
        'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=800&q=80',
        'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800&q=80',
        'https://images.unsplash.com/photo-1569691899455-88464f6d3ab1?w=800&q=80'
    ],
    'carnes': [
        'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80',
        'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80',
        'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80',
        'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800&q=80'
    ],
    'frutos': [
        'https://images.unsplash.com/photo-1559847844-5315695dadae?w=800&q=80',
        'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80',
        'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80',
        'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800&q=80'
    ],
    'batatas': [
        'https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=800&q=80',
        'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&q=80',
        'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=800&q=80'
    ],
    'pasteis': [
        'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80',
        'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800&q=80',
        'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&q=80'
    ],
    'caldinhos': [
        'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&q=80',
        'https://images.unsplash.com/photo-1547592180-85f173990554?w=800&q=80',
        'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&q=80'
    ],
    'molhos': [
        'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80',
        'https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=800&q=80',
        'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&q=80'
    ]
}

all_ok = True
for cat, urls in pools.items():
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=4)
            if res.getcode() != 200:
                print(f'{cat}: {u} -> status {res.getcode()}')
                all_ok = False
        except Exception as e:
            print(f'{cat}: {u} -> erro: {e}')
            all_ok = False

if all_ok:
    print('TODAS AS 33 IMAGENS TEMÁTICAS ESTÃO 100% OPERACIONAIS (HTTP 200)!')
