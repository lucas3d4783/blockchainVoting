from flask import Flask, request # importando o Flask framework 
import json
import Pyro4
from unicodedata import normalize

# RESUMO
#Desenvolvi uma API REST web em Python com o framework Flask, visando disponibilizar métodos de consulta e inserção na blockchain, 
#via requisições web (assim permitindo o uso do curl para as requisições).
#Criei um método para consultar todos os blocos (requisição GET para http://127.0.0.1:8001/blocos), um para filtrar os blocos 
#e só mostrar o bloco que tem um determinado index [requisição GET para http://127.0.0.1:8001/blocos/x (x sendo um inteiro)], 
#um para filtrar os blocos verificando se é do sistema de votação ou não [requisição GET para http://127.0.0.1:8001/blocos/x 
#(x sendo uma string que será convertida para boolean)] e um método para inserir blocos na blockchain (requisição POST para 
#http://127.0.0.1:8001/blocos passando um objeto json). 

app = Flask(__name__)

#GET
# curl com requisição com método GET:
# curl http://127.0.0.1:8001/blocos 
# também pode ser usado o comando jq para formatar o objeto json:
# curl http://127.0.0.1:8001/blocos | jq
#@app.route('/', methods=['GET']) # o GET já é por padrão se nada for informado
@app.route('/') # então não foi informado, só que vai ser o rota padrão
def home():
    return "API da Blockchain", 200 # vai retornar uma string e um status de sucesso (200)

ns = Pyro4.locateNS() # localizando o servidor de nomes
uri = ns.lookup('blockchain') # obtendo a uri do objeto remoto
o = Pyro4.Proxy(uri) #pegando o objeto remoto
#blockchain = o.getChainJson() # pega a lista de blocos em formato JSON

def atualizaListaDeBlocos(): # atualizar a lista de blocos
    return o.getChainJson()

@app.route('/blocos', methods=['GET']) 
def blocos(): # retorna todos os blocos
    blockchain = atualizaListaDeBlocos()
    return blockchain, 200 

@app.route('/blocos/<string:isVoto>', methods=['GET']) 
def blocos_por_isVoto(isVoto): # filtrar blocos por isVoto (True/False)
    blockchain = json.loads(atualizaListaDeBlocos())
    if isVoto == "false" or isVoto == "False": # verifica se foi passado False
        isVoto = "" # o bool() interpreta "" como false
    blocos = [bloco for bloco in blockchain if bloco['isVoto'] == bool(isVoto)] 
    return json.dumps(blocos), 200

#EXEMPLO:
# curl http://127.0.0.1:8001/blocos/1 | jq
@app.route('/blocos/<int:index>', methods=['GET']) 
def blocos_por_index(index): # filtrar blocos por index
    blockchain = json.loads(atualizaListaDeBlocos())
    blocos = [bloco for bloco in blockchain if bloco['index'] == index] 
    if len(blocos) < 1: # caso não encontre nenhum bloco com o index informado
        return json.dumps({"erro": "Index nao encontrado!"}), 404
    return json.dumps(blocos), 200 # se encontrar retorna o bloco e um status de sucesso


#POST
# requisição com método POST com curl:
# curl -X POST -H 'Content-Type: application/json' -d '{"exemplo": 1, "testando": "uma inserção qualquer"}' http://127.0.0.1:8001/blocos
@app.route('/blocos', methods=['POST']) 
def add_bloco_generico():
    dados = normalize('NFKD', str(request.get_json())).encode('ASCII', 'ignore').decode('ASCII')
    o.criarBlocoGenerico(json.dumps(dados))
    return json.dumps(dados), 201


if __name__=='__main__':
    app.run(debug=True, port=8001)

