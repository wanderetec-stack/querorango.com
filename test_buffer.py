import urllib.request, json

TOKEN = '_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2'

# Consultar perfis conectados no Buffer
url = 'https://api.bufferapp.com/1/profiles.json?access_token=' + TOKEN
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    r = urllib.request.urlopen(req, timeout=10)
    profiles = json.loads(r.read())
    print('Status:', r.getcode())
    print('Perfis encontrados:', len(profiles))
    for p in profiles:
        print('ID:', p.get('id'), '| Servico:', p.get('service'), '| Nome:', p.get('formatted_username'))
except urllib.error.HTTPError as e:
    print('Erro HTTP:', e.code, e.read().decode('utf-8'))
except Exception as e:
    print('Erro:', e)
