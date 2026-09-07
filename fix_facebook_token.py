# -*- coding: utf-8 -*-
"""
fix_facebook_token.py
Roda uma vez para trocar o token de usuario pelo page token correto.
Execute: python fix_facebook_token.py SEU_TOKEN_AQUI
"""
import sys, json, os, urllib.request, urllib.parse

BASE_DIR = r"c:\Users\Wander - Rosangela\Desktop\site de receitas"
FB_CONFIG = os.path.join(BASE_DIR, "fb_config.json")
PAGE_ID = "1073554579173855"

def test_and_save_token(user_token):
    print("Testando token...")
    # Checar permissoes
    try:
        url = "https://graph.facebook.com/debug_token?input_token=" + user_token + "&access_token=" + user_token
        r = urllib.request.urlopen(url)
        d = json.loads(r.read()).get("data", {})
        scopes = d.get("scopes", [])
        print("Permissoes encontradas:", scopes)
        has_posts = "pages_manage_posts" in scopes
        has_read  = "pages_read_engagement" in scopes
        print("pages_manage_posts:", has_posts)
        print("pages_read_engagement:", has_read)
    except Exception as e:
        print("Erro ao verificar token:", e)
        return

    # Obter page token
    try:
        url2 = "https://graph.facebook.com/v20.0/me/accounts?fields=id,name,access_token&access_token=" + user_token
        r2 = urllib.request.urlopen(url2)
        data = json.loads(r2.read())
        page_tok = None
        for p in data.get("data", []):
            print("Pagina disponivel:", p["name"], "ID:", p["id"])
            if p["id"] == PAGE_ID:
                page_tok = p["access_token"]
                print(">> Comida que Prende encontrada!")
        if not page_tok:
            print("ERRO: Comida que Prende (ID " + PAGE_ID + ") nao encontrada nesse token.")
            print("Use um token da conta que administra essa pagina.")
            return
    except Exception as e:
        print("Erro ao buscar paginas:", e)
        return

    # Testar post
    print("\nTestando post na fanpage...")
    ep = "https://graph.facebook.com/v20.0/" + PAGE_ID + "/feed"
    payload = urllib.parse.urlencode({
        "message": "Teste de integracao automatica - Quero Rango esta configurado para publicar receitas aqui automaticamente!",
        "access_token": page_tok
    }).encode("utf-8")
    try:
        req = urllib.request.Request(ep, data=payload, method="POST")
        r3 = urllib.request.urlopen(req, timeout=20)
        resp = json.loads(r3.read())
        print("POST PUBLICADO! ID:", resp.get("id"))
        # Salvar config
        config = {"FACEBOOK_PAGE_ID": PAGE_ID, "FACEBOOK_PAGE_TOKEN": page_tok, "SITE_URL": "https://querorango.com"}
        with open(FB_CONFIG, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print("fb_config.json atualizado! Facebook pronto para publicacao automatica.")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print("Erro " + str(e.code) + ":", body[:300])
        if "pages_manage_posts" in body:
            print("\n*** O token nao tem pages_manage_posts. ***")
            print("Siga os passos abaixo:")
            print("1. Acesse: https://developers.facebook.com/tools/explorer")
            print("2. App da Meta: QueroRango Publisher")
            print("3. Usuario ou Pagina: Comida Que Prende")
            print("4. Clique 'Adicionar permissao' -> busque 'pages_manage_posts' -> marque")
            print("5. Clique 'Generate Access Token' -> autorize")
            print("6. Cole o token aqui: python fix_facebook_token.py SEU_TOKEN")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fix_facebook_token.py SEU_TOKEN_AQUI")
        sys.exit(1)
    test_and_save_token(sys.argv[1])