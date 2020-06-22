# -*- coding: utf-8 -*-

from flask import Flask, request # importando o Flask framework 
import json
import Pyro4

# RESUMO
#Desenvolvi uma API REST web em Python com o framework Flask, visando disponibilizar métodos de consulta e inserção na blockchain, 
#via requisições web (assim permitindo o uso do curl para as requisições).
#Criei um método para consultar todos os blocos (requisição GET para http://127.0.0.1:8001/blocos), um para filtrar os blocos 
#e só mostrar o bloco que tem um determinado index [requisição GET para http://127.0.0.1:8001/blocos/x (x sendo um inteiro)], 
#um para filtrar os blocos verificando se é do sistema de votação ou não [requisição GET para http://127.0.0.1:8001/blocos/x 
#(x sendo uma string que será convertida para boolean)] e um método para inserir blocos na blockchain (requisição POST para 
#http://127.0.0.1:8001/blocos passando um objeto json). 

app = Flask(__name__)

nos = ['b1', 'b2', 'b3', 'b4'] # lista de blocos do sistema

#### Métodos ####

def selecionaNo(): # método que vai percorrer a lista que contém todos os processos do sistema e selecionar o primeiro que responder, como o processo central do sistema
    for no in nos:
        obj = False # variável para armazenar o processo central
        try:
            ns = Pyro4.locateNS() # localizando o servidor de nomes, e pegando os nomes dos objetos novamente
            try:
                #print(no)
                uri = ns.lookup(no) # obtendo a uri do objeto remoto (pode ser escolhido qualquer processo da rede)
                obj = Pyro4.Proxy(uri) #pegando o objeto remoto
                obj.isChainValid() # tenta acessar algum método do objeto para ver se vai gerar exception
            except Pyro4.errors.CommunicationError: # caso ocorra algum erro na comunicação com o nó
                obj = False # Quando não é possível conectar-se com o objeto remoto, o pyro4 armazena um objeto com status not connected, ex: <Pyro4.core.Proxy at 0x7fc5a7ccfc70; not connected; for PYRO:obj_2f0d564eac3f4089bfc782304eaad088@localhost:35723>
                print("O processo", no, "não respondeu")
            if obj: # verifica se foi possível acessar as informações de algum processo da rede
                print("O processo", no, "foi selecionado como nó central")
                return obj
        except Pyro4.errors.NamingError:
            print("Failed to locate the nameserver - Execute o servidor de nomes (pyro4-ns)")
            exit()

    print("Nenhum processo da rede respondeu, verifique a conexão com os nós da rede.")
    return False

def atualizaListaDeBlocos(): # atualizar a lista de blocos
    #return normalize('NFKD', o.getChainJson()).encode('utf8').decode('utf8')
    try: # tenta acessar o processo para obter a chain atualizada
        o = selecionaNo()
        return o.getChainJson()
    except: # caso não consiga acessar para obter a lista, escolhe um outro processo da rede e tenta obter a chain novamente
        return False


#### Rotas para acessar a API ####

#GET
# curl com requisição com método GET:
# curl http://127.0.0.1:8001/blocos 
# também pode ser usado o comando jq para formatar o objeto json:
# curl http://127.0.0.1:8001/blocos | jq
#@app.route('/', methods=['GET']) # o GET já é por padrão se nada for informado
@app.route('/') # então não foi informado, só que vai ser o rota padrão
def home():
    return "API da Blockchain", 200 # vai retornar uma string e um status de sucesso (200)

@app.route('/blocos', methods=['GET']) 
def blocos(): # retorna todos os blocos
    blockchain = atualizaListaDeBlocos()
    if blockchain == False: 
        return '{"erro": "Não foi possível obter a Blockchain, tente novamente!"}', 500
    return '{"blockchain":' + str(blockchain) + '}', 200 

@app.route('/blocos/quantidade', methods=['GET']) 
def quantidade(): # retorna todos os blocos
    try:
        o = selecionaNo()
        quantidade = '{"quantidade":"' + str(o.get_chain_size()) + '"}'
        return quantidade, 200 
    except:
        return '{"erro": "Não foi possível verificar o número total de blocos da Blockchain, tente novamente!"}', 500

@app.route('/blocos/status', methods=['GET']) 
def status(): # retorna todos os blocos
    try:
        o = selecionaNo()
        status = '{"status":"' + str(o.isChainValid()) + '"}'
        return status, 200 
    except: # exception caso o objeto esteja cadastrado no servidor de nomes, mas ocorra algum erro na comunicação com o mesmo
        return '{"erro": "Não foi possível verificar o STATUS da Blockchain, tente novamente!"}', 500

@app.route('/blocos/comparaChains', methods=['GET']) 
def coparaChains(): # Retorna a porcentagem de processos que estão com a chain no mesmo estado que o processo central
    try:
        o = selecionaNo()
        porcentagem = '{"porcentagem":"' + str(o.comparaChains()) + '%"}'
        return porcentagem, 200 
    except: # exception caso o objeto esteja cadastrado no servidor de nomes, mas ocorra algum erro na comunicação com o mesmo
        return '{"erro": "Não foi possível fazer a comparação entre as cadeias de blocos dos processos da rede, tente novamente!"}', 500

#EXEMPLO:
# curl http://127.0.0.1:8001/blocos/1 | jq
@app.route('/blocos/<int:index>', methods=['GET']) 
def blocos_por_index(index): # filtrar blocos por index
    try:
        blockchain = json.loads(atualizaListaDeBlocos())
        blocos = [bloco for bloco in blockchain if bloco['index'] == index] 
        if len(blocos) < 1: # caso não encontre nenhum bloco com o index informado
            return json.dumps({"erro": "Index nao encontrado!"}), 404
        return json.dumps(blocos), 200 # se encontrar retorna o bloco e um status de sucesso
    except:
        return '{"erro": "Não foi possível retornar o bloco, tente novamente!"}', 500


#POST
# requisição com método POST com curl:
# curl -X POST -H 'Content-Type: application/json' -d '{"exemplo": 1, "testando": "uma inserção qualquer"}' http://127.0.0.1:8001/blocos
@app.route('/blocos', methods=['POST']) 
def criarBloco():
    dados = str(request.get_json())
    try:
        o = selecionaNo()
        o.criarBloco(json.dumps(dados))
        return json.dumps(dados), 201
    except:
        return '{"erro": "Não foi possível adicionar o bloco na cadeia, tente novamente!"}', 500

if __name__=='__main__':
    app.run(debug=True, port=8001)

