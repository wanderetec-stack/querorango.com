# -*- coding: utf-8 -*-
"""
Gerador de RSS Feed para querorango.com
Roda automaticamente pelo hourly_scheduler.py apos cada publicacao.
"""
import os, sys, json, glob, re
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RSS_FILE = os.path.join(BASE_DIR, "feed.rss")
SITE_URL = "https://querorango.com"

def slugify_title(html_file):
    """Extrai titulo e imagem do index.html de uma receita."""
    try:
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        title_m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        title = title_m.group(1).strip() if title_m else "Receita"
        og_title = re.search(r'<meta property="og:title" content="([^"]+)"', content)
        if og_title:
            title = og_title.group(1).replace(" | Quero Rango", "").strip()
        img_m = re.search(r'<meta property="og:image" content="([^"]+)"', content)
        image = img_m.group(1) if img_m else ""
        desc_m = re.search(r'<meta name="description" content="([^"]+)"', content)
        description = desc_m.group(1) if desc_m else "Receita deliciosa do Quero Rango."
        return title, image, description
    except Exception:
        return "Receita", "", "Receita deliciosa do Quero Rango."

def build_rss():
    # Coletar todas as receitas publicadas
    items = []
    recipe_dirs = glob.glob(os.path.join(BASE_DIR, "receitas", "*", "*", "index.html"))
    
    for html_file in sorted(recipe_dirs, key=os.path.getmtime, reverse=True):
        parts = html_file.replace(BASE_DIR, "").replace("\\", "/").strip("/").split("/")
        if len(parts) < 4:
            continue
        # parts = [receitas, cat_slug, rec_slug, index.html]
        cat_slug = parts[1]
        rec_slug = parts[2]
        url = f"{SITE_URL}/receitas/{cat_slug}/{rec_slug}/"
        
        mtime = os.path.getmtime(html_file)
        pub_date = datetime.fromtimestamp(mtime, tz=timezone(timedelta(hours=-3)))
        pub_date_rfc = format_datetime(pub_date)
        
        title, image, description = slugify_title(html_file)
        
        # Limpar caracteres especiais para XML
        def esc(s):
            return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        
        item_xml = f"""    <item>
      <title>{esc(title)}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <description>{esc(description)}</description>
      <pubDate>{pub_date_rfc}</pubDate>
      <enclosure url="{esc(image)}" type="image/jpeg" length="0"/>
    </item>"""
        items.append(item_xml)
        
        if len(items) >= 50:  # RSS com ultimas 50 receitas
            break
    
    now_rfc = format_datetime(datetime.now(tz=timezone(timedelta(hours=-3))))
    
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Quero Rango - Receitas Brasileiras</title>
    <link>{SITE_URL}</link>
    <description>Receitas deliciosas para todo dia. Almoço, jantar, sobremesas, marmitas e muito mais!</description>
    <language>pt-BR</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.rss" rel="self" type="application/rss+xml"/>
    <image>
      <url>{SITE_URL}/assets/logo.png</url>
      <title>Quero Rango</title>
      <link>{SITE_URL}</link>
    </image>
{chr(10).join(items)}
  </channel>
</rss>"""
    
    with open(RSS_FILE, "w", encoding="utf-8") as f:
        f.write(rss)
    
    print(f"[RSS] feed.rss gerado com {len(items)} receitas em {RSS_FILE}")
    return len(items)

if __name__ == "__main__":
    build_rss()