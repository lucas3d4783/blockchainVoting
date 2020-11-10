# -*- coding: utf-8 -*-

import hashlib
import json
import datetime
import Pyro4 #biblioteca para a utilização de objetos remotos
from pytz import timezone
import threading
import pickle

atual = 'b2' # nó atual
nos = ['b1', 'b2', 'b3', 'b4'] # lista de blocos do sistema

class Envia_bloco_para_todos_os_nos(threading.Thread): # enviar bloco para os outros nós da rede, um em cada thread
    achou_nonce = False
    nonce = 0
    def __init__(self, bloco, no, mutex):
        self.bloco = bloco
        self.no = no
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
                uri = ns.lookup(self.no) # obtendo a uri do objeto remoto
                o = Pyro4.Proxy(uri) #pegando o objeto remoto

                b = {"index":self.bloco.index, "nonce":self.bloco.nonce, "tstamp":self.bloco.tstamp, "dados":self.bloco.dados, "prevhash":self.bloco.prevhash, "hash":self.bloco.hash}
                bloco = json.dumps(b)

                print("Enviado bloco para o nó ", self.no) # printando qual bloco está sendo enviado para qual nó da rede 

                retorno = o.consensus(bloco) # enviando o bloco serelizado para objeto remoto minerar 
            except: # caso ocorra algum erro ao tentar acessar algum processo
                print("Não foi possível enviar para o nó ", self.no) 
                return False

            if not Envia_bloco_para_todos_os_nos.achou_nonce:
                Envia_bloco_para_todos_os_nos.achou_nonce = True
                nonce = retorno
                #print("O nó ", self.no, " encontrou o nonce primeiro: ", str(Envia_bloco_para_todos_os_nos.achou_nonce))

                stdoutmutex = threading.Lock()
                threads = []
                for no in nos:
                    #if no != atual: # verifica se o objeto não tem o mesmo nome do objeto atual    
                    thread = Envia_nonce_para_todos_os_nos(nonce, no, stdoutmutex)
                    thread.start() # método da classe pai, dar iniciar a thread, vai criar operações básicas para poder usar 
                    threads.append(thread)
                #Envia_bloco_para_todos_os_nos.achou_nonce = False
                print("O nó ", self.no, " encontrou o nonce primeiro: ", str(retorno))
           
            print("O nó ", self.no, " encontrou o nonce: ", str(retorno))

    print('Saindo da Thread Principal')

class Envia_nonce_para_todos_os_nos(threading.Thread): # enviar nonce de um bloco para os outros nós da rede, um em cada thread
    def __init__(self, nonce, no, mutex):
        self.nonce = nonce
        self.no = no
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
                uri = ns.lookup(self.no) # obtendo a uri do objeto remoto
                o = Pyro4.Proxy(uri) #pegando o objeto remoto

                print("enviado nonce para o nó ", self.no) # printando o nó da rede

                retorno = o.verify_nonce(self.nonce) # enviando o nonce para verificalção
            except: # caso não consiga acessar o processo
                print("Não foi possível enviar para o nó ", self.no)
                return False

            print("O nó ", self.no, " retornou o STATUS: ", str(retorno))
            Envia_bloco_para_todos_os_nos.achou_nonce = False
            
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
        self.hash=self.calc_hash() # hash do bloco atual 

    #função responsável por realizar o cálculo do hash do bloco
    def calc_hash(self):
        #criando um dicionário com json, passando parâmetro por parâmetro, por fim, codificando para gerar o hash posteriormente
        #block_string=json.dumps({"index":self.index, "nonce":self.nonce, "tstamp":self.tstamp, "dados":self.dados, "prevhash":self.prevhash}).encode()
        block_string = str(self.index) + str(self.nonce) + str(self.tstamp) + str(self.dados) + str(self.prevhash)
        #block_string = "" + str(self.nonce)
        block_string = block_string.encode()
        #retornando o hash do bloco
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, diffic, nonce=-1): # método utilizado para encontrar um hash com um determinado número de zeros no início (dificuldade)
        self.nonce = nonce
        if self.nonce == -1: # se o nonce não tiver sido passado como parâmetro
            self.nonce = 0
            while(self.hash[:diffic] != str('').zfill(diffic)): # enquanto a o inicio do hash do bloco até a dificuldade -1 não for igual a uma string que tenha o mesmo números de zeros que a dificuldade
                self.nonce += 1 # incrementando o nonce para gerar um novo hash do bloco (também pode ser realizado de forma aleatória)
                self.hash=self.calc_hash() # gerando um novo hash para o bloco 
            print("Bloco Minerado! - ", self.hash)
            return True
        else:
            self.hash=self.calc_hash() # gera o hash do bloco com o nonce informado
            if self.hash[:diffic] == str('').zfill(diffic): # se tiver suprido o desafio é retornado True caso contrário false
                print("Bloco Minerado com nonce informado! - ", self.hash)
                return True
        return False
    
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
        self.difficulty=3 # definindo a dificuldade da mineração - quanto maior o valor, mais tempo para minerar
        self.unconfirmed_transactions = []
        self.chain=[self.generate_genesis_block(),] #criando a lista que será utilizada para armazenar os blocos, além de adicionar o bloco gênesis

    def generate_genesis_block(self): #método para a criação de um bloco gênesis
        bloco = Block(0)
        bloco.tstamp = 0 # modificando o tstamp para que todos os blocos da rede tenham o mesmo bloco gênesis
        bloco.mine_block(self.difficulty) # pois foi alterado na linha anterior
        return bloco #retorna um bloco gênesis
    
    def get_last_block(self): #método para obter o último bloco da cadeia
        return self.chain[-1] #pega o último elemento da lista
    
    def add_block(self, newBlock): #adicionar novo bloco na cadeia, passando o novo bloco como parâmetro
        newBlock.prevhash=self.get_last_block().hash # definindo o atributo 'prevhash' como o hash do último bloco da cadeia de blocos
        newBlock.mine_block(self.difficulty) #calculando o hash do novo bloco
        self.chain.append(newBlock) #adicionando o bloco novo na chain (lista da classe Blockchain)
        print(self.get_chain())
    
    def is_chain_valid(self): # Método para verificar de a cadeia de blocos é válida
        for i in range(1, len(self.chain)): # varrendo os blocos da lista, exceto o bloco gênesis
            prevb=self.chain[i-1] #pegando o bloco anterior da lista (i - 1)
            currb=self.chain[i] #pegando o bloco atual da lista
            if(currb.hash != currb.calc_hash()): # realizando o cálculo do hash do bloco atual para verificar se algum dado do bloco foi alterado, caso tenha sido alterado fazendo com que o hash não seja igual ao original, é retornado False
                print("inconsistência no bloco")
                return "inconsistência no bloco" # retorna falso caso algum valor do bloco tenha sido alterado
            if(currb.prevhash != prevb.hash): # verifica se a ligação com o bloco anterior ainda é válida, ou seja, se o campo prevhash do bloco atual, é igual ao campo hash do bloco anterior
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
            print("Não foi possível criar um bloco, pois o tipo de dado informado não é válido")
            return False

        bloco = Block() # criando um bloco 
        bloco.index = index
        bloco.dados = objJson
        self.enviar_bloco_para_os_nos(bloco) # adicionando o bloco na chain
        return True
    
    def get_chain(self):
        result = ""
        for bloco in self.chain: #varrer a cadeia de blocos
            result+="\n------------------------------\n"
            result+="           BLOCO " + str(bloco.index) + "\n"
            result+=bloco.__str__() + "\n" # mostrando as informações do respectivo bloco
        result+="STATUS da Chain: " + str(self.is_chain_valid()) + "\n"
        return result
    
    def get_chain_json(self):
        lista = []
        for bloco in self.chain:
            lista.append({"index":bloco.index, "nonce":bloco.nonce, "tstamp":bloco.tstamp, "dados":bloco.dados, "prevhash":bloco.prevhash, "hash":bloco.hash})
        return json.dumps(lista)

    def get_chain_size(self): # obter o tamanho da cadeia de blocos sem contar o bloco gênesis
        return len(self.chain)-1


    #############################################
    # MÉTODOS PARA APLICAR DE FORMA DISTRIBUÍDA # 
    #############################################
    @synchronized
    def enviar_bloco_para_os_nos(self, bloco): # chamada remota para os outros nós da rede em diferentes threads
        stdoutmutex = threading.Lock()
        threads = []

        b = {"index":bloco.index, "nonce":bloco.nonce, "tstamp":bloco.tstamp, "dados":bloco.dados, "prevhash":bloco.prevhash, "hash":bloco.hash}
        bb = json.dumps(b)
        self.consensus(bb)

        for no in nos: # enviando o bloco para os nós
            if no != atual: # verifica se o objeto não tem o mesmo nome do objeto atual    
                thread = Envia_bloco_para_todos_os_nos(bloco, no, stdoutmutex)
                thread.start() # método da classe pai, dar iniciar a thread, vai criar operações básicas para poder usar 
                threads.append(thread)
        print("enviou o bloco para os nós...")

        return True
    
    def add_new_transaction(self, bloco):
        self.unconfirmed_transactions.append(bloco)

    def get_last_tstamp_transaction(self):
        if len(self.unconfirmed_transactions) > 0: # verifica de a lista de transações não está vazia
            return int(self.unconfirmed_transactions[-1].tstamp) # retorna o último elemento
        return 0

    @synchronized
    def consensus(self, bloco):

        b = json.loads(bloco) # transformando o bloco enviado para algum formato em python, neste caso dict

        index = len(self.chain) # obtendo o index do bloco
        bloco = Block(index, b["dados"]) # criando um bloco passando os dados recebidos de outro nó da rede

        bloco.tstamp = b["tstamp"] #  colocando o tstamp como tstamp que ele foi enviado para o primeiro bloco

        if len(self.unconfirmed_transactions) > 0:
            bloco.prevhash=self.unconfirmed_transactions[-1] # pegando o hash do último bloco da lista de blocos não confirmados
            bloco.index = len(self.chain) + len(self.unconfirmed_transactions)
        else:
            bloco.prevhash=self.get_last_block().hash # pegando o hash do bloco anterior
    
        bloco.mine_block(self.difficulty) # minerando o bloco para encontrar o nonce para o desafio, assim será setado o valor o nonce e do hash do bloco
        
        print(bloco.__str__())

        novo = True
        for b in self.unconfirmed_transactions: # verifica se não tem nenhum bloco que foi criado posteriormente, ou junto ao bloco atual, assim evitando que se um bloco for recebido mais de uma vez ele não seja adicionado, além de manter a ordem da cadeia de blocos 
            if int(b.tstamp) <= int(bloco.tstamp): # caso o bloco tenha sido criado junto com algum dos blocos
                if b.hash == bloco.hash: # caso seja o mesmo bloco, então ele não é um bloco novo
                    novo = False
        
        if int(bloco.tstamp) == int(self.get_last_block().tstamp) and novo: # verifica se o bloco foi criado junto com o último bloco da cadeia
            if bloco.hash != self.get_last_block().hash: # caso tenha sido criado no mesmo momento, porém não seja o mesmo bloco 
                self.add_new_transaction(bloco) # adicionando o bloco na lista de blocos não confirmados
        elif int(bloco.tstamp) > int(self.get_last_block().tstamp) and novo: # garante que o bloco adicionado seja um bloco novo
            self.add_new_transaction(bloco) # adicionando o bloco na lista de blocos não confirmados
        

        print(bloco.dados)
        print("nonce encontrado: ", bloco.nonce) # printando o nonce encontrado

        #print(self.get_chain())

        #print(bloco.__str__())

        print(self.is_chain_valid())

        return bloco.nonce # retornando o nonce encontrado para os nós da rede 

    @synchronized
    def verify_nonce(self, nonce): # Função para verificar o nonce informado e adicionar o bloco na chain
        print("Nonce recebido: ", str(nonce))
        for bloco_n_confirmado in self.unconfirmed_transactions:
            bloco_n_confirmado.nonce = nonce
            if bloco_n_confirmado.mine_block(self.difficulty, nonce): # verifica se o nonce informado está correto 
                self.chain.append(bloco_n_confirmado)
                #print(self.get_chain())
                self.unconfirmed_transactions.remove(bloco_n_confirmado)

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
        for no in nos: #percorrendo a lista de processos
            if not no == atual:
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
                    
                    # Os dois próximos elifs são para dar uma tolerância de atraso de um bloco nas chain, ele vai verificar a diferença entre os tamanhos da chains
                    elif (o.get_chain_size() - self.get_chain_size()) == 1: # se a chain REMOTA for um bloco maior do que a chain LOCAL, tendo 1 como tolerância de atraso na rede
                        r = o.get_chain_json()
                        objR = json.loads(r)
                        del objR[-1] # removendo o bloco que está sobrando na comparação
                        teste = True
                        for x in len(self.get_chain_size):
                            if not self.chain[x].hash == objR[x].hash: # caso em alguma posição da chain, as duas chain não estejam iguais
                                total += 0 # soma zero no somatório  total
                                n_elementos += 1
                            else:                                
                                total += 1 # soma 1 no somatótio total
                                n_elementos += 1
                        
                        
                    elif (self.get_chain_size() - o.get_chain_size()) == 1: # se a chain LOCAL for um bloco maior do que a chain REMOTA, tendo 1 como tolerância de atraso na rede
                        objL = self.chain
                        del objL[-1] # removendo o bloco que está sobrando na comparação
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
        return porcentagem # retorna a porcentagem de processos que tem a chain igual a do processo atual


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
ns.register('b2', uri) # simplificando o nome do objeto

print(uri)

daemon.requestLoop()

