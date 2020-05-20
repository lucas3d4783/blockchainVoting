import requests, json

# home
r = requests.get('http://127.0.0.1:8001/')
print(r.text)

# obter todos os blocos 
r = requests.get('http://127.0.0.1:8001/blocos')
print("\nBlocos:\n", r.text)

# obter bloco por index
index = 1
r = requests.get('http://127.0.0.1:8001/blocos/'+str(index))
print("\nBlocos passando um INDEX:\n", r.text)

# obter votos referentes aos processos eleitorais (True) ou os que não são referentes ao processo eleitoral (False)
b = False
r = requests.get('http://127.0.0.1:8001/blocos/'+str(b))
print("\nBlocos passando True ou False:\n", r.text)

# passando objeto json via método post
url = 'http://127.0.0.1:8001/blocos'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}
requests.post(url, data=json.dumps(payload), headers=headers)

# obter todos os blocos 
r = requests.get('http://127.0.0.1:8001/blocos')
print(r.text)