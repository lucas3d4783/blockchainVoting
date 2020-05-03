from django.shortcuts import render
import json
import Pyro4
from unicodedata import normalize


def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'blockchain/index.html')

def add_bloco_generico(request): #quando for solicitado o url index, será encaminhado o index.html
    if request.method == "POST":
        print(request.POST['dados'])
        try:
            dados = normalize('NFKD', request.POST['dados']).encode('ASCII', 'ignore').decode('ASCII') # tratamento para os caracteres especiais
            #dados = json.dumps(request.POST['dados']) # decodificando objeto json para um objeto python
            print(dados)
            ns = Pyro4.locateNS() # localizando o servidor de nomes
            uri = ns.lookup('blockchain') # obtendo a uri do objeto remoto
            o = Pyro4.Proxy(uri) #pegando o objeto remoto
            o.criarBlocoGenerico(dados)
           
        except json.decoder.JSONDecodeError: # "unsupported serialized class: json.decoder.JSONDecodeError"
            print("os dados informados não correspondem a um formato json")
        return render(request, 'blockchain/add_bloco_generico.html')
    return render(request, 'blockchain/add_bloco_generico.html')

def consulta(request): # consultar os blocos da chain
    ns = Pyro4.locateNS() # localizando o servidor de nomes
    uri = ns.lookup('blockchain') # obtendo a uri do objeto remoto
    o = Pyro4.Proxy(uri) #pegando o objeto remoto

    c = o.getChainJson() # pega lista em formato JSON

    lista = json.loads(c) # passa a lista JSON para list

    if o.isChainValid() : # verifica se a chain está válida 
        status = "Consistente"
    else:
        status = "Inconsistente"
    
    n_blocos = o.get_chain_size() + 1 # verifica o número de blocos da chain, contando o bloco gênesis

    context = { # prepara o contexto da resposta 
        'status': status,
        'n_blocos': n_blocos,
        'chain': lista
    }

    return render(request, 'blockchain/consulta.html', context)