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
        text: "Teste de receita do Quero Rango",
        mode: shareNow,
        schedulingType: automatic
    }) {
        __typename
        ... on PostActionSuccess {
            post {
                id
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
        ... on InvalidInputError {
            message
        }
        ... on UnexpectedError {
            message
        }
        ... on NotFoundError {
            message
        }
    }
}
'''
r = requests.post(url, json={'query': q}, headers=headers, timeout=20)
print(r.text)
