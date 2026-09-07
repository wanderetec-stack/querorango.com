# -*- coding: utf-8 -*-
"""
Gera o catalogo geral /receitas/index.html com as 20 categorias e busca rapida
"""
import os
from build_catalog import CATEGORIES_DATA
from build_category_pages import CATEGORY_HERO_IMAGES
from recipe_media_data import get_recipe_info

def build_all_recipes_page():
    featured_cards = []
    for cat in CATEGORIES_DATA:
        cat_slug = cat["cat_slug"]
        cat_name = cat["cat_name"]
        hero_img = CATEGORY_HERO_IMAGES.get(cat_slug, "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500&q=80")
        for rec in cat["recipes"][:2]:
            rec_slug = rec[0]
            rec_title = rec[1]
            main_ing = rec[2]
            cook_t = rec[4]
            rec_url = f"/receitas/{cat_slug}/{rec_slug}/"
            rec_img, rec_desc = get_recipe_info(rec_slug, rec_title, main_ing, cat_slug)
            featured_cards.append(f"""      <article class="card recipe-filter-item" data-category="{cat_slug}" data-title="{rec_title.lower()}">
        <a href="{rec_url}">
          <img class="card-img" src="{rec_img}" alt="{rec_title}" loading="lazy" width="400" height="260">
        </a>
        <div class="card-body">
          <div class="card-meta">
            <span class="tag tag-primary">{cat_name}</span>
            <span>⏱ {cook_t}</span>
            <span>👥 4 porções</span>
          </div>
          <h3 class="card-title"><a href="{rec_url}">{rec_title}</a></h3>
          <p class="card-desc">{rec_desc}</p>
          <div class="stars-meta"><span class="stars">⭐⭐⭐⭐⭐</span><span>4.9 (300+)</span></div>
        </div>
      </article>""")

    cards_html = "\n".join(featured_cards)
    pills = ['<button class="filter-pill active" onclick="filterCategory(\'all\', this)">🔥 Todas (210 receitas)</button>']
    for cat in CATEGORIES_DATA:
        pills.append(f'<button class="filter-pill" onclick="filterCategory(\'{cat["cat_slug"]}\', this)">{cat["cat_name"]}</button>')
    pills_html = "\n      ".join(pills)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Todas as Receitas | Quero Rango (210 Receitas Testadas)</title>
  <meta name="description" content="Explore o acervo completo de receitas do Quero Rango. Filtre por categorias como Air Fryer, Almoço & Jantar, Rápidas, Marmitas, Sobremesas, Sopas e muito mais.">
  <link rel="canonical" href="https://querorango.com/receitas/">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#FF6B35">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    .filter-pills-container {{
      display: flex;
      gap: 0.5rem;
      overflow-x: auto;
      padding-bottom: 0.75rem;
      margin-bottom: 2rem;
      scrollbar-width: thin;
    }}
    .filter-pill {{
      white-space: nowrap;
      padding: 0.5rem 1rem;
      border-radius: 50px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .filter-pill:hover, .filter-pill.active {{
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="scroll-progress"></div>
    <nav class="nav container">
      <a href="/" class="nav-logo"><span class="nav-logo-icon">🍊</span>Quero Rango</a>
      <div class="nav-links">
        <a href="/receitas/" class="nav-link active">Todas as Receitas</a>
        <a href="/receitas/air-fryer/" class="nav-link">Air Fryer</a>
        <a href="/receitas/rapidas/" class="nav-link">Rápidas</a>
        <a href="/receitas/bolos/" class="nav-link">Bolos</a>
        <a href="/receitas/sobremesas/" class="nav-link">Sobremesas</a>
        <a href="/busca/" class="nav-link">🔍 Na Geladeira</a>
      </div>
      <div class="nav-actions">
        <a href="/favoritos/" class="btn-icon">❤️ Salvos</a>
        <button class="btn-icon notif-toggle-btn" onclick="window.toggleNotifications()" title="Notificações">🔔</button>
        <button class="btn-icon" id="theme-toggle">🌙</button>
        <button class="nav-hamburger">☰</button>
      </div>
    </nav>
  </header>

  <main class="container section">
    <nav class="breadcrumb">
      <a href="/">Início</a><span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">Todas as Receitas</span>
    </nav>

    <div class="section-header">
      <div>
        <h1 class="section-title">Catálogo Completo de Receitas 🍳</h1>
        <p class="section-subtitle">Mais de 200 receitas testadas e aprovadas com checklist e timers digitais</p>
      </div>
      <div>
        <input type="text" id="recipe-search-input" placeholder="Filtrar receitas nesta página..." class="form-input" style="max-width: 280px;" oninput="applyFilters()">
      </div>
    </div>

    <!-- Barra de Filtros das 20 Categorias -->
    <div class="filter-pills-container">
      {pills_html}
    </div>

    <!-- Grid de Receitas -->
    <div class="grid-3" id="recipes-grid">
{cards_html}
    </div>

    <div id="no-results" style="display: none; text-align: center; padding: 4rem 1rem;">
      <span style="font-size: 3rem;">🍽️</span>
      <h3 style="margin-top: 1rem;">Nenhuma receita encontrada com esse filtro</h3>
      <p class="text-muted">Tente buscar por outro termo ou navegue pelas categorias acima.</p>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container text-center">
      <p>© 2026 Quero Rango (querorango.com) — Todos os direitos reservados.</p>
      <div style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 1rem; font-size: 0.9rem;">
        <a href="/sobre/">Sobre Nós</a>
        <a href="/contato/">Fale Conosco</a>
        <a href="/politica-de-privacidade/">Privacidade</a>
        <a href="/termos-de-uso/">Termos de Uso</a>
      </div>
    </div>
  </footer>

  <script src="/js/main.js"></script>
  <script>
    let currentCategory = 'all';

    function filterCategory(catSlug, btn) {{
      currentCategory = catSlug;
      document.querySelectorAll('.filter-pill').forEach(el => el.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyFilters();
    }}

    function applyFilters() {{
      const query = document.getElementById('recipe-search-input').value.toLowerCase().trim();
      const items = document.querySelectorAll('.recipe-filter-item');
      let visibleCount = 0;

      items.forEach(item => {{
        const matchesCategory = currentCategory === 'all' || item.dataset.category === currentCategory;
        const matchesSearch = !query || item.dataset.title.includes(query);

        if (matchesCategory && matchesSearch) {{
          item.style.display = '';
          visibleCount++;
        }} else {{
          item.style.display = 'none';
        }}
      }});

      document.getElementById('no-results').style.display = visibleCount === 0 ? 'block' : 'none';
    }}
  </script>
</body>
</html>"""

    target_path = r"c:\Users\Wander - Rosangela\Desktop\site de receitas\receitas\index.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Catalogo geral /receitas/index.html atualizado com sucesso!")

if __name__ == "__main__":
    build_all_recipes_page()
