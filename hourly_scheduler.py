# -*- coding: utf-8 -*-
import os, sys, json, re, time, traceback, logging, urllib.request, urllib.parse, subprocess, requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Auto-carregar .env se existir localmente
try:
    dotenv_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip()
except Exception:
    pass

from build_catalog import build_article_text
from generator import save_recipe

QUEUE_FILE     = os.path.join(BASE_DIR, "recipe_queue.json")
PROGRESS_FILE  = os.path.join(BASE_DIR, "schedule_progress.json")
SITEMAP_FILE   = os.path.join(BASE_DIR, "sitemap.xml")
LOG_FILE       = os.path.join(BASE_DIR, "scheduler.log")
FB_CONFIG_FILE = os.path.join(BASE_DIR, "fb_config.json")
RSS_SCRIPT     = os.path.join(BASE_DIR, "generate_rss.py")
RECIPES_PER_HOUR = 2
GOAL = 2000

# Handler seguro para evitar conflito de lock no Windows
handlers = [logging.StreamHandler(sys.stdout)]
try:
    # Usar delay=True para nao travar o arquivo
    handlers.append(logging.FileHandler(LOG_FILE, encoding="utf-8", delay=True))
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("querorango")

# ── Cloudflare Pages Deploy ───────────────────────────────────────────────────
def deploy_to_cloudflare():
    try:
        env = os.environ.copy()
        env["CLOUDFLARE_API_TOKEN"] = os.environ.get("CLOUDFLARE_API_TOKEN", "")
        cmd = ["npx.cmd" if os.name == "nt" else "npx", "wrangler", "pages", "deploy", ".", "--project-name=querorango", "--branch=main", "--commit-dirty=true"]
        res = subprocess.run(cmd, cwd=BASE_DIR, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
        if res.returncode == 0:
            log.info("[CLOUDFLARE] Deploy realizado com sucesso no Cloudflare Pages (querorango.com)!")
        else:
            log.warning("[CLOUDFLARE AVISO] Deploy: " + str(res.stderr[:200]))
    except Exception as e:
        log.error("[CLOUDFLARE ERRO] " + str(e))

# ── RSS ────────────────────────────────────────────────────────────────────────
def update_rss():
    try:
        import generate_rss
        n = generate_rss.build_rss()
        log.info("[RSS] feed.rss atualizado com " + str(n) + " receitas")
    except Exception as e:
        log.error("[RSS ERRO] " + str(e))

# ── Facebook via Buffer API ───────────────────────────────────────────────────
BUFFER_TOKEN = "_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2"
BUFFER_CHANNEL_ID = "6a9cb071065799be4698d386"

def post_to_facebook(title, url, image_url=None, cat_name=None):
    """Publica a receita diretamente na fanpage Comida Que Prende via Buffer API."""
    try:
        mutation = {
            "query": """
                mutation CreatePost($input: CreatePostInput!) {
                    createPost(input: $input) {
                        __typename
                        ... on PostActionSuccess {
                            post {
                                id
                                status
                            }
                        }
                        ... on RestProxyError {
                            message
                        }
                        ... on LimitReachedError {
                            message
                        }
                        ... on InvalidInputError {
                            message
                        }
                    }
                }
            """,
            "variables": {
                "input": {
                    "channelId": BUFFER_CHANNEL_ID,
                    "text": f"Receita nova no Quero Rango! {title}\n\nConfira o passo a passo completo no site:\n{url}\n\n#receitas #comida #gastronomia #querorango #comidacaseira",
                    "mode": "shareNow",
                    "schedulingType": "automatic",
                    "metadata": {
                        "facebook": {
                            "type": "post",
                            "linkAttachment": {
                                "url": url
                            }
                        }
                    }
                }
            }
        }
        headers = {
            "Authorization": f"Bearer {BUFFER_TOKEN}",
            "Content-Type": "application/json"
        }
        res = requests.post("https://api.buffer.com", json=mutation, headers=headers, timeout=25)
        data = res.json().get("data", {}).get("createPost", {})
        if data.get("__typename") == "PostActionSuccess":
            pid = data.get("post", {}).get("id")
            log.info(f"[FACEBOOK OK] Publicado com sucesso na Fanpage Comida Que Prende! ID: {pid}")
            return True
        else:
            log.warning(f"[FACEBOOK AVISO] Resposta Buffer: {data}")
            return False
    except Exception as e:
        log.error(f"[FACEBOOK ERRO] {e}")
        return False

# ── Fila e Progresso ───────────────────────────────────────────────────────────
def load_queue():
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"current_total": 210, "goal": GOAL, "hourly_batch_size": RECIPES_PER_HOUR, "published_batches": [], "last_run": None}

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_sitemap(new_urls):
    if not os.path.exists(SITEMAP_FILE):
        return
    try:
        with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        today = datetime.now().strftime("%Y-%m-%d")
        entries = []
        for url in new_urls:
            if url not in content:
                entries.append(
                    "  <url>\n    <loc>" + url + "</loc>\n    <lastmod>" + today + "</lastmod>\n"
                    + "    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
                )
        if entries:
            updated = content.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
            with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
                f.write(updated)
            log.info("[SITEMAP] +" + str(len(entries)) + " URLs adicionadas")
    except Exception as e:
        log.error("[SITEMAP ERRO] " + str(e))

CAT_NAMES = {
    "air-fryer": "Air Fryer", "almoco": "Almoco e Jantar",
    "rapidas": "Rapidas", "marmitas": "Marmitas e Meal Prep",
    "saudavel": "Saudavel e High Protein", "economicas": "Economicas",
    "bolos": "Bolos Caseiros", "sobremesas": "Doces e Sobremesas",
    "paes": "Paes Caseiros", "virais": "Doces Virais",
    "frango": "Frango e Aves", "massas": "Massas e Lasanhas",
    "carne-moida": "Carne Moida", "pressao": "Panela de Pressao",
    "peixes": "Peixes e Frutos do Mar", "regional": "Culinaria Regional",
    "lanches": "Lanches e Petiscos", "sopas": "Sopas e Caldos",
    "sem-gluten": "Sem Gluten", "vegetarianas": "Vegetarianas e Veganas",
    "cafe-da-manha": "Cafe da Manha"
}

def build_recipe_object(item):
    cat_slug  = item["category_slug"]
    title     = item["title"]
    slug      = item["slug"]
    main_ing  = item["main_ingredient"]
    sec_ing   = item["secondary_ingredient"]
    cook_t    = item["cook_time"]
    prep_t    = item["prep_time"]
    image_url = item["image_url"]
    cat_name  = CAT_NAMES.get(cat_slug, cat_slug.replace("-", " ").title())

    try:
        cook_mins = int(re.search(r'\d+', cook_t).group())
    except Exception:
        cook_mins = 25
    try:
        prep_mins = int(re.search(r'\d+', prep_t).group())
    except Exception:
        prep_mins = 10
    total_mins = cook_mins + prep_mins
    article_html = build_article_text(title, cat_name, main_ing, sec_ing)

    return {
        "category_slug": cat_slug, "title": title, "slug": slug,
        "meta_description": "Aprenda a fazer " + title + " com nossa receita testada. Passo a passo completo.",
        "prep_time": prep_t, "cook_time": cook_t,
        "total_time": str(total_mins) + " min",
        "prep_minutes": prep_mins, "cook_minutes": cook_mins, "total_minutes": total_mins,
        "base_portions": 4, "yield_portions": "4 porcoes",
        "calories": "310 kcal", "rating": "4.9", "rating_count": "280",
        "image_url": image_url,
        "ingredients": [
            {"amount": "500", "unit": "g",       "name": "de " + main_ing + " frescos"},
            {"amount": "2",   "unit": "colheres", "name": "de " + sec_ing},
            {"amount": "3",   "unit": "dentes",   "name": "de alho picados"},
            {"amount": "1",   "unit": "colher",   "name": "de azeite de oliva extravirgem"},
            {"amount": "1",   "unit": "pitada",   "name": "de sal e pimenta moida na hora"},
            {"amount": "2",   "unit": "ramos",    "name": "de cheiro-verde fresco"}
        ],
        "steps": [
            {"text": "Separe e higienize: " + main_ing + " e " + sec_ing + ".", "timer_minutes": 0},
            {"text": "Misture tudo com alho, azeite e sal. Marine 10 min.", "timer_minutes": 10, "timer_label": "Marinada"},
            {"text": "Cozinhe por " + str(cook_mins) + " minutos ate dourar.", "timer_minutes": cook_mins, "timer_label": "Cozimento"},
            {"text": "Descanse 3 min, finalize com cheiro-verde e sirva!", "timer_minutes": 3, "timer_label": "Descanso"}
        ],
        "faq": [
            {"q": "Posso substituir " + sec_ing + "?", "a": "Sim! Use ervas frescas ou manteiga aromatizada."},
            {"q": "Como saber o ponto?", "a": "Coloracao dourada e suco claro ao corte."},
            {"q": "Posso congelar?", "a": "Sim! Potes hermeticos por ate 90 dias."}
        ],
        "article_html": article_html
    }

# ── Publicacao Principal ───────────────────────────────────────────────────────
def publish_batch():
    prog = load_progress()
    current_total = prog.get("current_total", 210)

    if current_total >= GOAL:
        log.info("[META ATINGIDA] " + str(current_total) + "/" + str(GOAL))
        return 0, 0, []

    queue = load_queue()
    if not queue:
        log.warning("[FILA VAZIA] Sem receitas.")
        return 0, 0, []

    log.info("=" * 60)
    log.info("LOTE HORARIO | " + str(current_total) + "/" + str(GOAL) + " | Fila: " + str(len(queue)))
    log.info("=" * 60)

    published_urls  = []
    published_count = 0
    error_count     = 0
    to_publish      = queue[:RECIPES_PER_HOUR]
    remaining_queue = queue[RECIPES_PER_HOUR:]

    for item in to_publish:
        try:
            recipe_obj = build_recipe_object(item)
            path, word_count = save_recipe(recipe_obj)
            url = "https://querorango.com/receitas/" + item["category_slug"] + "/" + item["slug"] + "/"
            published_urls.append(url)
            published_count += 1
            log.info("[OK] " + item["category_slug"] + "/" + item["slug"] + " | " + str(word_count) + " palavras")
            # Postar no Facebook logo apos publicar
            post_to_facebook(item["title"], url, item["image_url"], item["category_slug"])
        except Exception as e:
            error_count += 1
            log.error("[ERRO] " + item.get("slug", "?") + ": " + str(e))
            log.error(traceback.format_exc())

    save_queue(remaining_queue)

    if published_urls:
        update_sitemap(published_urls)
        update_rss()
        deploy_to_cloudflare()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prog["current_total"] = current_total + published_count
    prog["last_run"] = now_str
    prog["published_batches"].append({
        "timestamp": now_str, "count": published_count,
        "errors": error_count, "new_total": prog["current_total"],
        "queue_remaining": len(remaining_queue), "urls": published_urls
    })
    save_progress(prog)
    log.info("[LOTE OK] +" + str(published_count) + " | Total: " + str(prog["current_total"]) + "/" + str(GOAL) + " | Fila: " + str(len(remaining_queue)))
    return published_count, error_count, published_urls

def show_status():
    prog  = load_progress()
    queue = load_queue() if os.path.exists(QUEUE_FILE) else []
    current = prog.get("current_total", 210)
    q_rem   = len(queue)
    hs      = q_rem // RECIPES_PER_HOUR
    print("\n" + "="*55)
    print("  QUERO RANGO - STATUS")
    print("="*55)
    print("  Publicadas  : " + str(current) + " / " + str(GOAL))
    print("  Faltam      : " + str(GOAL - current) + " receitas")
    print("  Na fila     : " + str(q_rem) + " receitas")
    print("  Ritmo       : " + str(RECIPES_PER_HOUR) + " receitas/hora")
    print("  Conclusao   : ~" + str(hs) + " horas (~" + str(hs // 24) + " dias)")
    print("  Ultimo lote : " + str(prog.get("last_run", "Nunca")))
    print("="*55 + "\n")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--run-once"
    if mode == "--status":
        show_status()
    elif mode == "--run-once":
        log.info("Modo: --run-once")
        publish_batch()
    elif mode == "--daemon":
        log.info("Modo: --daemon | 2 receitas a cada 60 min")
        while True:
            p = load_progress()
            if p.get("current_total", 0) >= GOAL:
                log.info("[DAEMON] Meta atingida.")
                break
            publish_batch()
            log.info("[DAEMON] Aguardando 60 min...")
            time.sleep(3600)
    else:
        print("Uso: python hourly_scheduler.py [--run-once | --daemon | --status]")
        sys.exit(1)