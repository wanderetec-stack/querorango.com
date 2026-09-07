import os, sys, glob, re

BASE_DIR = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'

VERIFIED_IMAGES = [
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
    'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800&q=80', # queijos
    'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80', # molhos
    'https://images.unsplash.com/photo-1576107232684-1279f3908594?w=800&q=80', # frituras
    'https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=800&q=80', # batata frita
    'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80', # pastel
    'https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=800&q=80', # costelinha
    'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800&q=80'  # almondega
]

# 1. Corrigir imagens quebradas nos 300 HTMLs individuais de receitas
broken_urls = [
    'https://images.unsplash.com/photo-1527477378370-13f639ee8861?w=1200&q=80',
    'https://images.unsplash.com/photo-1499028344343-cd173efc68a9?w=1200&q=80'
]
fallback_img = 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800&q=80'

fixed_recipes = 0
boteco_files = glob.glob(os.path.join(BASE_DIR, 'receitas', 'boteco', '*', 'index.html'))
for fpath in boteco_files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    changed = False
    for b_url in broken_urls:
        if b_url in c:
            c = c.replace(b_url, fallback_img)
            changed = True
    if changed:
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(c)
        fixed_recipes += 1

print(f'Receitas individuais corrigidas: {fixed_recipes}')
