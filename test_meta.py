import requests, json

url = 'https://api.buffer.com'
headers = {
    'Authorization': 'Bearer _dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2',
    'Content-Type': 'application/json'
}
q = '''
query {
    __type(name: "PostInputMetaData") {
        inputFields {
            name
            type {
                name
                kind
                ofType {
                    name
                }
            }
        }
    }
}
'''
r = requests.post(url, json={'query': q}, headers=headers)
print(r.text)
