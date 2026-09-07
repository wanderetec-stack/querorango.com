import requests, json

url = 'https://api.buffer.com'
headers = {
    'Authorization': 'Bearer _dycXWygKpeBamrEhHYC-NOMZN4NbG_8I4kGWrIn-E2',
    'Content-Type': 'application/json'
}
q = '''
mutation {
    createPost(input: {
        channelId: "6a9cb071065799be4698d386",
        text: "Receita de Bolo de Cenoura Fofinho com Cobertura de Chocolate! Passo a passo completo no Quero Rango:",
        mode: shareNow,
        schedulingType: automatic,
        metadata: {
            facebook: {
                type: post,
                linkAttachment: {
                    url: "https://querorango.com/receitas/bolos/bolo-de-cenoura/"
                }
            }
        }
    }) {
        __typename
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
        ... on InvalidInputError {
            message
        }
        ... on UnexpectedError {
            message
        }
    }
}
'''
r = requests.post(url, json={'query': q}, headers=headers, timeout=25)
print('Status:', r.status_code)
print('Response:', r.text)
