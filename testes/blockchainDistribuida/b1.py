import hashlib
import json
import datetime
import Pyro4 #biblioteca para a utilização de objetos remotos
from pytz import timezone
import threading
import pickle
import threading # foi optado por usar Threads e não forks para não vincular a execução do programa a um sistema operacional específico, neste caso linux ou mac, pois eles possuem o recursos os.fork por serem baseados em Unix
# além disso a bilioteca threading tem um desempenho melho do que a biblioteca __thread 


atual = 'b1' # nó atual
#nos = ['b1', 'b2', 'b3', 'b4'] # lista de blocos do sistema
nos = ['b1', 'b2', 'b3'] # lista de blocos do sistema


class Minhathread(threading.Thread): # chamar os outros  nós da rede, um em cada thread
    achou_nonce = False
    def __init__(self, bloco, no, mutex):
        self.bloco = bloco
        self.no = no
        self.mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        #with self.mutex: # para evitar que mais de uma thread use o print ao mesmo tempo   
            ns = Pyro4.locateNS() # localizando o servidor de nomes
            uri = ns.lookup(self.no) # obtendo a uri do objeto remoto
            o = Pyro4.Proxy(uri) #pegando o objeto remoto

            b = {"index":self.bloco.index, "nonce":self.bloco.nonce, "tstamp":self.bloco.tstamp, "dados":self.bloco.dados, "prevhash":self.bloco.prevhash, "hash":self.bloco.hash}

            #b = {"index":self.bloco.index, "nonce":self.bloco.nonce, "tstamp":self.bloco.tstamp, "dados":"teste", "prevhash":"teste", "hash":self.bloco.hash}
            bloco = json.dumps(b)
            #print(bloco.__str__())

            print("enviado bloco para o nó ", self.no) # printando qual bloco está sendo enviado para qual nó da rede 

            retorno = o.consenso(bloco) # enviando o bloco serelizado para objeto remoto minerar 

            if Minhathread.achou_nonce == False:
                Minhathread.achou_nonce = retorno
                print("O nó ", self.no, " encontrou o nonce primeiro: ", str(Minhathread.achou_nonce))
           
            print("O nó ", self.no, " encontrou o nonce: ", str(retorno))

    print('Saindo da Thread Principal')


#primeiramente deve ser definido o bloco
class Block(): # classe utilizada para a criação e manipulação de cada bloco de forma individual
    #construtor do bloco
    def __init__(self, index=0, dados='{"Genesis Block":"Genesis Block"}', prevhash='{"Genesis Block":"Genesis Block"}', nonce=0): #quando não temos um bloco anterior, definimos ele como uma string vazia (valor default)
        #variáveis da classe
        self.index=index # index do bloco
        self.nonce=nonce # resposta do desafio para minerar o bloco
        self.tstamp=str(datetime.datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime("%s")) # quando o bloco foi criado, para poder realizar comparações posteriores         self.dados=dados # dados que serão armazenados em formato JSON no bloco
        self.dados=dados
        self.prevhash=prevhash # hash do bloco anterior
        self.hash=self.calcHash() # hash do bloco atual 

    #função responsável por realizar o cálculo do hash do bloco
    def calcHash(self):
        #criando um dicionário com json, passando parâmetro por parâmetro, por fim, codificando para gerar o hash posteriormente
        block_string=json.dumps({"index":self.index, "nonce":self.nonce, "tstamp":self.tstamp, "dados":self.dados, "prevhash":self.prevhash,}, sort_keys=True, ).encode()
        #retornando o hash do bloco
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self, diffic): # método utilizado para encontrar um hash com um determinado número de zeros no início (dificuldade)
        while(self.hash[:diffic] != str('').zfill(diffic)): # enquanto a o inicio do hash do bloco até a dificuldade -1 não for igual a uma string que tenha o mesmo números de zeros que a dificuldade
            self.nonce += 1 # incrementando o nonce para gerar um novo hash do bloco (também pode ser realizado de forma aleatória)
            self.hash=self.calcHash() # gerando um novo hash para o bloco 
        print("Bloco Minerado! - ", self.hash)
    
    # método para retornar informações do bloco
    def __str__(self):
        bloco = "------------------------------" 
        bloco += "\nindex: " + str(self.index) 
        bloco += "\nnonce: " + str(self.nonce)
        bloco += "\ntstamp: " + str(self.tstamp)
        bloco += "\n\n ---> DADOS"
        bloco += "\n" + str(self.dados)
        bloco += "\n <--- \n"
        bloco += "\nprev_hash: " + str(self.prevhash)
        bloco += "\nhash: " + str(self.hash)
        bloco += "\n------------------------------"
        return bloco


@Pyro4.expose
# após criar a classe referente aos blocos, deve ser criado a classe que vai representar a cadeia de blocos
class Blockchain(): #classe que será utilizada para armazenar e gerenciar a cadeia de blocos
    def __init__(self): #função construct da classe
        self.unconfirmed_transactions = []
        self.chain=[self.generateGenesisBlock(),] #criando a lista que será utilizada para armazenar os blocos, além de adicionar o bloco gênesis
        self.difficulty=4 # definindo a dificuldade da mineração - quanto maior o valor, mais tempo para minerar
        bloco = Block() # criando um bloco genérico para enviar para os nós e testar a chain
        self.enviar_para_os_nos(bloco) # para testes ao iniciar a chain

    def generateGenesisBlock(self): #método para a criação de um bloco gênesis
        bloco = Block(0)
        bloco.tstamp = 0 # modificando o tstamp para que todos os blocos da rede tenham o mesmo bloco gênesis

        return bloco #retorna um bloco gênesis
    
    def getLastBlock(self): #método para obter o último bloco da cadeia
        return self.chain[-1] #pega o último elemento da lista
    
    def addBlock(self, newBlock): #adicionar novo bloco na cadeia, passando o novo bloco como parâmetro
        newBlock.prevhash=self.getLastBlock().hash # definindo o atributo 'prevhash' como o hash do último bloco da cadeia de blocos
        newBlock.mineBlock(self.difficulty) #calculando o hash do novo bloco
        #aplicar semaforos no método
        self.chain.append(newBlock) #adicionando o bloco novo na chain (lista da classe Blockchain)
        print(self.getChain())
    
    def isChainValid(self): # Método para verificar de a cadeia de blocos é válida
        for i in range(1, len(self.chain)): # varrendo os blocos da lista, exceto o bloco gênesis
            prevb=self.chain[i-1] #pegando o bloco anterior da lista (i - 1)
            currb=self.chain[i] #pegando o bloco atual da lista
            if(currb.hash != currb.calcHash()): # realizando o cálculo do hash do bloco atual para verificar se algum dado do bloco foi alterado, caso tenha sido alterado fazendo com que o hash não seja igual ao original, é retornado False
                print("inconsistência no bloco")
                return "inconsistência no bloco" # retorna falso caso algum valor do bloco tenha sido alterado
            if(currb.prevhash != prevb.hash): # verifica se a ligação com o bloco anterior ainda é válida, ou seja, se o campo prevhash do bloco atual, é igual ao campo hash do bloco anterior
                print("inconsistência na chain")
                return "inconsistência na chain" # se os hashes forem diferente, é retornado falso
        return True

    def synchronized(func):
        func.__lock__ = threading.Lock()
            
        def synced_func(*args, **kws):
            with func.__lock__:
                return func(*args, **kws)
        
        return synced_func
    
    @synchronized
    def criarBloco(self, objJson):
        index = len(self.chain)
        try:
            d = json.loads(objJson) # tentando converter o objeto passado como parâmetro para um objeto python
        except json.decoder.JSONDecodeError: # caso o tipo de dado informado não possa ser convertido para json, vai ser retornado False 
            print("Não foi possível criar um bloco, pois o tipo de dado informado não é válido")
            return False

        bloco = Block(index, objJson) # criando um bloco 

        self.addBlock(bloco) # adicionando o bloco na chain
        return True
    
    def getChain(self):
        result = "";
        for bloco in self.chain: #varrer a cadeia de blocos
            result+="\n------------------------------\n"
            result+="           BLOCO " + str(bloco.index) + "\n"
            result+=bloco.__str__() + "\n" # mostrando as informações do respectivo bloco

        return result;
        #print("Estado do sistema: ", self.isChainValid()) #verifica a integridade dos blocos e da chain
    
    def getChainJson(self):
        lista = []
        for bloco in self.chain:
            lista.append({"index":bloco.index, "nonce":bloco.nonce, "tstamp":bloco.tstamp, "dados":bloco.dados, "prevhash":bloco.prevhash, "hash":bloco.hash})
        return json.dumps(lista)

    def get_chain_size(self): # obter o tamanho da cadeia de blocos sem contar o bloco gênesis
        return len(self.chain)-1
    
    # MÉTODOS PARA APLICAR DE FORMA DISTRIBUÍDA 

    def enviar_para_os_nos(self, bloco): # chamada remota para os outros nós da rede em diferentes threads
        stdoutmutex = threading.Lock()
        threads = []
        
        for no in nos:
            if no != atual: # verifica se o objeto não tem o mesmo nome do objeto atual    
                thread = Minhathread(bloco, no, stdoutmutex)
                thread.start() # método da classe pai, dar iniciar a thread, vai criar operações básicas para poder usar 
                threads.append(thread)

        #for thread in threads:
        #    print('executando a Thread')
        #    thread.join() # método da classe pai, este método espera até a threading terminar quando ela teminar ele executa o print
    
        print("enviou para os nós")

        return True
    
    def consenso(self, bloco):
        #bloco = json.loads(bloco)
        #self.add_new_transaction(bloco) #desserializando o objeto e convertendo ele para python

        #bloco.prevhash=self.getLastBlock().hash
        #bloco.mineBlock(self.difficulty)
        
        #return bloco.nonce
        #self.chain.append(newBlock)

        print("recebeu dos outros nós")
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and block_hash == block.compute_hash())

    def add_new_transaction(self, bloco):
        self.unconfirmed_transactions.append(bloco)



 
    #def mine(self):
    #    if not self.unconfirmed_transactions:
    #        return False
 
    #    last_block = self.getLastBlock()
 
    #    new_block = Block()
 
    #    proof = self.proof_of_work(new_block)
    #    self.add_block(new_block, proof)
    #    self.unconfirmed_transactions = []
    #    return new_block.index



# para adicionar um bloco da forma original, pode ser considerado muito fácil, porém se for muito fácil adiconar um novo bloco
# um hacker poderia alterar toda a cadeia de bloco de forma fácil, para evitar esse tipo de problema, são utilizados
# alguns algoritmos de consendo (probabilístico), como por exemplo o Proof of Work (PoW), o PoW torna a adição de um bloco 
# na chain uma tarefa difícil, por exemplo no Bitcoin que é apenas aceitos os hashes que começam com um específico 
# número de zeros, além do mesmo ter de ser realizado dentro de um tempo limite (encontrar um nonce adequado para ganhar o desafio)
# então um bloco será adicionado a cada 10 minutos
# a quantidade de números zeros no início dos hashes é chamada de dificuldade, então se tiver apenas 1 zero a dificuldade 
# será 1, se tiver dois zeros, a dificuldade será 2, etc.
# Como a técnologia de processamento está sempre evoluindo o bitcoin, tem sua dificuldade aumentada a cada 2 ou 3 anos.
# o processo de encontrar um certo número de zeros no início do hash do bloco, é chamado de minerar.

daemon = Pyro4.Daemon()

blockchain=Blockchain() # passando o objeto já isntânciado para manter os dados salvos de um acesso a outro do objeto remoto
uri = daemon.register(blockchain) #instanciando um objeto remoto, realizando o registrando dele. Vai ser retornando#
# uma URI do objeto para ele poder ser acessado, o método também vai checar se já não há um objeto registrado

# para poder utilizar deve estar sendo executado o pyro-ns em um terminal
ns = Pyro4.locateNS() # Get a proxy for a name server somewhere in the network.
ns.register('b1', uri) # simplificando o nome do objeto

print(uri)

daemon.requestLoop()

