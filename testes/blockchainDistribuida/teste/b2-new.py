# -*- coding: utf-8 -*-

import hashlib
import json
import datetime
import Pyro4 #biblioteca para a utilização de objetos remotos
from pytz import timezone
import threading
import pickle

current = 'b2' # current node
nodes = ['b1', 'b2', 'b3', 'b4'] # lista de blocks do sistema

class send_block_for_all_nodes(threading.Thread): # enviar block para os outros nós da rede, um em cada thread
    found_nonce = False
    nonce = 0
    def __init__(self, block, node, mutex):
        self.block = block
        self.node = node
        self.mutex = mutex
        #print("Mutex type: ", type(mutex)) # _thread.lock
        threading.Thread.__init__(self)

    def run(self):
        #with self.mutex: # para evitar que mais de uma thread use o print ao mesmo tempo   
            try:
                ns = Pyro4.locateNS() # localizando o servidor de nomes
            except Pyro4.errors.NamingError: # caso o servidor de nomes não esteja sendo executado
                print("Falha para localizar o servidor de nomes! - Execute o servidor de nomes (pyro4-ns)")
                exit()

            try: 
                uri = ns.lookup(self.node) # obtendo a uri do objeto remoto
                o = Pyro4.Proxy(uri) #pegando o objeto remoto

                b = {"index":self.block.index, "nonce":self.block.nonce, "tstamp":self.block.tstamp, "data":self.block.data, "prevhash":self.block.prevhash, "hash":self.block.hash}
                block = json.dumps(b)

                print("Enviado block para o nó ", self.node) # printando qual block está sendo enviado para qual nó da rede 

                retorno = o.consensus(block) # enviando o block serelizado para objeto remoto minerar 
            except: # caso ocorra algum erro ao tentar acessar algum processo
                print("Não foi possível enviar para o nó ", self.node) 
                return False

            if not send_block_for_all_nodes.found_nonce:
                send_block_for_all_nodes.found_nonce = True
                nonce = retorno
                #print("O nó ", self.no, " encontrou o nonce primeiro: ", str(send_block_for_all_nodes.found_nonce))

                stdoutmutex = threading.Lock()
                threads = []
                for node in nodes:
                    #if no != current: # verifica se o objeto não tem o mesmo nome do objeto current    
                    thread = send_block_for_all_nodes(nonce, node, stdoutmutex)
                    thread.start() # método da classe pai, dar iniciar a thread, vai criar operações básicas para poder usar 
                    threads.append(thread)
                #send_block_for_all_nodes.found_nonce = False
                print("O nó ", self.node, " encontrou o nonce primeiro: ", str(retorno))
           
            print("O nó ", self.node, " encontrou o nonce: ", str(retorno))

    print('Saindo da Thread Principal')

class send_nonce_for_all_nodes(threading.Thread): # enviar nonce de um block para os outros nós da rede, um em cada thread
    def __init__(self, nonce, node, mutex):
        self.nonce = nonce
        self.node = node
        self.mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        #with self.mutex: # para evitar que mais de uma thread use o print ao mesmo tempo   
            try:
                ns = Pyro4.locateNS() # localizando o servidor de nomes
            except Pyro4.errors.NamingError: # caso o servidor de nomes não esteja sendo executado
                print("Falha para localizar o servidor de nomes! - Execute o servidor de nomes (pyro4-ns)")
                exit()
            try:
                uri = ns.lookup(self.node) # obtendo a uri do objeto remoto
                o = Pyro4.Proxy(uri) #pegando o objeto remoto

                print("enviado nonce para o nó ", self.node) # printando o nó da rede

                retorno = o.check_nonce(self.nonce) # enviando o nonce para verificalção
            except: # caso não consiga acessar o processo
                print("Não foi possível enviar para o nó ", self.node)
                return False

            print("O nó ", self.node, " retornou o STATUS: ", str(retorno))
            send_block_for_all_nodes.found_nonce = False
            
    print('Saindo da Thread Principal')


#primeiramente deve ser definido o block
class Block(): # classe utilizada para a criação e manipulação de cada block de forma individual
    #construtor do block
    def __init__(self, index=0, data='{"Genesis Block":"Genesis Block"}', prevhash='{"Genesis Block":"Genesis Block"}', nonce=0): #quando não temos um block anterior, definimos ele como uma string vazia (valor default)
        #variáveis da classe
        self.index=index # index do block
        self.nonce=nonce # resposta do desafio para minerar o block
        self.tstamp=str(datetime.datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime("%s")) # quando o block foi criado, para poder realizar comparações posteriores         self.data=data # data que serão armazenados em formato JSON no block
        self.data=data
        self.prevhash=prevhash # hash do block anterior
        self.hash=self.calc_hash() # hash do block current 

    #função responsável por realizar o cálculo do hash do block
    def calc_hash(self):
        #criando um dicionário com json, passando parâmetro por parâmetro, por fim, codificando para gerar o hash posteriormente
        #block_string=json.dumps({"index":self.index, "nonce":self.nonce, "tstamp":self.tstamp, "data":self.data, "prevhash":self.prevhash}).encode()
        block_string = str(self.index) + str(self.nonce) + str(self.tstamp) + str(self.data) + str(self.prevhash)
        #block_string = "" + str(self.nonce)
        block_string = block_string.encode()
        #retornando o hash do block
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, diffic, nonce=-1): # método utilizado para encontrar um hash com um determinado número de zeros no início (dificuldade)
        self.nonce = nonce
        if self.nonce == -1: # se o nonce não tiver sido passado como parâmetro
            self.nonce = 0
            while(self.hash[:diffic] != str('').zfill(diffic)): # enquanto a o inicio do hash do block até a dificuldade -1 não for igual a uma string que tenha o mesmo números de zeros que a dificuldade
                self.nonce += 1 # incrementando o nonce para gerar um novo hash do block (também pode ser realizado de forma aleatória)
                self.hash=self.calc_hash() # gerando um novo hash para o block 
            print("block Minerado! - ", self.hash)
            return True
        else:
            self.hash=self.calc_hash() # gera o hash do block com o nonce informado
            if self.hash[:diffic] == str('').zfill(diffic): # se tiver suprido o desafio é retornado True caso contrário false
                print("block Minerado com nonce informado! - ", self.hash)
                return True
        return False
    
    # método para retornar informações do block
    def __str__(self):
        block = "------------------------------" 
        block += "\nindex: " + str(self.index) 
        block += "\nnonce: " + str(self.nonce)
        block += "\ntstamp: " + str(self.tstamp)
        block += "\n\n ---> data"
        block += "\n" + str(self.data)
        block += "\n <--- \n"
        block += "\nprev_hash: " + str(self.prevhash)
        block += "\nhash: " + str(self.hash)
        block += "\n------------------------------"
        return block


@Pyro4.expose
# após criar a classe referente aos blocks, deve ser criado a classe que vai representar a cadeia de blocks
class Blockchain(): #classe que será utilizada para armazenar e gerenciar a cadeia de blocks
    def __init__(self): #função construct da classe
        self.difficulty=3 # definindo a dificuldade da mineração - quanto maior o valor, mais tempo para minerar
        self.unconfirmed_transactions = []
        self.chain=[self.genereta_genesis_block(),] #criando a lista que será utilizada para armazenar os blocks, além de adicionar o block gênesis

    def genereta_genesis_block(self): #método para a criação de um block gênesis
        block = Block(0)
        block.tstamp = 0 # modificando o tstamp para que todos os blocks da rede tenham o mesmo block gênesis
        block.mine_block(self.difficulty) # pois foi alterado na linha anterior
        return block #retorna um block gênesis
    
    def get_last_block(self): #método para obter o último block da cadeia
        return self.chain[-1] #pega o último elemento da lista
    
    def add_block(self, newBlock): #adicionar novo block na cadeia, passando o novo block como parâmetro
        newBlock.prevhash=self.get_last_block().hash # definindo o atributo 'prevhash' como o hash do último block da cadeia de blocks
        newBlock.mine_block(self.difficulty) #calculando o hash do novo block
        self.chain.append(newBlock) #adicionando o block novo na chain (lista da classe Blockchain)
        print(self.get_chain())
    
    def is_chain_valid(self): # Método para verificar de a cadeia de blocks é válida
        for i in range(1, len(self.chain)): # varrendo os blocks da lista, exceto o block gênesis
            prevb=self.chain[i-1] #pegando o block anterior da lista (i - 1)
            currb=self.chain[i] #pegando o block current da lista
            if(currb.hash != currb.calc_hash()): # realizando o cálculo do hash do block current para verificar se algum dado do block foi alterado, caso tenha sido alterado fazendo com que o hash não seja igual ao original, é retornado False
                print("inconsistência no block")
                return "inconsistência no block" # retorna falso caso algum valor do block tenha sido alterado
            if(currb.prevhash != prevb.hash): # verifica se a ligação com o block anterior ainda é válida, ou seja, se o campo prevhash do block current, é igual ao campo hash do block anterior
                print("inconsistência na chain")
                return "inconsistência na chain" # se os hashes forem diferente, é retornado falso
        return True

    def synchronized(func):
        #print(type(func))
        func.__lock__ = threading.Lock()
            
        def synced_func(*args, **kws):
            with func.__lock__:
                #print("tipo: ", type(func(*args, **kws)))
                return func(*args, **kws)
        
        return synced_func
    
    @synchronized
    def create_block(self, objJson):
        index = len(self.chain)
        try:
            d = json.loads(objJson) # tentando converter o objeto passado como parâmetro para um objeto python
        except json.decoder.JSONDecodeError: # caso o tipo de dado informado não possa ser convertido para json, vai ser retornado False 
            print("Não foi possível criar um block, pois o tipo de dado informado não é válido")
            return False

        block = Block() # criando um block 
        block.index = index
        block.data = objJson
        self.send_block_for_all_nodes(block) # adicionando o block na chain
        return True
    
    def get_chain(self):
        result = ""
        for block in self.chain: #varrer a cadeia de blocks
            result+="\n------------------------------\n"
            result+="           block " + str(block.index) + "\n"
            result+=block.__str__() + "\n" # mostrando as informações do respectivo block
        result+="STATUS da Chain: " + str(self.is_chain_valid()) + "\n"
        return result
    
    def get_chain_json(self):
        lista = []
        for block in self.chain:
            lista.append({"index":block.index, "nonce":block.nonce, "tstamp":block.tstamp, "data":block.data, "prevhash":block.prevhash, "hash":block.hash})
        return json.dumps(lista)

    def get_chain_size(self): # obter o tamanho da cadeia de blocks sem contar o block gênesis
        return len(self.chain)-1


    #############################################
    # MÉTODOS PARA APLICAR DE FORMA DISTRIBUÍDA # 
    #############################################
    @synchronized
    def send_block_for_all_nodes(self, block): # chamada remota para os outros nós da rede em diferentes threads
        stdoutmutex = threading.Lock()
        threads = []

        b = {"index":block.index, "nonce":block.nonce, "tstamp":block.tstamp, "data":block.data, "prevhash":block.prevhash, "hash":block.hash}
        bb = json.dumps(b)
        self.consensus(bb)

        for node in nodes: # enviando o block para os nós
            if node != current: # verifica se o objeto não tem o mesmo nome do objeto current    
                thread = send_block_for_all_nodes(block, node, stdoutmutex)
                thread.start() # método da classe pai, dar iniciar a thread, vai criar operações básicas para poder usar 
                threads.append(thread)
        print("enviou o block para os nós...")

        return True
    
    def add_new_transaction(self, block):
        self.unconfirmed_transactions.append(block)
        return True

    def get_last_tstamp_transaction(self):
        if len(self.unconfirmed_transactions) > 0: # verifica de a lista de transações não está vazia
            return int(self.unconfirmed_transactions[-1].tstamp) # retorna o último elemento
        return 0

    @synchronized
    def consensus(self, block):

        b = json.loads(block) # transformando o block enviado para algum formato em python, neste caso dict

        index = len(self.chain) # obtendo o index do block
        block = Block(index, b["data"]) # criando um block passando os data recebidos de outro nó da rede

        block.tstamp = b["tstamp"] #  colocando o tstamp como tstamp que ele foi enviado para o primeiro block

        if len(self.unconfirmed_transactions) > 0:
            block.prevhash=self.unconfirmed_transactions[-1] # pegando o hash do último block da lista de blocks não confirmados
            block.index = len(self.chain) + len(self.unconfirmed_transactions)
        else:
            block.prevhash=self.get_last_block().hash # pegando o hash do block anterior
    
        block.mine_block(self.difficulty) # minerando o block para encontrar o nonce para o desafio, assim será setado o valor o nonce e do hash do block
        
        print(block.__str__())

        novo = True
        for b in self.unconfirmed_transactions: # verifica se não tem nenhum block que foi criado posteriormente, ou junto ao block current, assim evitando que se um block for recebido mais de uma vez ele não seja adicionado, além de manter a ordem da cadeia de blocks 
            if int(b.tstamp) <= int(block.tstamp): # caso o block tenha sido criado junto com algum dos blocks
                if b.hash == block.hash: # caso seja o mesmo block, então ele não é um block novo
                    novo = False
        
        if int(block.tstamp) == int(self.get_last_block().tstamp) and novo: # verifica se o block foi criado junto com o último block da cadeia
            if block.hash != self.get_last_block().hash: # caso tenha sido criado no mesmo momento, porém não seja o mesmo block 
                self.add_new_transaction(block) # adicionando o block na lista de blocks não confirmados
        elif int(block.tstamp) > int(self.get_last_block().tstamp) and novo: # garante que o block adicionado seja um block novo
            self.add_new_transaction(block) # adicionando o block na lista de blocks não confirmados
        

        print(block.data)
        print("nonce encontrado: ", block.nonce) # printando o nonce encontrado

        #print(self.get_chain())

        #print(block.__str__())

        print(self.is_chain_valid())

        return block.nonce # retornando o nonce encontrado para os nós da rede 

    @synchronized
    def check_nonce(self, nonce): # Função para verificar o nonce informado e adicionar o block na chain
        print("Nonce recebido: ", str(nonce))
        for block_n_confirmado in self.unconfirmed_transactions:
            block_n_confirmado.nonce = nonce
            if block_n_confirmado.mine_block(self.difficulty, nonce): # verifica se o nonce informado está correto 
                self.chain.append(block_n_confirmado)
                #print(self.get_chain())
                self.unconfirmed_transactions.remove(block_n_confirmado)

                return True # se sim, retorna verdadeiro
        return False # caso contrário, retorna falso

    def compare_chains(self):
        try:
            ns = Pyro4.locateNS() # localizando o servidor de nomes
        except Pyro4.errors.NamingError: # caso o servidor de nomes não esteja sendo executado
            print("Falha para localizar o servidor de nomes! - Execute o servidor de nomes (pyro4-ns)")
            exit()
        
        total = 1 # para contar com o próprio processo na porcentagem total
        n_elementos = 1 # para contar com o próprio processo na porcentagem total
        for no in nodes: #percorrendo a lista de processos
            if not no == current:
                try:
                    uri = ns.lookup(no) # obtendo a uri do objeto remoto
                    o = Pyro4.Proxy(uri) #pegando o objeto remoto
                    if o.get_chain_size() == self.get_chain_size():
                        if o.get_chain() == self.get_chain(): # se as cadeias forem iguai
                            total += 1 # soma 1 no somatótio total
                            n_elementos += 1 # incremaneta o número de elementos somados
                        else:
                            total += 0 # soma zero no somatório  total
                            n_elementos += 1
                    
                    # Os dois próximos elifs são para dar uma tolerância de atraso de um block nas chain, ele vai verificar a diferença entre os tamanhos da chains
                    elif (o.get_chain_size() - self.get_chain_size()) == 1: # se a chain REMOTA for um block maior do que a chain LOCAL, tendo 1 como tolerância de atraso na rede
                        r = o.get_chain_json()
                        objR = json.loads(r)
                        del objR[-1] # removendo o block que está sobrando na comparação
                        teste = True
                        for x in len(self.get_chain_size):
                            if not self.chain[x].hash == objR[x].hash: # caso em alguma posição da chain, as duas chain não estejam iguais
                                total += 0 # soma zero no somatório  total
                                n_elementos += 1
                            else:                                
                                total += 1 # soma 1 no somatótio total
                                n_elementos += 1
                        
                        
                    elif (self.get_chain_size() - o.get_chain_size()) == 1: # se a chain LOCAL for um block maior do que a chain REMOTA, tendo 1 como tolerância de atraso na rede
                        objL = self.chain
                        del objL[-1] # removendo o block que está sobrando na comparação
                        teste = True
                        for x in len(self.get_chain_size):
                            if not objL.chain[x].hash == objR[x].hash: # caso em alguma posição da chain, as duas chain não estejam iguais
                                total += 0 # soma zero no somatório  total
                                n_elementos += 1
                            else:
                                total += 1 # soma 1 no somatótio total
                                n_elementos += 1
                    
                    else: # caso a diferença for maior que 1
                        total += 0 # soma zero no somatório  total
                        n_elementos += 1
                        
                except: # caso não consiga se comunicar com o processo da rede, subtrai um do número total de nós, assim evitando que a quantidade total não seja dividida pela quantidade errada de elementos, ocasionando em uma porcentagem errada
                    print("Não foi possível acessar o nó", no)
        porcentagem = (total * 100)/n_elementos
        print("Pocentagem de nós com a mesma chain: ", porcentagem)
        return porcentagem # retorna a porcentagem de processos que tem a chain igual a do processo current


# para adicionar um block da forma original, pode ser considerado muito fácil, porém se for muito fácil adiconar um novo block
# um hacker poderia alterar toda a cadeia de block de forma fácil, para evitar esse tipo de problema, são utilizados
# alguns algoritmos de consendo (probabilístico), como por exemplo o Proof of Work (PoW), o PoW torna a adição de um block 
# na chain uma tarefa difícil, por exemplo no Bitcoin que é apenas aceitos os hashes que começam com um específico 
# número de zeros, além do mesmo ter de ser realizado dentro de um tempo limite (encontrar um nonce adequado para ganhar o desafio)
# então um block será adicionado a cada 10 minutos
# a quantidade de números zeros no início dos hashes é chamada de dificuldade, então se tiver apenas 1 zero a dificuldade 
# será 1, se tiver dois zeros, a dificuldade será 2, etc.
# Como a técnologia de processamento está sempre evoluindo o bitcoin, tem sua dificuldade aumentada a cada 2 ou 3 anodes.
# o processo de encontrar um certo número de zeros no início do hash do block, é chamado de minerar.

#daemon = Pyro4.Daemon("192.168.56.1")
daemon = Pyro4.Daemon()

blockchain=Blockchain() # passando o objeto já isntânciado para manter os data salvos de um acesso a outro do objeto remoto
uri = daemon.register(blockchain) #instanciando um objeto remoto, realizando o registrando dele. Vai ser retornando#

#print(dir(daemon))

# uma URI do objeto para ele poder ser acessado, o método também vai checar se já não há um objeto registrado

# para poder utilizar deve estar sendo executado o pyro-ns em um terminal
ns = Pyro4.locateNS() # Get a proxy for a name server somewhere in the network.
ns.register('b2', uri) # simplificando o nome do objeto

print(uri)

daemon.requestLoop()

