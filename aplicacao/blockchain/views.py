from django.shortcuts import render
import json
import Pyro4
import requests

def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'blockchain/index.html')

def add_bloco_generico(request): #quando for solicitado o url index, será encaminhado o index.html
    if request.method == "POST":
        print(request.POST['dados'])
        try:
            dados = request.POST['dados']
            url = 'http://127.0.0.1:8001/blocos'
            payload = dados
            headers = {'content-type': 'application/json'}
            #json.dumps(payload) # só para ver se não vai gerar exception
            requests.post(url, data=json.dumps(payload), headers=headers)
        except json.decoder.JSONDecodeError: # "unsupported serialized class: json.decoder.JSONDecodeError"
            print("os dados informados não correspondem a um formato json")
        return render(request, 'blockchain/add_bloco_generico.html')
    return render(request, 'blockchain/add_bloco_generico.html')

def consulta(request): # consultar os blocos da chain

    # verifica o número de blocos da chain, sem contar o bloco gênesis
    r = requests.get('http://127.0.0.1:8001/blocos/quantidade')
    n_blocos = json.loads(r.text)
    if 'quantidade' in n_blocos: # verfica se foi retornado a quantidade de blocos da chain
        n_blocos = n_blocos['quantidade']
    if 'erro' in n_blocos: # verifica se foi retornado um erro
        n_blocos = n_blocos['erro']

    # obter o status da chain
    r = requests.get('http://127.0.0.1:8001/blocos/status')
    status = json.loads(r.text)
    if 'status' in status: # verfica se foi retornado algum status
        status = "Consistente"
    if 'erro' in status: # verifica se foi retornado um erro
        status = status['erro']
    
    context = { # prepara o contexto da resposta 
        'status': status,
        'n_blocos': n_blocos,
    }

    # obter todos os blocos 
    r = requests.get('http://127.0.0.1:8001/blocos')
    blockchain = json.loads(r.text)
    if 'blockchain' in blockchain: # verifica se a cadeia de blocos foi retornada
        chain = blockchain['blockchain']
        context = { # prepara o contexto da resposta 
            'status': status,
            'n_blocos': n_blocos,
            'chain': chain
        }

    if 'erro' in blockchain: # verifica se foi retornado um erro
        erro = blockchain['erro']
        context = { # prepara o contexto da resposta 
            'erro': erro,
        }
        return render(request, 'blockchain/consulta.html', context)

    return render(request, 'blockchain/consulta.html', context)