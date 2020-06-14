import requests, json
from unicodedata import normalize

# home
r = requests.get('http://127.0.0.1:8001/')
print(r.text)

# obter todos os blocos 
r = requests.get('http://127.0.0.1:8001/blocos')
print("\nBlocos:\n", r.text)

# obter a quantidade de blocos sem contar o bloco gênesis
r = requests.get('http://127.0.0.1:8001/blocos/quantidade')
print("Quantidade de blocos:", r.text)

# obter o status da chain 
r = requests.get('http://127.0.0.1:8001/blocos/status')
print("STATUS:", r.text)

# obter bloco por index
index = 1
r = requests.get('http://127.0.0.1:8001/blocos/'+str(index))
print("\nBlocos passando um INDEX:\n", r.text)

# passando objeto json via método post
url = 'http://127.0.0.1:8001/blocos'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}
requests.post(url, data=json.dumps(payload), headers=headers)

# obter todos os blocos 
r = requests.get('http://127.0.0.1:8001/blocos')
print(r.text)