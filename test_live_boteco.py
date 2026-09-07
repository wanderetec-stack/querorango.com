import urllib.request

urls = [
    'https://querorango.com/receitas/boteco/',
    'https://querorango.com/receitas/boteco/torresmo-de-rolo-pururucado-classico/',
    'https://querorango.com/receitas/boteco/dadinho-de-tapioca-classico-com-queijo-coalho-e-geleia-de-pimenta/',
    'https://querorango.com/receitas/boteco/bolinho-de-feijoada-tradicional-com-couve-refogada-e-bacon/'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        r = urllib.request.urlopen(req, timeout=10)
        print(u, '-> HTTP', r.getcode())
    except Exception as e:
        print(u, '-> Error:', e)
