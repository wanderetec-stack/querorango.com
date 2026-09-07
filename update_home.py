# -*- coding: utf-8 -*-
"""
Atualiza a Homepage (index.html) do querorango.com para exibir:
- As 20 Categorias em Alta de 2026 com fotos reais
- Seções temáticas: Air Fryer, Rápidas, Marmitas, Bolos, Almoço de Domingo
- Últimas receitas adicionadas com links diretos e fotos apetitosas
"""

import os

# As 21 Categorias mais buscadas de 2026 com imagens reais e apetitosas
ALL_20_CATEGORIES = [
    {"slug": "air-fryer", "name": "Air Fryer", "desc": "Crocante sem óleo", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=240&auto=format&fit=crop&q=80"},
    {"slug": "almoco", "name": "Almoço & Jantar", "desc": "Refeições completas", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=240&auto=format&fit=crop&q=80"},
    {"slug": "rapidas", "name": "Rápidas (15 min)", "desc": "Sem complicação", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=240&auto=format&fit=crop&q=80"},
    {"slug": "marmitas", "name": "Marmitas & Meal Prep", "desc": "Economia semanal", "img": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=240&auto=format&fit=crop&q=80"},
    {"slug": "saudavel", "name": "Saudável & Fit", "desc": "Proteína e energia", "img": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=240&auto=format&fit=crop&q=80"},
    {"slug": "economicas", "name": "Econômicas", "desc": "Fim de mês esperto", "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=240&auto=format&fit=crop&q=80"},
    {"slug": "bolos", "name": "Bolos Caseiros", "desc": "Fofinhos de vó", "img": "/assets/recipes/bolo-cenoura.jpg"},
    {"slug": "sobremesas", "name": "Sobremesas", "desc": "Doces e caldas", "img": "/assets/recipes/pudim.jpg"},
    {"slug": "paes", "name": "Pães & Massas", "desc": "Cheirinho de padaria", "img": "/assets/recipes/pao-frances.jpg"},
    {"slug": "virais", "name": "Doces Virais", "desc": "Tendências da internet", "img": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=240&auto=format&fit=crop&q=80"},
    {"slug": "frango", "name": "Frango & Aves", "desc": "Suculência diária", "img": "/assets/recipes/frango-passarinho.jpg"},
    {"slug": "massas", "name": "Massas & Lasanhas", "desc": "Conforto italiano", "img": "/assets/recipes/lasanha.jpg"},
    {"slug": "carne-moida", "name": "Carne Moída", "desc": "Prática e versátil", "img": "/assets/recipes/almondegas.jpg"},
    {"slug": "pressao", "name": "Panela de Pressão", "desc": "Rápido na pressão", "img": "/assets/recipes/costela.jpg"},
    {"slug": "peixes", "name": "Peixes & Frutos do Mar", "desc": "Leves e frescos", "img": "/assets/recipes/peixe-grelhado.jpg"},
    {"slug": "regional", "name": "Culinária Regional", "desc": "Tradição do Brasil", "img": "/assets/recipes/baiao-de-dois.jpg"},
    {"slug": "lanches", "name": "Lanches & Petiscos", "desc": "Boteco em casa", "img": "/assets/recipes/coxinha.jpg"},
    {"slug": "sopas", "name": "Sopas & Caldos", "desc": "Aquece a alma", "img": "/assets/recipes/caldo-verde.jpg"},
    {"slug": "sem-gluten", "name": "Sem Glúten", "desc": "Inclusivo e fofo", "img": "/assets/recipes/pao-integral.jpg"},
    {"slug": "vegetarianas", "name": "Vegetarianas", "desc": "Sabor à base vegetal", "img": "/assets/recipes/falafel.jpg"},
    {"slug": "cafe-da-manha", "name": "Café & Brunch", "desc": "Comece bem o dia", "img": "/assets/recipes/panqueca-americana.jpg"}
]

# Prateleiras de Destaque
SECTION_AIRFRYER = [
    {"title": "Frango Crocante na Air Fryer com Casquinha Dourada", "url": "/receitas/air-fryer/frango-crocante-air-fryer/", "img": "/assets/recipes/frango-passarinho.jpg", "time": "25 min", "cal": "285 kcal", "desc": "O método de secagem e duas temperaturas que deixa a pele estaladiça e a carne suculenta."},
    {"title": "Batata Frita Perfeita na Air Fryer Sequinha", "url": "/receitas/air-fryer/batata-frita-air-fryer/", "img": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500&q=80", "time": "20 min", "cal": "190 kcal", "desc": "Sem murchar e sem encharcar: o choque térmico que garante o ponto de lanchonete."},
    {"title": "Pudim de Leite Condensado na Air Fryer Lisinho", "url": "/receitas/air-fryer/pudim-air-fryer/", "img": "/assets/recipes/pudim.jpg", "time": "30 min", "cal": "290 kcal", "desc": "Aveludado, sem furinhos e assado na metade do tempo do forno convencional com calda de caramelo."},
    {"title": "Bolo de Chocolate Fofinho na Air Fryer", "url": "/receitas/air-fryer/bolo-de-chocolate-air-fryer/", "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&q=80", "time": "25 min", "cal": "310 kcal", "desc": "Massa molhadinha com cobertura brilhante pronta em minutos para o café."}
]

SECTION_RAPIDAS = [
    {"title": "Macarrão Cremoso de Uma Panela Só", "url": "/receitas/rapidas/macarrao-uma-panela-so/", "img": "/assets/recipes/mac-and-cheese.jpg", "time": "15 min", "cal": "340 kcal", "desc": "Tudo na mesma panela: sem sujar louça e com molho encorpado e aveludado."},
    {"title": "Omelete de Hotel Super Fofinha com Queijo", "url": "/receitas/rapidas/omelete-recheada-hotel/", "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500&q=80", "time": "8 min", "cal": "220 kcal", "desc": "O segredo da manteiga em cubos gelada para criar dobras macias e cremosas."},
    {"title": "Bruschetta Italiana Tradicional de Pão Tostado", "url": "/receitas/rapidas/bruschetta-de-tomate-italiana/", "img": "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=500&q=80", "time": "10 min", "cal": "160 kcal", "desc": "Tomates maduros marinados no azeite, alho e folhas frescas de manjericão."},
    {"title": "Filé de Frango Grelhado Suculento no Limão", "url": "/receitas/rapidas/file-de-peito-limao/", "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500&q=80", "time": "12 min", "cal": "240 kcal", "desc": "Nunca mais coma frango seco: a técnica da marinada rápida de limão e azeite."}
]

SECTION_BOLOS = [
    {"title": "Bolo de Cenoura Fofinho com Calda Craquelada", "url": "/receitas/bolos/bolo-de-cenoura/", "img": "/assets/recipes/bolo-cenoura.jpg", "time": "60 min", "cal": "320 kcal", "desc": "Massa batida no liquidificador e cobertura de chocolate crocante que quebra na mordida."},
    {"title": "Bolo de Fubá Cremoso com Goiabada Cascão", "url": "/receitas/bolos/bolo-de-fuba-com-goiabada/", "img": "/assets/recipes/bolo-fuba.jpg", "time": "40 min", "cal": "295 kcal", "desc": "O truque para os cubos de goiabada não irem todos para o fundo da fôrma."},
    {"title": "Bolo de Milho de Liquidificador Cremoso", "url": "/receitas/bolos/bolo-de-milho-de-lata-cremoso/", "img": "/assets/recipes/bolo-milho.jpg", "time": "45 min", "cal": "310 kcal", "desc": "Textura parecida com pamonha de feira, usando milho de lata e leite condensado."},
    {"title": "Bolo de Laranja Molhadinho que Desmancha", "url": "/receitas/bolos/bolo-de-laranja-molhadinho/", "img": "/assets/recipes/bolo-laranja.jpg", "time": "40 min", "cal": "270 kcal", "desc": "Feito com o suco fresco da fruta e regado ainda quente com calda perfumada."}
]

SECTION_MARMITAS = [
    {"title": "Frango Desfiado Temperado para a Semana", "url": "/receitas/marmitas/frango-desfiado-congelar/", "img": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=500&q=80", "time": "30 min", "cal": "260 kcal", "desc": "Super suculento com refogado de páprica e cebola, perfeito para porcionar e congelar."},
    {"title": "Carne Moída com Cenoura e Vagem", "url": "/receitas/marmitas/carne-moida-com-legumes-marmita/", "img": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=500&q=80", "time": "25 min", "cal": "290 kcal", "desc": "Técnica que não solta água ao descongelar, mantendo os legumes al dente e crocantes."},
    {"title": "Purê de Batata-Doce Cremoso com Gengibre", "url": "/receitas/marmitas/pure-de-batata-doce-congelavel/", "img": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=500&q=80", "time": "20 min", "cal": "180 kcal", "desc": "Acompanhamento leve e aromático que descongela com textura macia de restaurante."},
    {"title": "Arroz Integral Soltinho que Não Empapa", "url": "/receitas/marmitas/arroz-integral-soltinho-marmita/", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&q=80", "time": "35 min", "cal": "210 kcal", "desc": "O ponto exato de água e refogado no azeite com alho dourado para durar 5 dias fresco."}
]

SECTION_SOBREMESAS = [
    {"title": "Brigadeiro de Colher Aveludado de Panela", "url": "/receitas/sobremesas/brigadeiro-de-colher/", "img": "/assets/recipes/brigadeiro.jpg", "time": "20 min", "cal": "290 kcal", "desc": "Ponto de colher brilhante e sedoso com cacau nobre e toque de flor de sal."},
    {"title": "Pudim de Leite Condensado Sem Furinhos", "url": "/receitas/sobremesas/pudim-de-leite-sem-furinho/", "img": "/assets/recipes/pudim.jpg", "time": "60 min", "cal": "320 kcal", "desc": "Receita tradicional de vó com calda dourada espelhada que desliza na travessa."},
    {"title": "Mousse de Maracujá com 3 Ingredientes", "url": "/receitas/sobremesas/mousse-de-maracuja-3-ingredientes/", "img": "/assets/recipes/quindim.jpg", "time": "10 min", "cal": "240 kcal", "desc": "Sem gelatina e sem fogo: batido no liquidificador até ficar firme e aveludado."},
    {"title": "Pavê de Chocolate Clássico de Domingo", "url": "/receitas/sobremesas/pave-de-chocolate-tradicional/", "img": "/assets/recipes/pave.jpg", "time": "25 min", "cal": "310 kcal", "desc": "Camadas generosas de creme aveludado, biscoito umedecido e raspas de chocolate."}
]

def render_cards(items, tag_name="Receita", tag_class="tag-primary"):
    cards = []
    for item in items:
        cards.append(f"""      <article class="card">
        <a href="{item['url']}">
          <img class="card-img" src="{item['img']}" alt="{item['title']}" loading="lazy" width="400" height="300">
        </a>
        <div class="card-body">
          <div class="card-meta">
            <span class="tag {tag_class}">{tag_name}</span>
            <span>⏱ {item['time']}</span>
            <span>🔥 {item['cal']}</span>
          </div>
          <h3 class="card-title">
            <a href="{item['url']}">{item['title']}</a>
          </h3>
          <p class="card-desc">{item['desc']}</p>
          <div class="stars-meta">
            <span class="stars">⭐⭐⭐⭐⭐</span>
            <span>4.9 (320+)</span>
          </div>
        </div>
      </article>""")
    return "\n\n".join(cards)

def build_home():
    categories_html = []
    for cat in ALL_20_CATEGORIES:
        categories_html.append(f"""      <a href="/receitas/{cat['slug']}/" class="category-card">
        <img class="category-thumb" src="{cat['img']}" alt="{cat['name']}" width="88" height="88" loading="lazy">
        <div class="category-name">{cat['name']}</div>
        <div class="category-count">{cat['desc']}</div>
      </a>""")
    categories_rendered = "\n".join(categories_html)

    cards_airfryer = render_cards(SECTION_AIRFRYER, "Air Fryer", "tag-primary")
    cards_rapidas = render_cards(SECTION_RAPIDAS, "Rápida", "tag-green")
    cards_bolos = render_cards(SECTION_BOLOS, "Bolos", "tag-primary")
    cards_marmitas = render_cards(SECTION_MARMITAS, "Marmita", "tag-green")
    cards_sobremesas = render_cards(SECTION_SOBREMESAS, "Sobremesa", "tag-primary")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Quero Rango 🍊 | O Livro de Receitas Digital Mais Completo de 2026</title>
  <meta name="description" content="Descubra mais de 200 receitas testadas com artigos profundos, checklists de preparo, timers integrados, modo cozinhando e busca por ingredientes.">
  
  <meta property="og:title" content="Quero Rango 🍊 | Receitas Fáceis e Passo a Passo Interativo">
  <meta property="og:description" content="Seu livro de receitas digital interativo com porções ajustáveis, timers e modo sem apagar a tela!">
  <meta property="og:image" content="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&q=80">
  <meta property="og:url" content="https://querorango.com/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <link rel="canonical" href="https://querorango.com/">

  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#FF6B35">

  <link rel="stylesheet" href="/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Quero Rango",
    "url": "https://querorango.com/",
    "potentialAction": {{
      "@type": "SearchAction",
      "target": {{
        "@type": "EntryPoint",
        "urlTemplate": "https://querorango.com/busca/?q={{search_term_string}}"
      }},
      "query-input": "required name=search_term_string"
    }}
  }}
  </script>
</head>
<body>

  <header class="site-header">
    <div class="scroll-progress"></div>
    <nav class="nav container">
      <a href="/" class="nav-logo">
        <span class="nav-logo-icon">🍊</span>
        Quero Rango
      </a>
      <div class="nav-links">
        <a href="/receitas/" class="nav-link">Todas as Receitas</a>
        <a href="/receitas/air-fryer/" class="nav-link">Air Fryer</a>
        <a href="/receitas/rapidas/" class="nav-link">Rápidas</a>
        <a href="/receitas/marmitas/" class="nav-link">Marmitas</a>
        <a href="/receitas/bolos/" class="nav-link">Bolos</a>
        <a href="/receitas/sobremesas/" class="nav-link">Sobremesas</a>
        <a href="/busca/" class="nav-link">Na Geladeira</a>
      </div>
      <div class="nav-actions">
        <a href="/favoritos/" class="btn-icon" title="Receitas Salvas" aria-label="Favoritos">Salvos</a>
        <button class="btn-icon notif-toggle-btn" onclick="window.toggleNotifications()" title="Ativar Notificações" aria-label="Notificações">🔔</button>
        <button class="btn-icon" id="theme-toggle" title="Alternar tema" aria-label="Modo escuro">Tema</button>
        <button class="nav-hamburger" aria-label="Menu" aria-expanded="false">☰</button>
      </div>
    </nav>
    <nav class="mobile-menu" aria-label="Menu mobile">
      <a href="/receitas/" class="nav-link">Todas as Receitas (200+)</a>
      <a href="/receitas/air-fryer/" class="nav-link">Air Fryer (Sem Óleo)</a>
      <a href="/receitas/rapidas/" class="nav-link">Rápidas (15 min)</a>
      <a href="/receitas/marmitas/" class="nav-link">Marmitas & Meal Prep</a>
      <a href="/receitas/bolos/" class="nav-link">Bolos Caseiros</a>
      <a href="/receitas/sobremesas/" class="nav-link">Doces & Sobremesas</a>
      <a href="/receitas/regional/" class="nav-link">Cozinha Regional</a>
      <a href="/busca/" class="nav-link">O que tem na geladeira?</a>
      <a href="/favoritos/" class="nav-link">Receitas Salvas</a>
      <a href="/sobre/" class="nav-link">Sobre o Quero Rango</a>
    </nav>
  </header>

  <section class="hero">
    <div class="container hero-content">
      <span class="hero-eyebrow">Livro de Receitas Digital • Mais de 200 Receitas Testadas</span>
      <h1>O que você quer <span>cozinhar hoje?</span></h1>
      <p class="hero-desc">Descubra receitas fáceis com artigos detalhados, checklist de passos, timers integrados na panela e modo tela cheia para cozinhar sem sujar o celular.</p>
      
      <form action="/busca/" method="GET" class="search-bar">
        <input type="text" name="q" class="search-input" placeholder="Digite um ingrediente ou receita (ex: frango, cenoura, air fryer, chocolate)..." required>
        <button type="submit" class="search-btn">
          <span>Buscar Receita</span>
        </button>
      </form>

      <div class="stats-row mt-3">
        <div class="stat-item" style="color: rgba(255,255,255,0.9);">
          <strong>20 Categorias em Alta</strong>
        </div>
        <div class="stat-item" style="color: rgba(255,255,255,0.9);">
          <strong>Checklist Passo a Passo</strong> (com timers)
        </div>
        <div class="stat-item" style="color: rgba(255,255,255,0.9);">
          <strong>Instalável no Celular</strong> (PWA Offline)
        </div>
        <div class="stat-item" style="color: rgba(255,255,255,0.9);">
          <strong>Artigos com mais de 1.000 Palavras</strong>
        </div>
      </div>
    </div>
  </section>

  <main class="container section">
    
    <!-- As 20 Categorias com Fotos Reais Gastronômicas -->
    <div class="section-header">
      <div>
        <h2 class="section-title">Explore as 20 Categorias em Alta</h2>
        <p class="section-subtitle">Escolha o tipo de preparo ou o momento perfeito do seu dia</p>
      </div>
      <a href="/receitas/" class="section-link">Ver catálogo completo →</a>
    </div>

    <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem;">
{categories_rendered}
    </div>

    <!-- Destaque Semanal -->
    <div class="section-header mt-4">
      <div>
        <span class="tag tag-primary">Destaque da Semana</span>
        <h2 class="section-title mt-1">A Receita Favorita da Comunidade</h2>
      </div>
    </div>

    <div class="recipe-feature">
      <img src="https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80" 
           alt="Bolo de Cenoura Fofinho com Calda Craquelada Quero Rango" 
           class="recipe-feature-img" loading="lazy" width="600" height="450">
      <div class="recipe-feature-body">
        <div class="card-meta">
          <span class="tag tag-primary">Bolos</span>
          <span>⏱ 60 min</span>
          <span>👥 8 porções</span>
          <span>🔥 320 kcal</span>
        </div>
        <h2>Bolo de Cenoura com Calda Craqueluda de Chocolate</h2>
        <p class="card-desc" style="-webkit-line-clamp: 3;">
          Massa ultra fofinha, molhadinha e batida no liquidificador em 3 minutos, coberta com aquela casquinha crocante que quebra na mordida. Experimente no nosso modo interativo com timer de forno!
        </p>
        <div class="stars-meta">
          <span class="stars">⭐⭐⭐⭐⭐</span>
          <strong>4.9 / 5.0</strong>
          <span class="text-muted">(238 avaliações no Google)</span>
        </div>
        <div class="flex gap-1 mt-2 flex-wrap">
          <a href="/receitas/bolos/bolo-de-cenoura/" class="btn btn-primary">
            Abrir Livro de Receita
          </a>
          <a href="/receitas/bolos/" class="btn btn-ghost">
            Mais Bolos
          </a>
        </div>
      </div>
    </div>

    <!-- Prateleira 1: Em Alta na Air Fryer -->
    <div class="section-header mt-4">
      <div>
        <span class="tag tag-primary">Megatendência 2026</span>
        <h2 class="section-title mt-1">Bombando na Air Fryer</h2>
        <p class="section-subtitle">Economia de energia, crocância sem óleo e zero bagunça na pia</p>
      </div>
      <a href="/receitas/air-fryer/" class="section-link">Ver todas na Air Fryer →</a>
    </div>

    <div class="grid-4">
{cards_airfryer}
    </div>

    <!-- Prateleira 2: Sem Tempo? Rápidas em 15 Minutos -->
    <div class="section-header mt-4">
      <div>
        <span class="tag tag-green">Para Quem Tem Pressa</span>
        <h2 class="section-title mt-1">Prontas em 15 a 20 Minutos</h2>
        <p class="section-subtitle">Refeições completas, deliciosas e sem sujeira para os dias corridos</p>
      </div>
      <a href="/receitas/rapidas/" class="section-link">Ver receitas rápidas →</a>
    </div>

    <div class="grid-4">
{cards_rapidas}
    </div>

    <!-- Prateleira 3: Café da Tarde & Bolos Fofinhos -->
    <div class="section-header mt-4">
      <div>
        <span class="tag tag-primary">Café da Tarde</span>
        <h2 class="section-title mt-1">Bolos Caseiros que Não Solam</h2>
        <p class="section-subtitle">Receitas afetivas com o aroma de casa de vó</p>
      </div>
      <a href="/receitas/bolos/" class="section-link">Ver todos os bolos →</a>
    </div>

    <div class="grid-4">
{cards_bolos}
    </div>

    <!-- Prateleira 4: Marmitas & Meal Prep para a Semana -->
    <div class="section-header mt-4">
      <div>
        <span class="tag tag-green">Planejamento & Economia</span>
        <h2 class="section-title mt-1">Marmitas & Meal Prep da Semana</h2>
        <p class="section-subtitle">Comida fresca, congelável e super nutritiva para economizar tempo</p>
      </div>
      <a href="/receitas/marmitas/" class="section-link">Ver todas as marmitas →</a>
    </div>

    <div class="grid-4">
{cards_marmitas}
    </div>

    <!-- Prateleira 5: Sobremesas & Doces Irresistíveis -->
    <div class="section-header mt-4">
      <div>
        <span class="tag tag-primary">Para Adoçar o Dia</span>
        <h2 class="section-title mt-1">Doces & Sobremesas Favoritas</h2>
        <p class="section-subtitle">Pudins lisinhos, mousses cremosos e doces que derretem na boca</p>
      </div>
      <a href="/receitas/sobremesas/" class="section-link">Ver todas as sobremesas →</a>
    </div>

    <div class="grid-4">
{cards_sobremesas}
    </div>

    <!-- PWA Callout -->
    <div style="background: linear-gradient(135deg, var(--dark) 0%, var(--dark-2) 100%); color: #fff; border-radius: var(--radius-lg); padding: 3rem 2rem; margin-top: 4rem; display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center;" class="card">
      <div>
        <span class="tag tag-primary">App Gratuito PWA</span>
        <h2 style="color: #fff; margin-top: 0.75rem;">Leve o Quero Rango para a sua bancada de cozinha</h2>
        <p style="color: rgba(255,255,255,0.8); max-width: 600px; margin-top: 0.5rem;">
          Instale diretamente no seu celular sem baixar na Play Store. As receitas salvas funcionam até sem internet e o modo cozinhando não deixa a tela apagar!
        </p>
      </div>
      <div>
        <button onclick="document.getElementById('pwa-install-btn')?.click() || alert('Clique no ícone de compartilhar do seu navegador e selecione \'Adicionar à tela de início\'')" class="btn btn-primary btn-lg">
          Instalar no Celular
        </button>
      </div>
    </div>

  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-logo">🍊 Quero Rango</div>
          <p class="footer-desc">Seu livro de receitas digital interativo com mais de 200 receitas testadas, timers integrados e artigos detalhados para o seu dia a dia.</p>
        </div>
        <div>
          <div class="footer-title">Top Categorias</div>
          <div class="footer-links">
            <a href="/receitas/air-fryer/" class="footer-link">Air Fryer</a>
            <a href="/receitas/rapidas/" class="footer-link">Rápidas (15 min)</a>
            <a href="/receitas/marmitas/" class="footer-link">Marmitas & Meal Prep</a>
            <a href="/receitas/bolos/" class="footer-link">Bolos Caseiros</a>
            <a href="/receitas/sobremesas/" class="footer-link">Doces & Sobremesas</a>
          </div>
        </div>
        <div>
          <div class="footer-title">Ferramentas</div>
          <div class="footer-links">
            <a href="/busca/" class="footer-link">Buscar por Ingrediente</a>
            <a href="/favoritos/" class="footer-link">Receitas Salvas</a>
            <button onclick="window.toggleNotifications()" class="footer-link" style="text-align: left; background: none; border: none; cursor: pointer; padding: 0;">Receber Notificações</button>
          </div>
        </div>
        <div>
          <div class="footer-title">Institucional</div>
          <div class="footer-links">
            <a href="/sobre/" class="footer-link">Sobre Nós (E-E-A-T)</a>
            <a href="/contato/" class="footer-link">Fale Conosco</a>
            <a href="/politica-de-privacidade/" class="footer-link">Política de Privacidade (LGPD)</a>
            <a href="/termos-de-uso/" class="footer-link">Termos de Uso</a>
            <button onclick="window.openCookiePreferences()" class="footer-link" style="text-align: left; background: none; border: none; cursor: pointer; padding: 0;">Preferências de Cookies</button>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Quero Rango (querorango.com) — Todos os direitos reservados.</span>
        <div>
          <a href="/politica-de-privacidade/" style="color: rgba(255,255,255,0.6); margin-right: 1rem; font-size: 0.8rem;">Privacidade</a>
          <a href="/termos-de-uso/" style="color: rgba(255,255,255,0.6); margin-right: 1rem; font-size: 0.8rem;">Termos</a>
          <a href="/contato/" style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Contato</a>
        </div>
      </div>
    </div>
  </footer>

  <div class="pwa-banner" id="pwa-banner" role="alert">
    <div class="pwa-banner-icon">🍊</div>
    <div class="pwa-banner-text">
      <div class="pwa-banner-title">Instalar Quero Rango</div>
      <div class="pwa-banner-desc">Adicione à tela inicial para usar offline na cozinha!</div>
    </div>
    <button class="btn btn-primary btn-sm" id="pwa-install-btn">Instalar</button>
    <button class="pwa-banner-close" id="pwa-banner-close" aria-label="Fechar">✕</button>
  </div>

  <script src="/js/main.js"></script>
</body>
</html>
"""
    with open(r"c:\Users\Wander - Rosangela\Desktop\site de receitas\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] Homepage atualizada com as 20 categorias e prateleiras temáticas de receitas!")

if __name__ == "__main__":
    build_home()
