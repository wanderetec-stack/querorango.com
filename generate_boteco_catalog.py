import os, sys, glob, json, re

BASE_DIR = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'
SCRATCH_DIR = r'C:\Users\Wander - Rosangela\.gemini\antigravity\brain\33960100-d973-4234-86ad-38085252313a\scratch'
sys.path.insert(0, SCRATCH_DIR)

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

import build_and_publish_boteco_300 as b300
from build_and_publish_boteco_300 import RECIPES_DATA, slugify

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

cards_html = ''
for i, (title, main_ing, sec_ing, prep_m, cook_m, cals) in enumerate(RECIPES_DATA):
    slug = slugify(title)
    img_url = VERIFIED_IMAGES[i % len(VERIFIED_IMAGES)]
    total_m = prep_m + cook_m
    
    cur_cat = 'outros'
    cur_label = 'Petisco'
    for tag_id, label, start, end in groups:
        if start <= i < end:
            cur_cat = tag_id
            cur_label = label
            break
            
    cards_html += f'''
      <article class="recipe-card" data-cat="{cur_cat}" data-title="{title.lower()}">
        <a href="/receitas/boteco/{slug}/" class="recipe-card-img-wrap">
          <img src="{img_url}" alt="{title}" class="recipe-card-img" loading="lazy" width="400" height="250" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800&q=80'">
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
  <meta property="og:image" content="https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=1200&q=80">
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
    <img src="https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=1200&q=80" alt="Comida de Boteco" class="recipe-hero-img">
    <div class="recipe-hero-overlay">
      <div class="container recipe-hero-content">
        <nav class="breadcrumb" aria-label="Navegação">
          <a href="/">Início</a> <span>›</span>
          <a href="/receitas/">Receitas</a> <span>›</span>
          <span aria-current="page">Comida de Boteco</span>
        </nav>
        <h1 class="recipe-title">Comida de Boteco 🍺</h1>
        <p class="recipe-subtitle" style="color: rgba(255,255,255,0.9); font-size: 1.15rem; max-width: 680px; margin-top: 0.5rem;">
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

print('receitas/boteco/index.html gerado com sucesso!')
