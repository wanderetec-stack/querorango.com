import urllib.request, json

TOKEN = '_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2'

query = {
    'query': '''
        query {
            __type(name: "CreatePostInput") {
                inputFields {
                    name
                    type {
                        name
                        kind
                        ofType {
                            name
                            kind
                        }
                    }
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
for f in data['data']['__type']['inputFields']:
    t = f['type']['name'] or (f['type']['ofType']['name'] if f['type']['ofType'] else '')
    print(f['name'], '->', t)
