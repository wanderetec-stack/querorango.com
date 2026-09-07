# -*- coding: utf-8 -*-
"""
Aplica a foto gastronômica correta em TODAS as receitas e páginas de categoria
"""
import os
import re
from build_catalog import CATEGORIES_DATA
from culinary_photos import get_accurate_photo

def update_all_category_pages():
    for cat in CATEGORIES_DATA:
        cat_slug = cat["cat_slug"]
        cat_name = cat["cat_name"]
        cat_index = os.path.join("receitas", cat_slug, "index.html")
        
        if not os.path.exists(cat_index):
            continue
            
        with open(cat_index, "r", encoding="utf-8") as f:
            html = f.read()

        # Para cada receita da categoria, atualizar a imagem no card
        for rec in cat["recipes"]:
            rec_slug = rec[0]
            rec_title = rec[1]
            main_ing = rec[2]
            correct_photo = get_accurate_photo(rec_slug, rec_title, main_ing, cat_slug)
            
            # Encontrar o card desta receita
            card_pattern = re.compile(rf'(<article class="card">[\s\S]*?<a href="/receitas/{cat_slug}/{rec_slug}/">[\s\S]*?<img class="card-img" src=")([^"]+)("[\s\S]*?</article>)')
            
            def replace_img(match):
                return match.group(1) + correct_photo + match.group(3)
                
            html = card_pattern.sub(replace_img, html)

        with open(cat_index, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Categoria atualizada com fotos reais: {cat_slug}")

if __name__ == "__main__":
    update_all_category_pages()
