from django.shortcuts import render
import json
import Pyro4
from unicodedata import normalize

# Create your views here.

class Bloco():
    def __init__(self, index, nonce, tstamp, isVoto, dados, prevhash, b_hash): 
        #variáveis da classe
        self.index=index # index do bloco
        self.nonce=nonce # resposta do desafio para minerar o bloco
        self.tstamp=tstamp
        self.isVoto=isVoto # flag para identificar se o bloco corresponde a um voto do sistema de votação ou não 
        self.dados=dados # dados que serão armazenados em formato JSON no bloco
        self.prevhash=prevhash # hash do bloco anterior
        self.hash=b_hash # hash do bloco atual 

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
            uri = ns.lookup('obj') # obtendo a uri do objeto remoto
            o = Pyro4.Proxy(uri) #pegando o objeto remoto
            o.criarBlocoGenerico(dados)
           
        except json.decoder.JSONDecodeError: # "unsupported serialized class: json.decoder.JSONDecodeError"
            print("os dados informados não correspondem a um formato json")
        return render(request, 'blockchain/add_bloco_generico.html')
    return render(request, 'blockchain/add_bloco_generico.html')

def consulta(request): #
    ns = Pyro4.locateNS() # localizando o servidor de nomes
    uri = ns.lookup('obj') # obtendo a uri do objeto remoto
    o = Pyro4.Proxy(uri) #pegando o objeto remoto
    #chain = o.getChainJson() # obtendo a chain
    #c = json.dumps(o.getChainJson())
    #chain = json.loads(c) 
    c = o.getChainJson()
    #print(type(json.loads(c)))
    
    chain = json.loads(c)

    lista = []
    for b in chain["bloco"]:
        bloco = Bloco(b["index"], b["nonce"], b["tstamp"], b["isVoto"], b["dados"], b["prev_hash"], b["hash"])
        lista.append(bloco)

    #print((chain["bloco"][0]["index"]))

    status = o.isChainValid()
    context = {
        'status': status,
        'chain': lista
    }

    return render(request, 'blockchain/consulta.html', context)