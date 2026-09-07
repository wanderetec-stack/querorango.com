import os, sys, json, re, glob, unicodedata, subprocess
from datetime import datetime

BASE_DIR = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'
sys.path.insert(0, BASE_DIR)

from generator import save_recipe
from build_catalog import build_article_text

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return re.sub(r'[-\s]+', '-', text)

print('Carregando dados das 300 receitas de boteco...')
