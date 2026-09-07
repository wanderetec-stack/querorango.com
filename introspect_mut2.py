import urllib.request, json

TOKEN = '_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2'

query = {
    'query': '''
        query {
            __type(name: "Mutation") {
                fields {
                    name
                    type {
                        ofType {
                            name
                            kind
                            fields {
                                name
                            }
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
for f in data['data']['__type']['fields']:
    if f['name'] == 'createPost':
        print('Return type:', f['type']['ofType']['name'])
        print('Fields:', [x['name'] for x in f['type']['ofType']['fields']])
