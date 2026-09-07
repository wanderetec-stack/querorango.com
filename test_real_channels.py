import requests, json

url = 'https://api.buffer.com'
headers = {
    'Authorization': 'Bearer _dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2',
    'Content-Type': 'application/json'
}
q = '''
query {
    channels(input: { organizationId: "6a9cafa5247c4b504f81fff4" }) {
        id
        name
        service
    }
}
'''
r = requests.post(url, json={'query': q}, headers=headers)
print(r.text)
