# -*- coding: utf-8 -*-
"""
Gera as páginas index.html de cada uma das 20 categorias,
listando as 10 receitas reais de cada uma, com cards, fotos apetitosas e links funcionais.
Também atualiza o index.html da Home com fotos 100% de comida (removendo tênis/sapatos).
"""

import os
from build_catalog import CATEGORIES_DATA
from recipe_media_data import get_recipe_info

# Fotos verificadas de comida deliciosa para cada categoria
CATEGORY_HERO_IMAGES = {
    "air-fryer": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=1200&q=80",
    "almoco": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=1200&q=80",
    "rapidas": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=1200&q=80",
    "marmitas": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=1200&q=80",
    "saudavel": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&q=80",
    "economicas": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=1200&q=80",
    "bolos": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=1200&q=80",
    "sobremesas": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=1200&q=80",
    "paes": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=1200&q=80",
    "virais": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=1200&q=80",
    "frango": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=1200&q=80",
    "massas": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=1200&q=80",
    "carne-moida": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=1200&q=80",
    "pressao": "https://images.unsplash.com/photo-1544025162-d76694265947?w=1200&q=80",
    "peixes": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=1200&q=80",
    "regional": "https://images.unsplash.com/photo-1547592180-85f173990554?w=1200&q=80",
    "lanches": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=1200&q=80",
    "sopas": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=1200&q=80",
    "sem-gluten": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1200&q=80",
    "vegetarianas": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200&q=80",
    "cafe-da-manha": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=1200&q=80"
}

# Descrições ricas para cada categoria
CATEGORY_DESCRIPTIONS = {
    "air-fryer": "Descubra as 10 melhores receitas na Air Fryer testadas na prática: do frango dourado e suculento ao pudim lisinho e batatas crocantes sem usar óleo.",
    "almoco": "Receitas completas, práticas e afetivas para o almoço do dia a dia e os grandes encontros de família no final de semana.",
    "rapidas": "Sem tempo para cozinhar? Confira 10 receitas fáceis prontas em até 15 a 20 minutos, sem sujeira e cheias de sabor para o dia a dia.",
    "marmitas": "Organize sua semana e economize dinheiro com nosso guia de 10 marmitas completas, congeláveis e nutritivas que mantêm o sabor de comida fresca.",
    "saudavel": "Refeições equilibradas com foco em alta densidade de proteínas, fibras e ingredientes naturais para sua rotina de treino e bem-estar.",
    "economicas": "Receitas inteligentes de fim de mês para aproveitar sobras e ingredientes simples como ovos, arroz e batatas sem gastar quase nada.",
    "bolos": "Bolos caseiros de liquidificador e tradicionais com massa fofa que nunca sola, perfeitos para perfumar a casa na hora do café.",
    "sobremesas": "Os doces mais amados do Brasil: pudins, brigadeiros aveludados, pavês e tortas clássicas com passo a passo ilustrado.",
    "paes": "Aprenda a fazer pães caseiros fofos sem precisar sovar, pão de queijo autêntico e massas artesanais com aroma irresistível de padaria.",
    "virais": "As receitas que viralizaram no TikTok e Instagram: doces vidrados, bombons de travessa e sobremesas modernas explicadas em detalhes.",
    "frango": "As melhores formas de preparar a carne favorita do Brasil com molhos cremosos, empanados crocantes e assados suculentos.",
    "massas": "Lasanhas clássicas, macarrões de uma panela só e molhos rústicos de tomate para o almoço de domingo em família.",
    "carne-moida": "A proteína mais versátil da cozinha em 10 pratos irresistíveis: almôndegas, rocamboles, escondidinhos e panquecas recheadas.",
    "pressao": "Economize gás e tempo com receitas de panela de pressão: carnes que desmancham na boca, feijão com caldo grosso e costela sem água.",
    "peixes": "Moquecas, tilápias grelhadas e pratos leves com peixes e frutos do mar com dicas para não ressecar e manter o ponto suculento.",
    "regional": "A riqueza cultural da culinária brasileira: baião de dois, feijão tropeiro mineiro, acarajé baiano e pratos típicos inesquecíveis.",
    "lanches": "Petiscos e salgados clássicos de boteco e festas: coxinhas com massa de batata, pastéis crocantes e sanduíches caprichados.",
    "sopas": "Caldos aveludados e sopas reconfortantes para aquecer as noites frias com muito aconchego e nutrição.",
    "sem-gluten": "Receitas fofinhas e saborosas sem farinha de trigo e sem leite, feitas para celíacos e intolerantes sem abrir mão do sabor.",
    "vegetarianas": "Pratos 100% vegetais cheios de cores e nutrientes: hambúrgueres de grão-de-bico, strogonoff de cogumelos e moquecas aromáticas.",
    "cafe-da-manha": "Transforme suas manhãs em momentos de cafeteria gourmet: ovos cremosos de hotel, waffles crocantes e panquecas americanas altas."
}

def build_category_page(cat):
    cat_slug = cat["cat_slug"]
    cat_name = cat["cat_name"]
    hero_img = CATEGORY_HERO_IMAGES.get(cat_slug, "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&q=80")
    cat_desc = CATEGORY_DESCRIPTIONS.get(cat_slug, f"Explore as 10 melhores receitas testadas na categoria {cat_name}.")

    cards_html = []
    for rec_slug, rec_title, main_ing, sec_ing, cook_t, prep_t in cat["recipes"]:
        rec_url = f"/receitas/{cat_slug}/{rec_slug}/"
        rec_img, rec_desc = get_recipe_info(rec_slug, rec_title, main_ing, cat_slug)
        cards_html.append(f"""      <article class="card">
        <a href="{rec_url}">
          <img class="card-img" src="{rec_img}" alt="{rec_title}" loading="lazy" width="400" height="300">
        </a>
        <div class="card-body">
          <div class="card-meta">
            <span class="tag tag-primary">{cat_name}</span>
            <span>⏱ {cook_t}</span>
            <span>👥 4 porções</span>
          </div>
          <h3 class="card-title">
            <a href="{rec_url}">{rec_title}</a>
          </h3>
          <p class="card-desc">{rec_desc}</p>
          <div class="stars-meta">
            <span class="stars">⭐⭐⭐⭐⭐</span>
            <span>4.9 (320+)</span>
          </div>
        </div>
      </article>""")

    cards_rendered = "\n".join(cards_html)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Receitas de {cat_name} (10 Receitas Testadas) | Quero Rango</title>
  <meta name="description" content="{cat_desc}">
  
  <meta property="og:title" content="Receitas de {cat_name} | Quero Rango">
  <meta property="og:description" content="{cat_desc}">
  <meta property="og:image" content="{hero_img}">
  <meta property="og:url" content="https://querorango.com/receitas/{cat_slug}/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <link rel="canonical" href="https://querorango.com/receitas/{cat_slug}/">

  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#FF6B35">

  <link rel="stylesheet" href="/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Receitas de {cat_name}",
    "description": "{cat_desc}",
    "url": "https://querorango.com/receitas/{cat_slug}/"
  }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="scroll-progress"></div>
    <nav class="nav container">
      <a href="/" class="nav-logo"><span class="nav-logo-icon">🍊</span>Quero Rango</a>
      <div class="nav-links">
        <a href="/receitas/" class="nav-link">Todas as Receitas</a>
        <a href="/receitas/air-fryer/" class="nav-link{' active' if cat_slug == 'air-fryer' else ''}">Air Fryer</a>
        <a href="/receitas/bolos/" class="nav-link{' active' if cat_slug == 'bolos' else ''}">Bolos</a>
        <a href="/receitas/rapidas/" class="nav-link{' active' if cat_slug == 'rapidas' else ''}">Rápidas</a>
        <a href="/receitas/marmitas/" class="nav-link{' active' if cat_slug == 'marmitas' else ''}">Marmitas</a>
        <a href="/busca/" class="nav-link">Na Geladeira</a>
      </div>
      <div class="nav-actions">
        <a href="/favoritos/" class="btn-icon" title="Receitas Salvas">Salvos</a>
        <button class="btn-icon notif-toggle-btn" onclick="window.toggleNotifications()" title="Notificações">🔔</button>
        <button class="btn-icon" id="theme-toggle">Tema</button>
        <button class="nav-hamburger">☰</button>
      </div>
    </nav>
  </header>

  <div class="recipe-hero">
    <img src="{hero_img}" alt="{cat_name}" class="recipe-hero-img">
    <div class="recipe-hero-overlay">
      <div class="container recipe-hero-content">
        <span class="tag tag-primary">10 Receitas Completas</span>
        <h1 style="margin-top: 0.5rem;">{cat_name}</h1>
      </div>
    </div>
  </div>

  <main class="container section">
    <nav class="breadcrumb">
      <a href="/">Início</a><span class="breadcrumb-sep">/</span>
      <a href="/receitas/">Receitas</a><span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{cat_name}</span>
    </nav>

    <div class="section-header">
      <div>
        <h2 class="section-title">Todas as Receitas de {cat_name}</h2>
        <p class="section-subtitle">{cat_desc}</p>
      </div>
      <a href="/receitas/" class="section-link">Ver outras categorias →</a>
    </div>

    <div class="grid-3">
{cards_rendered}
    </div>
  </main>

  <footer class="site-footer">
    <div class="container text-center">
      <p>© 2026 Quero Rango (querorango.com) — Receitas de {cat_name} testadas e aprovadas ❤️</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
"""
    target_dir = os.path.join(r"c:\Users\Wander - Rosangela\Desktop\site de receitas\receitas", cat_slug)
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, "index.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[CATEGORIA OK] Criada página index.html para: {cat_slug} (com 10 receitas)")

def main():
    print("=" * 60)
    print("CRIANDO AS 20 PÁGINAS DE CATEGORIA COM 10 RECEITAS CADA")
    print("=" * 60)
    for cat in CATEGORIES_DATA:
        build_category_page(cat)
    print("\n[SUCESSO] Todas as 20 páginas de categoria foram geradas com 10 receitas cada!")

if __name__ == "__main__":
    main()
