import urllib.request, json

TOKEN = '_dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2'
CHANNEL_ID = '6a9cb071065799be4698d986'

# Let's inspect root queries available in Buffer GraphQL
query = {
    'query': '''
        query {
            __schema {
                queryType {
                    fields {
                        name
                    }
                }
                mutationType {
                    fields {
                        name
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
print('Queries:', [f['name'] for f in data['data']['__schema']['queryType']['fields']])
print('Mutations:', [f['name'] for f in data['data']['__schema']['mutationType']['fields']])
