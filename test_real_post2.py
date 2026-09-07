import requests, json

url = 'https://api.buffer.com'
headers = {
    'Authorization': 'Bearer _dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2',
    'Content-Type': 'application/json'
}
q = '''
mutation {
    createPost(input: {
        channelId: "6a9cb071065799be4698d986",
        text: "Receita deliciosa do Quero Rango! https://querorango.com",
        mode: shareNow,
        schedulingType: automatic
    }) {
        ... on PostActionSuccess {
            post {
                id
                status
            }
        }
        ... on RestProxyError {
            message
        }
        ... on UnauthorizedError {
            message
        }
        ... on LimitReachedError {
            message
        }
    }
}
'''
r = requests.post(url, json={'query': q}, headers=headers, timeout=20)
print('Status:', r.status_code)
print('Response:', r.text)
