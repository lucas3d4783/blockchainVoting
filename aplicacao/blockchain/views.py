from django.shortcuts import render
import json
import Pyro4
from unicodedata import normalize
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
            requests.post(url, data=json.dumps(payload), headers=headers)
        except json.decoder.JSONDecodeError: # "unsupported serialized class: json.decoder.JSONDecodeError"
            print("os dados informados não correspondem a um formato json")
        return render(request, 'blockchain/add_bloco_generico.html')
    return render(request, 'blockchain/add_bloco_generico.html')

def consulta(request): # consultar os blocos da chain

    # obter todos os blocos 
    blockchain = requests.get('http://127.0.0.1:8001/blocos')

    # verifica o número de blocos da chain, sem contar o bloco gênesis
    n_blocos = requests.get('http://127.0.0.1:8001/blocos/quantidade')

    # obter o status da chain
    status = requests.get('http://127.0.0.1:8001/blocos/status')

    #print(blockchain.text)
    lista = json.loads(blockchain.text)

    context = { # prepara o contexto da resposta 
        'status': status.text,
        'n_blocos': n_blocos.text,
        'chain': lista
    }

    return render(request, 'blockchain/consulta.html', context)