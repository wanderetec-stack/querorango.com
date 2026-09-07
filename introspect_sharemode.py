import urllib.request, json

TOKEN = '_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2'

query = {
    'query': '''
        query {
            __type(name: "ShareMode") {
                enumValues {
                    name
                }
            }
        }
    '''
}

req = urllib.request.Request(
    'https://api.buffer.com',
    data=json.dumps(query).encode('utf-8'),
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
)

r = urllib.request.urlopen(req)
data = json.loads(r.read())
print('ShareModes:', [v['name'] for v in data['data']['__type']['enumValues']])
