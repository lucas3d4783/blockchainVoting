# -*- coding: utf-8 -*-

from flask import Flask, request # importando o Flask framework 
import json
import Pyro4

# RESUMO
#Desenvolvi uma API REST web em Python com o framework Flask, visando disponibilizar métodos de consulta e inserção na blockchain, 
#via requisições web (assim permitindo o uso do curl para as requisições).
#Criei um método para consultar todos os blocks (requisição GET para http://127.0.0.1:8001/blocks), um para filtrar os blocks 
#e só mostrar o block que tem um determinado index [requisição GET para http://127.0.0.1:8001/blocks/x (x sendo um inteiro)], 
#um para filtrar os blocks verificando se é do sistema de votação ou não [requisição GET para http://127.0.0.1:8001/blocks/x 
#(x sendo uma string que será convertida para boolean)] e um método para inserir blocks na blockchain (requisição POST para 
#http://127.0.0.1:8001/blocks passando um objeto json). 

app = Flask(__name__)

nodes = ['b1', 'b2', 'b3', 'b4'] # lista de blocks do sistema

#### Métodos ####

def select_node(): # método que vai percorrer a lista que contém todos os processos do sistema e selecionar o primeiro que responder, como o processo central do sistema
    for node in nodes:
        obj = False # variável para armazenar o processo central
        try:
            ns = Pyro4.locateNS() # localizando o servidor de nomes, e pegando os nomes dos objetos novamente
            try:
                #print(no)
                uri = ns.lookup(node) # obtendo a uri do objeto remoto (pode ser escolhido qualquer processo da rede)
                obj = Pyro4.Proxy(uri) #pegando o objeto remoto
                obj.is_chain_valid() # tenta acessar algum método do objeto para ver se vai gerar exception
            except Pyro4.errors.CommunicationError: # caso ocorra algum erro na comunicação com o nó
                obj = False # Quando não é possível conectar-se com o objeto remoto, o pyro4 armazena um objeto com status not connected, ex: <Pyro4.core.Proxy at 0x7fc5a7ccfc70; not connected; for PYRO:obj_2f0d564eac3f4089bfc782304eaad088@localhost:35723>
                print("O processo", node, "não respondeu")
            if obj: # verifica se foi possível acessar as informações de algum processo da rede
                print("O processo", node, "foi selecionado como nó central")
                return obj
        except Pyro4.errors.NamingError:
            print("Failed to locate the nameserver - Execute o servidor de nomes (pyro4-ns)")
            exit()

    print("Nenhum processo da rede respondeu, verifique a conexão com os nós da rede.")
    return False

def update_block_list(): # atualizar a lista de blocks
    #return normalize('NFKD', o.get_chain_json()).encode('utf8').decode('utf8')
    try: # tenta acessar o processo para obter a chain atualizada
        o = select_node()
        return o.get_chain_json()
    except: # caso não consiga acessar para obter a lista, escolhe um outro processo da rede e tenta obter a chain novamente
        return False


#### Rotas para acessar a API ####

#GET
# curl com requisição com método GET:
# curl http://127.0.0.1:8001/blocks 
# também pode ser usado o comando jq para formatar o objeto json:
# curl http://127.0.0.1:8001/blocks | jq
#@app.route('/', methods=['GET']) # o GET já é por padrão se nada for informado
@app.route('/') # então não foi informado, só que vai ser o rota padrão
def home():
    return "API da Blockchain", 200 # vai retornar uma string e um status de sucesso (200)

@app.route('/blocks', methods=['GET']) 
def blocks(): # retorna todos os blocks
    blockchain = update_block_list()
    if blockchain == False: 
        return '{"erro": "Não foi possível obter a Blockchain, tente novamente!"}', 500
    return '{"blockchain":' + str(blockchain) + '}', 200 

@app.route('/blocks/amount', methods=['GET']) 
def amount(): # retorna todos os blocks
    try:
        o = select_node()
        amount = '{"amount":"' + str(o.get_chain_size()) + '"}'
        return amount, 200 
    except:
        return '{"erro": "Não foi possível verificar o número total de blocks da Blockchain, tente novamente!"}', 500

@app.route('/blocks/status', methods=['GET']) 
def status(): # retorna todos os blocks
    try:
        o = select_node()
        status = '{"status":"' + str(o.is_chain_valid()) + '"}'
        return status, 200 
    except: # exception caso o objeto esteja cadastrado no servidor de nomes, mas ocorra algum erro na comunicação com o mesmo
        return '{"erro": "Não foi possível verificar o STATUS da Blockchain, tente novamente!"}', 500

@app.route('/blocks/compare_chains', methods=['GET']) 
def compare_chains(): # Retorna a porcentagem de processos que estão com a chain no mesmo estado que o processo central
    try:
        o = select_node()
        porcentagem = '{"porcentagem":"' + str(o.compare_chains()) + '%"}'
        return porcentagem, 200 
    except: # exception caso o objeto esteja cadastrado no servidor de nomes, mas ocorra algum erro na comunicação com o mesmo
        return '{"erro": "Não foi possível fazer a comparação entre as cadeias de blocks dos processos da rede, tente novamente!"}', 500

@app.route('/blocks/amount_of_nodes', methods=['GET']) 
def amount_of_nodes(): # Retorna a amount de processos do sistema 
    quant = '{"amount_of_nodes":"' + str(len(nodes)) + '"}'
    return quant, 200 

#EXEMPLO:
# curl http://127.0.0.1:8001/blocks/1 | jq
@app.route('/blocks/<int:index>', methods=['GET']) 
def blocks_por_index(index): # filtrar blocks por index
    try:
        blockchain = json.loads(update_block_list())
        blocks = [block for block in blockchain if block['index'] == index] 
        if len(blocks) < 1: # caso não encontre nenhum block com o index informado
            return json.dumps({"erro": "Index nao encontrado!"}), 404
        return json.dumps(blocks), 200 # se encontrar retorna o block e um status de sucesso
    except:
        return '{"erro": "Não foi possível retornar o block, tente novamente!"}', 500


#POST
# requisição com método POST com curl:
# curl -X POST -H 'Content-Type: application/json' -d '{"exemplo": 1, "testando": "uma inserção qualquer"}' http://127.0.0.1:8001/blocks
@app.route('/blocks', methods=['POST']) 
def create_block():
    data = str(request.get_json())
    try:
        o = select_node()
        o.create_block(json.dumps(data))
        return json.dumps(data), 201
    except:
        return '{"erro": "Não foi possível adicionar o block na cadeia, tente novamente!"}', 500

if __name__=='__main__':
    app.run(debug=True, port=8001)

