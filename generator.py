"""
Gerador de Receitas Autênticas e Artigos Longos (>1000 palavras) para querorango.com
Cria receitas estruturadas com SEO, Schema.org Recipe, Checklist, Timers e Conteúdo Editorial 100% Autoral.
"""

import os
import re
import json

CATEGORIES_MAP = {
    "air-fryer": "Air Fryer",
    "rapidas": "Rápidas (15 a 20 min)",
    "marmitas": "Marmitas & Meal Prep",
    "saudavel": "Saudável & High Protein",
    "economicas": "Econômicas & Fim de Mês",
    "bolos": "Bolos Caseiros",
    "sobremesas": "Doces & Sobremesas",
    "paes": "Pães & Massas",
    "virais": "Doces Virais das Redes",
    "frango": "Frango & Aves",
    "massas": "Massas & Lasanhas",
    "carne-moida": "Carne Moída",
    "pressao": "Panela de Pressão",
    "peixes": "Peixes & Frutos do Mar",
    "regional": "Culinária Regional",
    "lanches": "Lanches & Petiscos",
    "sopas": "Sopas & Caldos",
    "sem-gluten": "Sem Glúten & Sem Lactose",
    "vegetarianas": "Vegetarianas & Veganas",
    "cafe-da-manha": "Café da Manhã & Brunch"
}

def generate_recipe_html(recipe):
    cat_slug = recipe["category_slug"]
    cat_name = CATEGORIES_MAP.get(cat_slug, "Geral")
    title = recipe["title"]
    slug = recipe["slug"]
    prep_time = recipe.get("prep_time", "15 min")
    cook_time = recipe.get("cook_time", "25 min")
    total_time = recipe.get("total_time", "40 min")
    yield_portions = recipe.get("yield_portions", "4 porções")
    base_portions = recipe.get("base_portions", 4)
    calories = recipe.get("calories", "320 kcal")
    rating = recipe.get("rating", "4.9")
    rating_count = recipe.get("rating_count", "240")
    image_url = recipe.get("image_url", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&q=85")
    
    ingredients = recipe["ingredients"]
    steps = recipe["steps"]
    article_html = recipe["article_html"]
    faq = recipe.get("faq", [])
    nutrition = recipe.get("nutrition", {
        "Calorias": calories,
        "Carboidratos": "35g",
        "Proteínas": "24g",
        "Gorduras": "12g",
        "Fibras": "4g",
        "Sódio": "310mg"
    })

    # Schema Ingredients JSON
    schema_ingredients = json.dumps([f"{ing.get('amount', '')} {ing.get('unit', '')} {ing['name']}".strip() for ing in ingredients], ensure_ascii=False)
    
    # Schema Steps JSON
    schema_steps = json.dumps([
        {
            "@type": "HowToStep",
            "name": f"Passo {i+1}",
            "text": step["text"]
        } for i, step in enumerate(steps)
    ], ensure_ascii=False)

    # HTML dos Ingredientes
    ing_html_list = []
    for ing in ingredients:
        amount = ing.get("amount", "")
        unit = ing.get("unit", "")
        name = ing["name"]
        data_unit_attr = f' data-unit="{unit}"' if unit else ''
        data_amount_attr = f' data-amount="{amount}"' if amount else ''
        display_amount = f"{amount} {unit}".strip() if amount or unit else ""
        
        ing_html_list.append(f"""            <li class="ingredient-item">
              <span class="ingredient-checkbox">✓</span>
              {f'<span class="ingredient-amount"{data_amount_attr}{data_unit_attr}>{display_amount}</span>' if display_amount else ''}
              <span class="ingredient-text">{name}</span>
            </li>""")
    ingredients_rendered = "\n".join(ing_html_list)

    # HTML dos Passos
    steps_html_list = []
    for i, step in enumerate(steps):
        timer_btn = ""
        if "timer_minutes" in step and step["timer_minutes"] > 0:
            timer_btn = f"""\n                <button class="step-timer-btn" data-minutes="{step['timer_minutes']}" data-label="{step.get('timer_label', f'Passo {i+1}')}">⏱ Iniciar Timer ({step['timer_minutes']} min)</button>"""
        
        steps_html_list.append(f"""            <div class="step-item">
              <div class="step-number">{i+1}</div>
              <div class="step-content">
                <div class="step-text">{step['text']}</div>{timer_btn}
              </div>
            </div>""")
    steps_rendered = "\n".join(steps_html_list)

    # HTML do FAQ
    faq_html_list = []
    for item in faq:
        faq_html_list.append(f"""          <div class="faq-item">
            <button class="faq-question">
              <span>{item['q']}</span>
              <span class="faq-icon">▼</span>
            </button>
            <div class="faq-answer">
              <div class="faq-answer-inner">{item['a']}</div>
            </div>
          </div>""")
    faq_rendered = "\n".join(faq_html_list)

    # HTML da Tabela Nutricional
    nutrition_rows = "\n".join([f"              <tr><td>{k}</td><td>{v}</td></tr>" for k, v in nutrition.items()])

    # Posts Relacionados Categoria-Específicos (sem cross-category)
    RELATED_BY_CAT = {
        "boteco": [
            {"title": "Torresmo de Rolo Pururucado Clássico", "url": "/receitas/boteco/torresmo-de-rolo-pururucado-classico/", "img": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=600&q=80", "time": "65 min", "cat": "Comida de Boteco"},
            {"title": "Dadinho de Tapioca com Geleia de Pimenta", "url": "/receitas/boteco/dadinho-de-tapioca-classico-com-queijo-coalho-e-geleia-de-pimenta/", "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80", "time": "35 min", "cat": "Comida de Boteco"},
            {"title": "Mandioca Frita Crocante por Fora e Cremosa", "url": "/receitas/boteco/mandioca-frita-crocante-por-fora-e-cremosa-por-dentro/", "img": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=600&q=80", "time": "35 min", "cat": "Comida de Boteco"},
            {"title": "Bolinho de Feijoada com Couve e Bacon", "url": "/receitas/boteco/bolinho-de-feijoada-tradicional-com-couve-refogada-e-bacon/", "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=600&q=80", "time": "50 min", "cat": "Comida de Boteco"},
            {"title": "Calabresa Flambada na Cachaça com Cebola", "url": "/receitas/boteco/linguica-calabresa-flambada-na-cachaca-com-cebola-roxa/", "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80", "time": "25 min", "cat": "Comida de Boteco"}
        ],
        "air-fryer": [
            {"title": "Frango Crocante na Air Fryer", "url": "/receitas/air-fryer/coxa-de-frango-crocante-na-air-fryer-com-marinada-de-mostarda/", "img": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=600&q=80", "time": "35 min", "cat": "Air Fryer"},
            {"title": "Batata Frita na Air Fryer sem Óleo", "url": "/receitas/air-fryer/batata-frita-crocante-na-air-fryer-sem-oleo/", "img": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80", "time": "25 min", "cat": "Air Fryer"},
            {"title": "Chips de Abobrinha na Air Fryer", "url": "/receitas/air-fryer/chips-de-abobrinha-na-air-fryer-super-sequinhas-com-parmesao/", "img": "https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=600&q=80", "time": "20 min", "cat": "Air Fryer"},
            {"title": "Banana Assada na Air Fryer com Canela", "url": "/receitas/air-fryer/banana-assada-na-air-fryer-com-canela-e-pasta-de-amendoim/", "img": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=600&q=80", "time": "15 min", "cat": "Air Fryer"}
        ],
        "bolos": [
            {"title": "Bolo de Cenoura com Cobertura de Chocolate", "url": "/receitas/bolos/bolo-de-cenoura-classico-com-cobertura-de-chocolate/", "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80", "time": "60 min", "cat": "Bolos"},
            {"title": "Bolo de Milho Cremoso", "url": "/receitas/bolos/bolo-de-milho-cremoso-de-lata/", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80", "time": "50 min", "cat": "Bolos"},
            {"title": "Bolo de Chocolate Fudge", "url": "/receitas/bolos/bolo-de-chocolate-fudge-ultra-molhado/", "img": "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600&q=80", "time": "55 min", "cat": "Bolos"},
            {"title": "Bolo Toalha Felpuda de Coco", "url": "/receitas/bolos/bolo-toalha-felpuda-molhadinho-de-coco-caseiro-classico/", "img": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80", "time": "60 min", "cat": "Bolos"}
        ],
        "sobremesas": [
            {"title": "Brigadeiro de Colher Cremoso", "url": "/receitas/sobremesas/brigadeiro-de-colher-cremoso/", "img": "https://images.unsplash.com/photo-1528975604071-b4dc52a2d18c?w=600&q=80", "time": "20 min", "cat": "Sobremesas"},
            {"title": "Mousse de Chocolate 3 Ingredientes", "url": "/receitas/sobremesas/mousse-de-chocolate-3-ingredientes/", "img": "https://images.unsplash.com/photo-1541599188778-cdc73298e8fd?w=600&q=80", "time": "25 min", "cat": "Sobremesas"},
            {"title": "Manjar Branco de Coco com Calda de Ameixa", "url": "/receitas/sobremesas/manjar-branco-de-coco-com-calda-de-ameixa-caseiro-classico/", "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600&q=80", "time": "30 min", "cat": "Sobremesas"},
            {"title": "Pudim de Leite Condensado Clássico", "url": "/receitas/sobremesas/pudim-de-leite-condensado-classico/", "img": "https://images.unsplash.com/photo-1559620192-032c4bc4674e?w=600&q=80", "time": "70 min", "cat": "Sobremesas"}
        ],
        "frango": [
            {"title": "Frango Assado com Batatas Rústicas", "url": "/receitas/frango/frango-assado-com-batatas-rusticas/", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=600&q=80", "time": "80 min", "cat": "Frango"},
            {"title": "Frango ao Molho de Mostarda e Mel", "url": "/receitas/frango/frango-ao-molho-de-mostarda-e-mel/", "img": "https://images.unsplash.com/photo-1569691899455-88464f6d3ab1?w=600&q=80", "time": "45 min", "cat": "Frango"},
            {"title": "Coxinhas da Asa Douradas com Alho", "url": "/receitas/air-fryer/coxinhas-da-asa-douradas-com-alho-e-ervas-caseiro-classico/", "img": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=600&q=80", "time": "40 min", "cat": "Frango"}
        ],
        "almoco": [
            {"title": "Filé Mignon Suíno com Geleia de Pimenta", "url": "/receitas/almoco/file-mignon-suino-com-geleia-de-pimenta-caseiro-classico/", "img": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80", "time": "50 min", "cat": "Almoço"},
            {"title": "Arroz com Frango Caipira", "url": "/receitas/almoco/arroz-com-frango-caipira/", "img": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&q=80", "time": "65 min", "cat": "Almoço"},
            {"title": "Carne Assada ao Molho Madeira", "url": "/receitas/almoco/carne-assada-ao-molho-madeira/", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80", "time": "90 min", "cat": "Almoço"}
        ],
        "marmitas": [
            {"title": "Iscas de Carne Acebolada com Pimentão", "url": "/receitas/marmitas/iscas-de-carne-aceboladas-com-pimentao-caseiro-classico/", "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80", "time": "35 min", "cat": "Marmitas"},
            {"title": "Arroz Integral com Frango e Legumes", "url": "/receitas/marmitas/arroz-integral-com-frango-e-legumes/", "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=600&q=80", "time": "40 min", "cat": "Marmitas"},
            {"title": "Macarrão Integral com Atum e Tomate", "url": "/receitas/marmitas/macarrao-integral-com-atum-e-tomate/", "img": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=600&q=80", "time": "25 min", "cat": "Marmitas"}
        ],
        "rapidas": [
            {"title": "Macarrão Alho e Óleo com Tomatinhos", "url": "/receitas/rapidas/macarrao-alho-e-oleo-com-tomatinhos-cereja-e-manjericao-fresco/", "img": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=600&q=80", "time": "20 min", "cat": "Rápidas"},
            {"title": "Frittata de Espinafre com Ricota", "url": "/receitas/rapidas/frittata-de-espinafre-com-ricota-de-frigideira/", "img": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600&q=80", "time": "15 min", "cat": "Rápidas"},
            {"title": "Quesadilla de Queijo e Milho", "url": "/receitas/rapidas/quesadilla-rapida-de-queijo-e-milho-na-frigideira/", "img": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80", "time": "15 min", "cat": "Rápidas"}
        ],
        "saudavel": [
            {"title": "Salada de Quinoa com Legumes Grelhados", "url": "/receitas/saudavel/salada-de-quinoa-com-legumes-grelhados/", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80", "time": "35 min", "cat": "Saudável"},
            {"title": "Panqueca Proteica de Claras com Cacau", "url": "/receitas/saudavel/panqueca-proteica-de-claras-com-cacau-e-banana-caseiro-classico/", "img": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=600&q=80", "time": "20 min", "cat": "Saudável"},
            {"title": "Bowl de Açaí com Frutas e Granola", "url": "/receitas/saudavel/bowl-de-acai-com-frutas-e-granola/", "img": "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=600&q=80", "time": "10 min", "cat": "Saudável"}
        ],
        "massas": [
            {"title": "Lasanha à Bolonhesa Clássica", "url": "/receitas/massas/lasanha-a-bolonhesa-classica/", "img": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=600&q=80", "time": "75 min", "cat": "Massas"},
            {"title": "Espaguete ao Molho Carbonara", "url": "/receitas/massas/espaguete-ao-molho-carbonara/", "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80", "time": "30 min", "cat": "Massas"},
            {"title": "Talharim ao Pesto com Castanhas", "url": "/receitas/massas/talharim-ao-pesto-genoves-com-castanhas-caseiro-classico/", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80", "time": "25 min", "cat": "Massas"}
        ]
    }
    default_related = RELATED_BY_CAT.get(cat_slug, RELATED_BY_CAT["almoco"])
    
    cur_url = f"/receitas/{cat_slug}/{slug}/"
    raw_list = recipe.get("related_posts", default_related)
    related_list = [d for d in raw_list if d.get("url") != cur_url and slug not in d.get("url", "")][:3]
    
    related_html_cards = []
    for item in related_list:
        related_html_cards.append(f"""            <article class="card">
              <a href="{item['url']}">
                <img class="card-img" src="{item['img']}" alt="{item['title']}" loading="lazy" style="height: 160px; object-fit: cover;">
              </a>
              <div class="card-body">
                <span class="tag tag-primary" style="font-size: 0.7rem;">{item.get('cat', 'Receita')}</span>
                <h3 class="card-title mt-1" style="font-size: 0.95rem;"><a href="{item['url']}">{item['title']}</a></h3>
                <small class="text-muted">⏱ {item.get('time', '30 min')} • ⭐ 4.9</small>
              </div>
            </article>""")
    related_rendered = "\n".join(related_html_cards)

    sidebar_cards = []
    for item in related_list[:2]:
        sidebar_cards.append(f"""            <a href="{item['url']}" style="display: flex; gap: 0.75rem; text-decoration: none; color: var(--text);">
              <img src="{item['img']}" style="width: 54px; height: 54px; object-fit: cover; border-radius: 8px;" alt="{item['title']}">
              <div>
                <strong style="font-size: 0.85rem; display: block;">{item['title']}</strong>
                <small class="text-muted">⏱ {item.get('time', '30 min')} • ⭐ 4.9</small>
              </div>
            </a>""")
    sidebar_related_rendered = "\n".join(sidebar_cards)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Quero Rango</title>
  <meta name="description" content="{recipe.get('meta_description', title)}">
  
  <meta property="og:title" content="{title} | Quero Rango">
  <meta property="og:description" content="{recipe.get('meta_description', title)}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:url" content="https://querorango.com/receitas/{cat_slug}/{slug}/">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="pt_BR">
  <link rel="canonical" href="https://querorango.com/receitas/{cat_slug}/{slug}/">

  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#FF6B35">

  <link rel="stylesheet" href="/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org Recipe -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Recipe",
    "name": "{title}",
    "image": ["{image_url}"],
    "author": {{
      "@type": "Person",
      "name": "Equipe Quero Rango"
    }},
    "datePublished": "2026-09-05",
    "description": "{recipe.get('meta_description', title)}",
    "prepTime": "PT{recipe.get('prep_minutes', 15)}M",
    "cookTime": "PT{recipe.get('cook_minutes', 25)}M",
    "totalTime": "PT{recipe.get('total_minutes', 40)}M",
    "recipeYield": "{yield_portions}",
    "recipeCategory": "{cat_name}",
    "recipeCuisine": "Brasileira",
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "{rating}",
      "reviewCount": "{rating_count}"
    }},
    "recipeIngredient": {schema_ingredients},
    "recipeInstructions": {schema_steps}
  }}
  </script>

  <!-- Schema.org BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://querorango.com/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "{cat_name}",
        "item": "https://querorango.com/receitas/{cat_slug}/"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{title}",
        "item": "https://querorango.com/receitas/{cat_slug}/{slug}/"
      }}
    ]
  }}
  </script>
</head>
<body>
  <input type="hidden" id="recipe-id" value="{slug}">

  <header class="site-header">
    <div class="scroll-progress"></div>
    <nav class="nav container">
      <a href="/" class="nav-logo">
        <span class="nav-logo-accent">Quero</span> Rango
      </a>
      <div class="nav-links">
        <a href="/" class="nav-link">Início</a>
        <a href="/receitas/boteco/" class="nav-link nav-highlight">🍺 Comida de Boteco</a>

        <!-- Dropdown com Todas as Categorias -->
        <div class="nav-dropdown">
          <button class="nav-dropdown-btn" type="button" aria-haspopup="true" aria-expanded="false">
            Categorias ▾
          </button>
          <div class="nav-dropdown-menu">
            <div class="dropdown-group">
              <div class="dropdown-group-title">Petiscos & Rápidas</div>
              <a href="/receitas/boteco/" class="dropdown-item">
                <span class="item-name">🍺 Comida de Boteco</span>
                <span class="item-count">300+</span>
              </a>
              <a href="/receitas/air-fryer/" class="dropdown-item">
                <span class="item-name">⚡ Air Fryer</span>
                <span class="item-count">Crocante</span>
              </a>
              <a href="/receitas/rapidas/" class="dropdown-item">
                <span class="item-name">⏱️ Rápidas (15 min)</span>
                <span class="item-count">Práticas</span>
              </a>
              <a href="/receitas/lanches/" class="dropdown-item">
                <span class="item-name">🥪 Lanches & Petiscos</span>
                <span class="item-count">Sanduíches</span>
              </a>
              <a href="/receitas/pressao/" class="dropdown-item">
                <span class="item-name">🍲 Panela de Pressão</span>
                <span class="item-count">Carnes & Caldos</span>
              </a>
              <a href="/receitas/economicas/" class="dropdown-item">
                <span class="item-name">💰 Econômicas</span>
                <span class="item-count">Fim de mês</span>
              </a>
            </div>

            <div class="dropdown-group">
              <div class="dropdown-group-title">Almoço, Jantar & Carnes</div>
              <a href="/receitas/almoco/" class="dropdown-item">
                <span class="item-name">🍽️ Almoço & Jantar</span>
                <span class="item-count">Completas</span>
              </a>
              <a href="/receitas/frango/" class="dropdown-item">
                <span class="item-name">🍗 Frango & Aves</span>
                <span class="item-count">Assados</span>
              </a>
              <a href="/receitas/massas/" class="dropdown-item">
                <span class="item-name">🍝 Massas & Lasanhas</span>
                <span class="item-count">Molhos</span>
              </a>
              <a href="/receitas/carne-moida/" class="dropdown-item">
                <span class="item-name">🥩 Carne Moída</span>
                <span class="item-count">Versátil</span>
              </a>
              <a href="/receitas/peixes/" class="dropdown-item">
                <span class="item-name">🐟 Peixes & Frutos do Mar</span>
                <span class="item-count">Frescos</span>
              </a>
              <a href="/receitas/regional/" class="dropdown-item">
                <span class="item-name">🇧🇷 Culinária Regional</span>
                <span class="item-count">Tradição</span>
              </a>
            </div>

            <div class="dropdown-group">
              <div class="dropdown-group-title">Doces & Confeitaria</div>
              <a href="/receitas/bolos/" class="dropdown-item">
                <span class="item-name">🎂 Bolos Caseiros</span>
                <span class="item-count">Fofinhos</span>
              </a>
              <a href="/receitas/sobremesas/" class="dropdown-item">
                <span class="item-name">🍮 Sobremesas & Pudins</span>
                <span class="item-count">Doces</span>
              </a>
              <a href="/receitas/paes/" class="dropdown-item">
                <span class="item-name">🍞 Pães & Padaria</span>
                <span class="item-count">Massas</span>
              </a>
              <a href="/receitas/virais/" class="dropdown-item">
                <span class="item-name">✨ Doces Virais</span>
                <span class="item-count">Tendências</span>
              </a>
              <a href="/receitas/cafe-da-manha/" class="dropdown-item">
                <span class="item-name">☕ Café & Brunch</span>
                <span class="item-count">Manhã</span>
              </a>
            </div>

            <div class="dropdown-group">
              <div class="dropdown-group-title">Saudável & Especial</div>
              <a href="/receitas/saudavel/" class="dropdown-item">
                <span class="item-name">🥗 Saudável & Fit</span>
                <span class="item-count">Proteína</span>
              </a>
              <a href="/receitas/marmitas/" class="dropdown-item">
                <span class="item-name">🍱 Marmitas & Meal Prep</span>
                <span class="item-count">Semanal</span>
              </a>
              <a href="/receitas/sopas/" class="dropdown-item">
                <span class="item-name">🥣 Sopas & Caldos</span>
                <span class="item-count">Conforto</span>
              </a>
              <a href="/receitas/vegetarianas/" class="dropdown-item">
                <span class="item-name">🌱 Vegetarianas & Veganas</span>
                <span class="item-count">Vegetais</span>
              </a>
              <a href="/receitas/sem-gluten/" class="dropdown-item">
                <span class="item-name">🌾 Sem Glúten & Lactose</span>
                <span class="item-count">Leve</span>
              </a>
              <a href="/receitas/" class="dropdown-item" style="border-top: 1px dashed var(--border); margin-top: 0.25rem; font-weight: 700; color: var(--primary);">
                <span class="item-name">📖 Ver Todas as Receitas</span>
                <span class="item-count">→</span>
              </a>
            </div>
          </div>
        </div>

        <a href="/receitas/air-fryer/" class="nav-link">Air Fryer</a>
        <a href="/receitas/rapidas/" class="nav-link">Rápidas</a>
        <a href="/busca/" class="nav-link">Na Geladeira 🔍</a>
      </div>
      <div class="nav-actions">
        <button class="btn-icon notif-toggle-btn" onclick="window.toggleNotifications()" title="Notificações" aria-label="Notificações">🔔</button>
        <button class="btn-icon" id="theme-toggle" title="Alternar tema" aria-label="Modo escuro">🌙</button>
        <button class="nav-hamburger" aria-label="Menu" aria-expanded="false">☰</button>
      </div>
    </nav>
    <nav class="mobile-menu" aria-label="Menu mobile">
      <a href="/" class="nav-link">🏠 Início</a>
      <a href="/receitas/boteco/" class="nav-link nav-highlight">🍺 Especial Comida de Boteco (300)</a>
      <a href="/receitas/" class="nav-link">📖 Todas as Receitas (500+)</a>
      <a href="/busca/" class="nav-link">🔍 O que tem na geladeira?</a>

      <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: var(--primary); margin: 0.75rem 0 0.25rem 0.5rem;">
        Todas as Categorias
      </div>
      <div class="mobile-categories-grid">
        <a href="/receitas/boteco/" class="mobile-category-link">🍺 Boteco</a>
        <a href="/receitas/air-fryer/" class="mobile-category-link">⚡ Air Fryer</a>
        <a href="/receitas/rapidas/" class="mobile-category-link">⏱️ Rápidas</a>
        <a href="/receitas/almoco/" class="mobile-category-link">🍽️ Almoço</a>
        <a href="/receitas/bolos/" class="mobile-category-link">🎂 Bolos</a>
        <a href="/receitas/sobremesas/" class="mobile-category-link">🍮 Sobremesas</a>
        <a href="/receitas/frango/" class="mobile-category-link">🍗 Frango</a>
        <a href="/receitas/massas/" class="mobile-category-link">🍝 Massas</a>
        <a href="/receitas/carne-moida/" class="mobile-category-link">🥩 Carne Moída</a>
        <a href="/receitas/saudavel/" class="mobile-category-link">🥗 Saudável</a>
        <a href="/receitas/marmitas/" class="mobile-category-link">🍱 Marmitas</a>
        <a href="/receitas/paes/" class="mobile-category-link">🍞 Pães</a>
        <a href="/receitas/peixes/" class="mobile-category-link">🐟 Peixes</a>
        <a href="/receitas/pressao/" class="mobile-category-link">🍲 Pressão</a>
        <a href="/receitas/lanches/" class="mobile-category-link">🥪 Lanches</a>
        <a href="/receitas/sopas/" class="mobile-category-link">🥣 Sopas</a>
        <a href="/receitas/economicas/" class="mobile-category-link">💰 Econômicas</a>
        <a href="/receitas/virais/" class="mobile-category-link">✨ Virais</a>
        <a href="/receitas/regional/" class="mobile-category-link">🇧🇷 Regional</a>
        <a href="/receitas/cafe-da-manha/" class="mobile-category-link">☕ Café</a>
        <a href="/receitas/sem-gluten/" class="mobile-category-link">🌾 Sem Glúten</a>
        <a href="/receitas/vegetarianas/" class="mobile-category-link">🌱 Veganas</a>
      </div>

      <a href="/sobre/" class="nav-link">ℹ️ Sobre o Quero Rango</a>
    </nav>
  </header>

  <div class="recipe-hero">
    <img src="{image_url}" alt="{title}" class="recipe-hero-img">
    <div class="recipe-hero-overlay">
      <div class="container recipe-hero-content">
        <span class="tag tag-primary">{cat_name}</span>
        <h1 id="recipe-title" style="margin-top: 0.5rem;">{title}</h1>
      </div>
    </div>
  </div>

  <main class="container" style="padding-top: 2rem;">
    <nav class="breadcrumb">
      <a href="/">Início</a><span class="breadcrumb-sep">/</span>
      <a href="/receitas/">Receitas</a><span class="breadcrumb-sep">/</span>
      <a href="/receitas/{cat_slug}/">{cat_name}</a><span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{title}</span>
    </nav>

    <div class="recipe-meta-bar">
      <div class="recipe-meta-item"><span>Preparo</span><strong>{prep_time}</strong></div>
      <div class="recipe-meta-divider"></div>
      <div class="recipe-meta-item"><span>Cozimento</span><strong>{cook_time}</strong></div>
      <div class="recipe-meta-divider"></div>
      <div class="recipe-meta-item"><span>Calorias</span><strong>{calories}</strong></div>
      <div class="recipe-meta-divider"></div>
      <div class="recipe-meta-item"><span>Avaliação</span><strong style="color: #F5A623;">⭐ {rating} ({rating_count})</strong></div>
      <div class="recipe-meta-actions">
        <button id="fav-btn" class="btn btn-ghost btn-sm">🤍 Salvar</button>
        <button onclick="window.printRecipe()" class="btn btn-ghost btn-sm">🖨️ Imprimir</button>
        <button id="start-cooking-mode" class="btn btn-primary btn-sm">🎯 Modo Cozinhando</button>
      </div>
    </div>

    <div class="recipe-layout">
      <div>
        
        <!-- Artigo Aprofundado Editorial (>1000 palavras) -->
        <article class="mb-4" style="line-height: 1.85; font-size: 1.05rem;">
          {article_html}
        </article>

        <!-- Barra de Progresso do Checklist -->
        <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 1rem 1.5rem; border-radius: var(--radius); margin-bottom: 2rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong id="recipe-progress-text">0 de {len(steps)} passos concluídos</strong>
            <button id="reset-checks" class="btn btn-ghost btn-sm" style="font-size: 0.75rem;">♻️ Limpar marcações</button>
          </div>
          <div style="width: 100%; height: 8px; background: var(--gray-2); border-radius: 4px; overflow: hidden;">
            <div id="recipe-progress" style="width: 0%; height: 100%; background: var(--green); transition: width 0.3s ease;"></div>
          </div>
        </div>

        <!-- Ingredientes com Porções Reativas -->
        <section id="ingredientes" class="mb-4">
          <div class="section-header">
            <div>
              <h2 class="section-title">🛒 Ingredientes Selecionados</h2>
              <p class="section-subtitle">Ajuste o rendimento para calcular as porções na medida certa</p>
            </div>
          </div>

          <div class="portions-control">
            <span class="portions-label">Rendimento:</span>
            <input type="range" id="portions-slider" min="1" max="16" step="1" value="{base_portions}" data-base="{base_portions}" class="portions-slider">
            <span id="portions-value" class="portions-value">{base_portions} porções</span>
          </div>

          <ul class="ingredient-list">
{ingredients_rendered}
          </ul>
        </section>

        <!-- Modo de Preparo Interativo com Timers -->
        <section id="preparo" class="mb-4">
          <div class="section-header">
            <div>
              <h2 class="section-title">👩‍🍳 Modo de Preparo Passo a Passo</h2>
              <p class="section-subtitle">Acompanhe com checklist e ative os timers diretamente na tela</p>
            </div>
          </div>

          <div class="step-list">
{steps_rendered}
          </div>
        </section>

        <!-- Tabela Nutricional -->
        <section id="nutricao" class="mb-4">
          <h3 class="mb-2">📊 Tabela Nutricional (Porção Individual)</h3>
          <table class="nutrition-table">
            <thead>
              <tr><th>Nutriente</th><th>Quantidade Média</th></tr>
            </thead>
            <tbody>
{nutrition_rows}
            </tbody>
          </table>
        </section>

        <!-- Seção de Posts Relacionados (Backlinks Visuais) -->
        <section class="mb-4">
          <div class="section-header">
            <div>
              <h2 class="section-title">Você Também Vai Amar</h2>
              <p class="section-subtitle">Receitas complementares testadas para o seu cardápio</p>
            </div>
          </div>
          <div class="grid-3">
{related_rendered}
          </div>
        </section>

        <!-- FAQ Accordion -->
        <section id="faq" class="mb-4">
          <h2 class="section-title mb-2">Dúvidas Frequentes da Receita (FAQ)</h2>
{faq_rendered}
        </section>

        <!-- Compartilhamento -->
        <section class="mb-4">
          <h4 class="mb-2">Gostou da receita? Compartilhe:</h4>
          <div class="share-buttons">
            <a href="https://api.whatsapp.com/send?text=Veja%20essa%20receita%20no%20Quero%20Rango:%20https://querorango.com/receitas/{cat_slug}/{slug}/" target="_blank" rel="noopener" class="share-btn share-whatsapp">📱 WhatsApp</a>
            <button onclick="window.copyToClipboard(window.location.href)" class="share-btn share-copy">🔗 Copiar Link</button>
            <button onclick="window.shareRecipe(document.title, window.location.href)" class="share-btn share-twitter">📤 Compartilhar</button>
          </div>
        </section>

        <!-- Comentários da Comunidade -->
        <section id="comentarios" class="mb-4">
          <h3 class="mb-2">Perguntas & Avaliações</h3>
          <div class="question-form mb-3">
            <form id="question-form">
              <div class="form-group">
                <label class="form-label" for="user-name">Seu Nome:</label>
                <input type="text" id="user-name" name="name" class="form-input" placeholder="Ex: Rosângela ou Wander" required>
              </div>
              <div class="form-group">
                <label class="form-label" for="user-message">Sua Dúvida ou Dica:</label>
                <textarea id="user-message" name="message" class="form-textarea" placeholder="Deixe seu comentário sobre a receita..." required></textarea>
              </div>
              <button type="submit" class="btn btn-primary">💬 Publicar Comentário</button>
            </form>
          </div>
        </section>

      </div>

      <aside class="recipe-sidebar">
        <div class="toc mb-3">
          <div class="toc-title">Índice da Receita</div>
          <a href="#artigo-completo">📖 Artigo & Guia do Chef</a>
          <a href="#ingredientes">🛒 Ingredientes com Check</a>
          <a href="#preparo">👩‍🍳 Modo de Preparo</a>
          <a href="#nutricao">📊 Tabela Nutricional</a>
          <a href="#faq">❓ Perguntas Frequentes</a>
          <a href="#comentarios">💬 Comunidade</a>
        </div>

        <div class="card p-3" style="padding: 1.25rem;">
          <h4 class="mb-2">Recomendados:</h4>
          <div style="display: flex; flex-direction: column; gap: 1rem;">
{sidebar_related_rendered}
          </div>
        </div>
      </aside>
    </div>
  </main>

  <div class="timer-modal" id="timer-modal">
    <div class="timer-box">
      <span style="font-size: 2.5rem;">⏰</span>
      <h3 id="timer-label">Timer Quero Rango</h3>
      <div class="timer-display" id="timer-display">00:00</div>
      <div class="timer-controls">
        <button id="timer-pause" class="btn btn-ghost btn-sm">⏸ Pausar</button>
        <button id="timer-close" class="btn btn-primary btn-sm">Fechar</button>
      </div>
    </div>
  </div>

  <div class="cooking-mode-overlay" id="cooking-mode">
    <button class="cooking-close" id="cooking-close">✕ Fechar</button>
    <div class="cooking-step-display">
      <div class="cooking-step-num" id="cooking-step-num">Passo 1</div>
      <div class="cooking-step-text" id="cooking-step-text">Modo Cozinhando</div>
      <div class="cooking-nav">
        <button id="cooking-prev" class="btn btn-ghost btn-lg">← Voltar</button>
        <button id="cooking-next" class="btn btn-primary btn-lg">Próximo →</button>
      </div>
    </div>
  </div>

  <footer class="site-footer">
    <div class="container text-center">
      <p>© 2026 Quero Rango (querorango.com) — Todos os direitos reservados. • Desenvolvido por Wander Santos</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
  <script src="/js/recipe.js"></script>
</body>
</html>
"""
    return html

def save_recipe(recipe, base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    cat_slug = recipe["category_slug"]
    slug = recipe["slug"]
    target_dir = os.path.join(base_dir, "receitas", cat_slug, slug)
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, "index.html")
    
    html_content = generate_recipe_html(recipe)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Contagem de palavras do artigo para verificação
    words = len(re.findall(r'\b\w+\b', recipe["article_html"]))
    print(f"[OK] Criada: {cat_slug}/{slug} | Palavras no artigo: {words}")
    return file_path, words
