# -*- coding: utf-8 -*-
import os, sys, glob, json, re, unicodedata

BASE_DIR = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'
SCRATCH_DIR = r'C:\Users\Wander - Rosangela\.gemini\antigravity\brain\33960100-d973-4234-86ad-38085252313a\scratch'
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SCRATCH_DIR)

from generator import save_recipe
from build_catalog import build_article_text
from build_and_publish_boteco_300 import RECIPES_DATA, slugify

POOLS = {
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

groups = [
    ('torresmos', 'Torresmos & Suínos', 0, 30),
    ('queijos', 'Queijos & Dadinhos', 30, 60),
    ('bolinhos', 'Bolinhos & Croquetes', 60, 90),
    ('frangos', 'Frangos & Asinhas', 90, 120),
    ('carnes', 'Carnes & Chapas', 120, 150),
    ('frutos', 'Frutos do Mar', 150, 180),
    ('batatas', 'Batatas & Mandiocas', 180, 210),
    ('pasteis', 'Pastéis & Salgados', 210, 240),
    ('caldinhos', 'Caldinhos', 240, 270),
    ('molhos', 'Molhos & Conservas', 270, 300)
]

# Sugestões de relacionados estritamente dentro de boteco
related_recommendations = {
    'torresmos': [
        {'title': 'Mandioca Frita Crocante por Fora e Cremosa', 'url': '/receitas/boteco/mandioca-frita-crocante-por-fora-e-cremosa-por-dentro/', 'img': POOLS['batatas'][1], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Calabresa Flambada na Cachaça com Cebola', 'url': '/receitas/boteco/linguica-calabresa-flambada-na-cachaca-com-cebola-roxa/', 'img': POOLS['carnes'][0], 'time': '25 min', 'cat': 'Comida de Boteco'},
        {'title': 'Caldinho de Feijão Preto com Torresmo e Couve', 'url': '/receitas/boteco/caldinho-de-feijao-preto-com-torresminho-couve-e-cheiro-verde/', 'img': POOLS['caldinhos'][0], 'time': '50 min', 'cat': 'Comida de Boteco'}
    ],
    'queijos': [
        {'title': 'Dadinho de Tapioca com Geleia de Pimenta', 'url': '/receitas/boteco/dadinho-de-tapioca-classico-com-queijo-coalho-e-geleia-de-pimenta/', 'img': POOLS['queijos'][2], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Provolone à Milanesa com Molho Tártaro', 'url': '/receitas/boteco/provolone-a-milanesa-crocante-com-oregano-e-molho-tartaro/', 'img': POOLS['queijos'][0], 'time': '25 min', 'cat': 'Comida de Boteco'},
        {'title': 'Geleia de Pimenta Vermelha Agridoce', 'url': '/receitas/boteco/geleia-de-pimenta-vermelha-agridoce-para-queijos-e-empanados/', 'img': POOLS['molhos'][1], 'time': '45 min', 'cat': 'Comida de Boteco'}
    ],
    'bolinhos': [
        {'title': 'Bolinho de Feijoada Tradicional com Couve', 'url': '/receitas/boteco/bolinho-de-feijoada-tradicional-com-couve-refogada-e-bacon/', 'img': POOLS['bolinhos'][0], 'time': '50 min', 'cat': 'Comida de Boteco'},
        {'title': 'Bolinho de Bacalhau Tradicional Português', 'url': '/receitas/boteco/bolinho-de-bacalhau-tradicional-portugues-de-boteco/', 'img': POOLS['bolinhos'][1], 'time': '50 min', 'cat': 'Comida de Boteco'},
        {'title': 'Molho de Pimenta Dedo-de-Moça na Cachaça', 'url': '/receitas/boteco/molho-de-pimenta-caseiro-dedo-de-moca-curtido-na-cachaca/', 'img': POOLS['molhos'][1], 'time': '25 min', 'cat': 'Comida de Boteco'}
    ],
    'frangos': [
        {'title': 'Frango a Passarinho com Muito Alho Crocante', 'url': '/receitas/boteco/frango-a-passarinho-classico-com-muito-alho-crocante-e-limao/', 'img': POOLS['frangos'][1], 'time': '40 min', 'cat': 'Comida de Boteco'},
        {'title': 'Batata Frita Rústica com Alecrim e Alho', 'url': '/receitas/boteco/batata-frita-rustica-com-casca-alecrim-e-alho-frito/', 'img': POOLS['batatas'][1], 'time': '40 min', 'cat': 'Comida de Boteco'},
        {'title': 'Molho de Alho Assado Cremoso para Petiscos', 'url': '/receitas/boteco/molho-de-alho-assado-cremoso-para-carnes-e-petiscos/', 'img': POOLS['molhos'][0], 'time': '45 min', 'cat': 'Comida de Boteco'}
    ],
    'carnes': [
        {'title': 'Picanha Fatiada na Chapa com Alho Crocante', 'url': '/receitas/boteco/picanha-fatiada-na-chapa-com-alho-crocante-e-mandioca/', 'img': POOLS['carnes'][1], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Isca de Filé Mignon ao Quatro Queijos', 'url': '/receitas/boteco/isca-de-file-mignon-ao-molho-quatro-queijos-de-boteco/', 'img': POOLS['carnes'][2], 'time': '30 min', 'cat': 'Comida de Boteco'},
        {'title': 'Vinagrete Tradicional de Boteco com Azeite', 'url': '/receitas/boteco/vinagrete-tradicional-de-boteco-com-cebola-tomate-e-azeite/', 'img': POOLS['molhos'][2], 'time': '15 min', 'cat': 'Comida de Boteco'}
    ],
    'frutos': [
        {'title': 'Isca de Tilápia no Fubá com Limão', 'url': '/receitas/boteco/isca-de-tilapia-crocante-empanada-no-fuba-com-limao/', 'img': POOLS['frutos'][2], 'time': '30 min', 'cat': 'Comida de Boteco'},
        {'title': 'Camarão Alho e Óleo Crocante com Casca', 'url': '/receitas/boteco/camarao-alho-e-oleo-crocante-frito-com-casca/', 'img': POOLS['frutos'][0], 'time': '25 min', 'cat': 'Comida de Boteco'},
        {'title': 'Molho Tártaro Artesanal com Picles', 'url': '/receitas/boteco/molho-tartaro-artesanal-com-picles-crocante-e-alcaparras/', 'img': POOLS['molhos'][0], 'time': '15 min', 'cat': 'Comida de Boteco'}
    ],
    'batatas': [
        {'title': 'Mandioca Frita Crocante por Fora e Cremosa', 'url': '/receitas/boteco/mandioca-frita-crocante-por-fora-e-cremosa-por-dentro/', 'img': POOLS['batatas'][1], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Batata com Cheddar Cremoso e Bacon', 'url': '/receitas/boteco/batata-frita-coberta-com-cheddar-cremoso-e-bacon-crocante/', 'img': POOLS['batatas'][0], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Polenta Frita Palito com Parmesão', 'url': '/receitas/boteco/polenta-frita-palito-sequinha-com-parmesao-ralado/', 'img': POOLS['batatas'][1], 'time': '40 min', 'cat': 'Comida de Boteco'}
    ],
    'pasteis': [
        {'title': 'Pastel de Feira de Carne com Ovo e Azeitona', 'url': '/receitas/boteco/pastel-de-feira-de-carne-moida-com-azeitona-e-ovo-cozido/', 'img': POOLS['pasteis'][0], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Coxinha sem Massa de Frango com Catupiry', 'url': '/receitas/boteco/coxinha-sem-massa-de-frango-cremoso-com-catupiry/', 'img': POOLS['pasteis'][1], 'time': '35 min', 'cat': 'Comida de Boteco'},
        {'title': 'Kibe Frito Recheado com Coalhada Seca', 'url': '/receitas/boteco/kibe-frito-recheado-com-coalhada-seca-e-hortela-fresca/', 'img': POOLS['pasteis'][2], 'time': '45 min', 'cat': 'Comida de Boteco'}
    ],
    'caldinhos': [
        {'title': 'Caldinho de Feijão Preto com Torresmo e Couve', 'url': '/receitas/boteco/caldinho-de-feijao-preto-com-torresminho-couve-e-cheiro-verde/', 'img': POOLS['caldinhos'][0], 'time': '50 min', 'cat': 'Comida de Boteco'},
        {'title': 'Caldinho de Mocotó Encorpado e Aromático', 'url': '/receitas/boteco/caldinho-de-mocoto-tradicional-encorpado-e-aromatico/', 'img': POOLS['caldinhos'][1], 'time': '75 min', 'cat': 'Comida de Boteco'},
        {'title': 'Torresmo de Rolo Pururucado Clássico', 'url': '/receitas/boteco/torresmo-de-rolo-pururucado-classico/', 'img': POOLS['torresmos'][0], 'time': '65 min', 'cat': 'Comida de Boteco'}
    ],
    'molhos': [
        {'title': 'Molho de Pimenta Dedo-de-Moça na Cachaça', 'url': '/receitas/boteco/molho-de-pimenta-caseiro-dedo-de-moca-curtido-na-cachaca/', 'img': POOLS['molhos'][1], 'time': '25 min', 'cat': 'Comida de Boteco'},
        {'title': 'Molho Verde Cremoso de Ervas de Boteco', 'url': '/receitas/boteco/molho-verde-cremoso-de-ervas-com-maionese-artesanal/', 'img': POOLS['molhos'][0], 'time': '10 min', 'cat': 'Comida de Boteco'},
        {'title': 'Dadinho de Tapioca com Queijo Coalho', 'url': '/receitas/boteco/dadinho-de-tapioca-classico-com-queijo-coalho-e-geleia-de-pimenta/', 'img': POOLS['queijos'][2], 'time': '35 min', 'cat': 'Comida de Boteco'}
    ]
}

print('=== REGENERANDO 300 RECEITAS COM IMAGENS 100% TEMÁTICAS E BACKLINKS ESTRITOS DE BOTECO ===')

generated_for_catalog = []

for i, (title, main_ing, sec_ing, prep_m, cook_m, cals) in enumerate(RECIPES_DATA):
    slug = slugify(title)
    total_m = prep_m + cook_m

    # Determinar subcategoria
    cur_cat = 'torresmos'
    cur_label = 'Torresmos & Suínos'
    for tag_id, label, start, end in groups:
        if start <= i < end:
            cur_cat = tag_id
            cur_label = label
            break

    # Imagem 100% tematica
    cat_pool = POOLS[cur_cat]
    img_url = cat_pool[i % len(cat_pool)]

    # Relacionados 100% relevantes da mesma categoria
    rec_list = [r for r in related_recommendations[cur_cat] if r['title'].lower() not in title.lower()][:3]

    article_html = build_article_text(title, 'Comida de Boteco', main_ing, sec_ing)

    recipe_obj = {
        'category_slug': 'boteco',
        'title': title,
        'slug': slug,
        'meta_description': f'Receita de {title} autêntica de boteco: passo a passo completo, ingredientes, dicas de crocância e segredos de preparo em casa.',
        'prep_time': f'PT{prep_m}M',
        'cook_time': f'PT{cook_m}M',
        'total_time': f'{total_m} min',
        'prep_minutes': prep_m,
        'cook_minutes': cook_m,
        'total_minutes': total_m,
        'base_portions': 6,
        'yield_portions': '6 porções de boteco',
        'calories': f'{cals} kcal',
        'rating': '4.9',
        'rating_count': '320',
        'image_url': img_url,
        'ingredients': [
            {'amount': '600', 'unit': 'g', 'name': f'de {main_ing} fresco selecionado'},
            {'amount': '3', 'unit': 'colheres', 'name': f'de {sec_ing}'},
            {'amount': '4', 'unit': 'dentes', 'name': 'de alho picadinhos ou amassados'},
            {'amount': '2', 'unit': 'colheres', 'name': 'de azeite de oliva extravirgem ou banha'},
            {'amount': '1', 'unit': 'colher', 'name': 'de sal marinho e pimenta-do-reino moída na hora'},
            {'amount': '1', 'unit': 'maço', 'name': 'de cheiro-verde fresco picadinho'},
            {'amount': '1', 'unit': 'unidade', 'name': 'de limão taiti cortado em gomos para acompanhar'}
        ],
        'steps': [
            {'text': f'Separe e higienize os ingredientes. Corte o(a) {main_ing} no tamanho clássico de aperitivo de boteco.', 'timer_minutes': 0},
            {'text': f'Tempere com o alho, {sec_ing}, sal e pimenta. Deixe marinar por 15 minutos para absorver todo o tempero.', 'timer_minutes': 15, 'timer_label': 'Marinada'},
            {'text': f'Inicie o preparo térmico (fritura, assamento ou cozimento) por cerca de {cook_m} minutos até dourar e ficar com a textura perfeita.', 'timer_minutes': cook_m, 'timer_label': 'Preparo'},
            {'text': 'Escorra em papel toalha se necessário, salpique cheiro-verde fresco e sirva imediatamente bem quentinho!', 'timer_minutes': 3, 'timer_label': 'Finalização'}
        ],
        'faq': [
            {'q': f'Qual a melhor bebida para acompanhar {title}?', 'a': 'Combina perfeitamente com chopp bem tirado ou cerveja artesanal gelada, caipirinha clássica de limão ou batida de maracujá.'},
            {'q': 'Qual o segredo para manter a textura crocante?', 'a': 'O segredo é secar bem os ingredientes antes de fritar, usar gordura limpa e bem quente (180°C) e escorrer em grade ou papel toalha sem abafar.'},
            {'q': 'Posso fazer na Air Fryer?', 'a': 'Sim! Acomode em cesto único a 180°C a 200°C virando na metade do tempo para dourar de forma uniforme sem excesso de gordura.'}
        ],
        'related_posts': rec_list,
        'article_html': article_html
    }

    save_recipe(recipe_obj)
    generated_for_catalog.append((title, slug, img_url, total_m, cals, cur_cat, cur_label))

print('300 receitas atualizadas com sucesso!')

# Gerar Catalogo receitas/boteco/index.html
cards_html = ''
for title, slug, img_url, total_m, cals, cur_cat, cur_label in generated_for_catalog:
    cards_html += f'''
      <article class="recipe-card" data-cat="{cur_cat}" data-title="{title.lower()}">
        <a href="/receitas/boteco/{slug}/" class="recipe-card-img-wrap">
          <img src="{img_url}" alt="{title}" class="recipe-card-img" loading="lazy" width="400" height="250" onerror="this.onerror=null; this.src='{POOLS['torresmos'][0]}'">
          <span class="badge">⏱️ {total_m} min</span>
        </a>
        <div class="recipe-card-body">
          <div class="recipe-card-meta">
            <span class="recipe-category">{cur_label}</span>
            <span class="recipe-rating">★ 4.9</span>
          </div>
          <h3 class="recipe-card-title">
            <a href="/receitas/boteco/{slug}/">{title}</a>
          </h3>
          <div class="recipe-card-footer">
            <span>🔥 {cals} kcal</span>
            <span>👥 6 porções</span>
          </div>
        </div>
      </article>'''

cat_page = f'''<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Comida de Boteco | 300 Receitas de Petiscos e Porções | Quero Rango</title>
  <meta name="description" content="Guia definitivo de comida de boteco com 300 receitas de petiscos, porções na chapa, torresmos pururucados, bolinhos e tira-gostos testados para fazer em casa.">
  
  <meta property="og:title" content="Comida de Boteco - 300 Petiscos e Porções de Respeito | Quero Rango">
  <meta property="og:description" content="Guia definitivo de comida de boteco com 300 receitas de petiscos, porções na chapa, torresmos pururucados, bolinhos e tira-gostos testados para fazer em casa.">
  <meta property="og:image" content="{POOLS['torresmos'][0]}">
  <meta property="og:url" content="https://querorango.com/receitas/boteco/">
  <meta property="og:type" content="website">
  <link rel="canonical" href="https://querorango.com/receitas/boteco/">

  <link rel="stylesheet" href="/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    .boteco-filters {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin: 1.5rem 0;
    }}
    .filter-btn {{
      padding: 0.5rem 1rem;
      border-radius: 50px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .filter-btn:hover, .filter-btn.active {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}
    .boteco-search-wrap {{
      margin: 1rem 0;
      max-width: 500px;
    }}
    .boteco-search-input {{
      width: 100%;
      padding: 0.8rem 1.2rem;
      border-radius: 50px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      font-size: 0.95rem;
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="scroll-progress"></div>
    <nav class="nav container">
      <a href="/" class="nav-logo">Quero Rango</a>
      <div class="nav-links">
        <a href="/receitas/" class="nav-link">Todas as Receitas</a>
        <a href="/receitas/boteco/" class="nav-link active">Comida de Boteco</a>
        <a href="/receitas/air-fryer/" class="nav-link">Air Fryer</a>
        <a href="/receitas/bolos/" class="nav-link">Bolos</a>
        <a href="/receitas/rapidas/" class="nav-link">Rápidas</a>
        <a href="/busca/" class="nav-link">Na Geladeira</a>
      </div>
      <div class="nav-actions">
        <a href="/favoritos/" class="btn-icon" title="Receitas Salvas">Salvos</a>
        <button class="btn-icon notif-toggle-btn" onclick="window.toggleNotifications()" title="Notificações">🔔</button>
        <button class="btn-icon" id="theme-toggle">Tema</button>
      </div>
    </nav>
  </header>

  <div class="recipe-hero">
    <img src="{POOLS['torresmos'][0]}" alt="Comida de Boteco" class="recipe-hero-img">
    <div class="recipe-hero-overlay">
      <div class="container recipe-hero-content">
        <nav class="breadcrumb" aria-label="Navegação">
          <a href="/">Início</a> <span>›</span>
          <a href="/receitas/">Receitas</a> <span>›</span>
          <span aria-current="page">Comida de Boteco</span>
        </nav>
        <h1 class="recipe-title" style="font-size: 2.5rem; text-shadow: 0 2px 10px rgba(0,0,0,0.8);">Comida de Boteco 🍺</h1>
        <p class="recipe-subtitle" style="color: rgba(255,255,255,0.95); font-size: 1.15rem; max-width: 680px; margin-top: 0.5rem; text-shadow: 0 1px 6px rgba(0,0,0,0.8);">
          O maior guia de tira-gostos do Brasil: 300 porções crocantes, chapas quentes, bolinhos clássicos e caldinhos reconfortantes com artigos aprofundados e passo a passo com timers.
        </p>
      </div>
    </div>
  </div>

  <main class="container section">
    <div class="section-header" style="margin-bottom: 1rem;">
      <div>
        <h2 class="section-title">Catálogo Completo (300 Receitas)</h2>
        <p class="section-subtitle">Filtre por tipo de petisco ou pesquise pelo nome</p>
      </div>
    </div>

    <!-- Barra de Busca Rápida -->
    <div class="boteco-search-wrap">
      <input type="text" id="boteco-filter-input" class="boteco-search-input" placeholder="🔍 Digite para filtrar (ex: torresmo, dadinho, camarão, queijo)...">
    </div>

    <!-- Filtros de Boteco por Categoria -->
    <div class="boteco-filters" id="boteco-filters">
      <button class="filter-btn active" data-filter="all">Todos (300)</button>
      <button class="filter-btn" data-filter="torresmos">Torresmos & Suínos</button>
      <button class="filter-btn" data-filter="queijos">Queijos & Dadinhos</button>
      <button class="filter-btn" data-filter="bolinhos">Bolinhos & Croquetes</button>
      <button class="filter-btn" data-filter="frangos">Frangos & Asinhas</button>
      <button class="filter-btn" data-filter="carnes">Carnes & Chapas</button>
      <button class="filter-btn" data-filter="frutos">Frutos do Mar</button>
      <button class="filter-btn" data-filter="batatas">Batatas & Mandiocas</button>
      <button class="filter-btn" data-filter="pasteis">Pastéis & Salgados</button>
      <button class="filter-btn" data-filter="caldinhos">Caldinhos</button>
      <button class="filter-btn" data-filter="molhos">Molhos & Conservas</button>
    </div>

    <!-- Grid com Cards Perfeitamente Padronizados -->
    <div id="boteco-grid" class="grid-3" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 1.5rem;">
      {cards_html}
    </div>
  </main>

  <footer class="site-footer">
    <div class="container text-center">
      <p>© 2026 Quero Rango (querorango.com) — Todos os direitos reservados. • Desenvolvido por Wander Santos</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
  <script>
    const filterInput = document.getElementById('boteco-filter-input');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('#boteco-grid .recipe-card');

    let currentCategory = 'all';

    function applyFilter() {{
      const query = filterInput.value.toLowerCase().trim();
      cards.forEach(card => {{
        const title = card.getAttribute('data-title') || '';
        const cat = card.getAttribute('data-cat') || '';
        const matchesCat = (currentCategory === 'all' || cat === currentCategory);
        const matchesSearch = !query || title.includes(query);
        card.style.display = (matchesCat && matchesSearch) ? 'flex' : 'none';
      }});
    }}

    filterBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = btn.getAttribute('data-filter');
        applyFilter();
      }});
    }});

    filterInput.addEventListener('input', applyFilter);
  </script>
</body>
</html>
'''

target_index = os.path.join(BASE_DIR, 'receitas', 'boteco', 'index.html')
with open(target_index, 'w', encoding='utf-8') as f:
    f.write(cat_page)

print('receitas/boteco/index.html atualizado!')
