import urllib.request

test_urls = {
    # 1. Torresmo / Porco
    'pork_torresmo_1': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80', # ribs
    'pork_torresmo_2': 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800&q=80', # crispy pork belly
    'pork_torresmo_3': 'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800&q=80', # meat/pork
    'pork_torresmo_4': 'https://images.unsplash.com/photo-1514944298352-bf6d48259b13?w=800&q=80', # pork meat
    
    # 2. Queijos / Dadinhos
    'cheese_1': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&q=80', # cheese board
    'cheese_2': 'https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?w=800&q=80', # fried cheese
    'cheese_3': 'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&q=80', # crispy bites
    'cheese_4': 'https://images.unsplash.com/photo-1548946526-f69e2424cf45?w=800&q=80', # mozzarella sticks
    
    # 3. Bolinhos / Croquetes
    'bolinho_1': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&q=80', # fried balls/croquettes
    'bolinho_2': 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800&q=80', # meatballs/croquetes
    'bolinho_3': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80', # bar snacks
    'bolinho_4': 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800&q=80', # falafel/bolinhos
    
    # 4. Frango / Asinhas
    'chicken_1': 'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=800&q=80', # wings
    'chicken_2': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&q=80', # fried chicken
    'chicken_3': 'https://images.unsplash.com/photo-1527477378370-13f639ee8861?w=800&q=80', # chicken
    'chicken_4': 'https://images.unsplash.com/photo-1569691899455-88464f6d3ab1?w=800&q=80', # fried chicken
    
    # 5. Carnes bovinas / Iscas / Chapa
    'beef_1': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80', # skewers / bbq
    'beef_2': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80', # ribs/meat
    'beef_3': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80', # beef dish
    'beef_4': 'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800&q=80', # steak
    
    # 6. Peixes / Frutos do Mar
    'seafood_1': 'https://images.unsplash.com/photo-1559847844-5315695dadae?w=800&q=80', # shrimp
    'seafood_2': 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80', # fried seafood
    'seafood_3': 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80', # fried fish bites
    'seafood_4': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800&q=80', # fish dish
    
    # 7. Batatas / Mandioca / Polenta
    'fries_1': 'https://images.unsplash.com/photo-1576107232684-1279f3908594?w=800&q=80', # fries
    'fries_2': 'https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=800&q=80', # french fries
    'fries_3': 'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&q=80', # rustic fries
    'fries_4': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=800&q=80', # fries
    
    # 8. Pastéis / Salgados / Coxinhas
    'pastel_1': 'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&q=80', # fried pastry
    'pastel_2': 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800&q=80', # savory snacks
    'pastel_3': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80', # dumplings/pastéis
    'pastel_4': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80', # fried snacks
    
    # 9. Caldinhos de Boteco
    'soup_1': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&q=80', # hot soup
    'soup_2': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=800&q=80', # bean soup
    'soup_3': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&q=80', # rustic broth
    
    # 10. Molhos e Conservas
    'sauce_1': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80', # dips and sauces
    'sauce_2': 'https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=800&q=80', # sauces
    'sauce_3': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&q=80'  # vinagrete
}

valid = {}
for k, u in test_urls.items():
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=4)
        if res.getcode() == 200:
            valid[k] = u
    except Exception as e:
        print(f'{k} falhou: {e}')

print(f'Total de imagens temáticas aprovadas: {len(valid)} de {len(test_urls)}')
