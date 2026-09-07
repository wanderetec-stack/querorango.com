import urllib.request, json

TOKEN = '_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2'
url = 'https://api.buffer.com'

query = {
    'query': '''
        query {
            account {
                id
                email
            }
        }
    '''
}

req = urllib.request.Request(
    url,
    data=json.dumps(query).encode('utf-8'),
    headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    },
    method='POST'
)

try:
    r = urllib.request.urlopen(req)
    print('Account:', r.read().decode('utf-8'))
except Exception as e:
    print('Error:', e)
