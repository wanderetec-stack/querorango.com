import os, sys, json, re, glob, unicodedata
from datetime import datetime

BASE_DIR = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'
sys.path.insert(0, BASE_DIR)

from generator import save_recipe
from build_catalog import build_article_text

print('Iniciando construcao do lote de 300 receitas de Comida de Boteco...')
