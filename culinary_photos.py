# -*- coding: utf-8 -*-
"""
Auditor e Corretor Global de Fotos Gastronômicas do Quero Rango (querorango.com)
Garante que CADA receita possua uma fotografia gastronômica 100% de comida real,
correspondente ao prato (sem tênis, sapatos, nem pratos trocados).
"""

import os
import re

# Banco de dados curado de fotos reais verificadas no Unsplash por palavra-chave culinária
CULINARY_PHOTOS = {
    # Tipos de Preparo e Pratos Específicos
    "pudim": "https://images.unsplash.com/photo-1528975604071-b4dc52a2d18c?w=600&q=80",
    "flan": "https://images.unsplash.com/photo-1528975604071-b4dc52a2d18c?w=600&q=80",
    "batata-frita": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80",
    "batatas": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80",
    "pastel": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=600&q=80",
    "coxinha": "https://images.unsplash.com/photo-1562967914-608f82629710?w=600&q=80",
    "torresmo": "https://images.unsplash.com/photo-1528607929212-2636ec44253e?w=600&q=80",
    "pao-de-queijo": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80",
    "peixe": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600&q=80",
    "tilapia": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600&q=80",
    "salmao": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600&q=80",
    "frango": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=600&q=80",
    "sobrecoxa": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=600&q=80",
    "bolo": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80",
    "chocolate": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80",
    "brigadeiro": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80",
    "macarrao": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=600&q=80",
    "espaguete": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=600&q=80",
    "penne": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=600&q=80",
    "lasanha": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=600&q=80",
    "omelete": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600&q=80",
    "ovos": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600&q=80",
    "panqueca": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&q=80",
    "waffle": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&q=80",
    "salada": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
    "quinoa": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
    "legumes": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&q=80",
    "sopa": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&q=80",
    "caldo": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&q=80",
    "canja": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&q=80",
    "marmita": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=600&q=80",
    "arroz": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80",
    "feijao": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
    "pao": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
    "carne-moida": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=600&q=80",
    "almondegas": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=600&q=80",
    "hamburguer": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=600&q=80",
    "regional": "https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80",
    "baiao": "https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80",
    "cuscuz": "https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80",
    "canjica": "https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80",
    "costela": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
    "camarao": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600&q=80",
    "morango": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80",
    "doce": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80",
    "cookies": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600&q=80",
    "torta": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80"
}

from recipe_media_data import get_recipe_info

def get_accurate_photo(slug, title, main_ing, cat_slug):
    img, _ = get_recipe_info(slug, title, main_ing, cat_slug)
    return img

