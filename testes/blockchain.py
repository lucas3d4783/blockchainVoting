import hashlib
import json
import datetime
import Pyro4 #biblioteca para a utilização de objetos remotos
from pytz import timezone
import threading

class Voto(): #objeto que deve funcionar como uma matriz dinâmica para armazenar os votos
    def __init__(self, eleicao_pk, candidato_pk):
        self.eleicao_pk=eleicao_pk
        self.candidato_pk=candidato_pk
        self.votos=1


#primeiramente deve ser definido o bloco
class Block(): # classe utilizada para a criação e manipulação de cada bloco de forma individual
    #construtor do bloco
    def __init__(self, index=0, eleicao_pk=-1, eleitor_pk=-1, candidato_pk=-1, prevhash='Genesis Block', nonce=0): #quando não temos um bloco anterior, definimos ele como uma string vazia (valor default)
        #variáveis da classe
        self.index=index
        self.nonce=nonce
        self.tstamp=str(datetime.datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime("%d/%b/%Y-%H:%M:%S"))
        self.eleicao_pk=eleicao_pk
        self.eleitor_pk=eleitor_pk
        self.candidato_pk=candidato_pk
        self.prevhash=prevhash
        self.hash=self.calcHash()

    #função responsável por realizar o cálculo do hash do bloco
    def calcHash(self):
        #criando um dicionário com json, passando parâmetro por parâmetro, por fim, codificando para gerar o hash posteriormente
        block_string=json.dumps({"index":self.index, "nonce":self.nonce, "tstamp":self.tstamp, "eleicao_pk":self.eleicao_pk, "eleitor_pk":self.eleitor_pk, "candidato_pk":self.candidato_pk, "prevhash":self.prevhash,}, sort_keys=True, ).encode()
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
        bloco += "\neleição_pk: " + str(self.eleicao_pk)
        bloco += "\neleitor_pk: " + str(self.eleitor_pk)
        bloco += "\ncandidato_pk: " + str(self.candidato_pk)
        bloco += "\nprev_hash: " + str(self.prevhash)
        bloco += "\nhash: " + str(self.hash)
        bloco += "\n------------------------------"
        return bloco

#geração de um bloco para teste
#bblock=Block(1, '19/03/2020', 100)
#print(bblock)


@Pyro4.expose
# após criar a classe referente aos blocos, deve ser criado a classe que vai representar a cadeia de blocos
class Blockchain(): #classe que será utilizada para armazenar e gerenciar a cadeia de blocos
    def __init__(self): #função construct da classe
        self.chain=[self.generateGenesisBlock(),] #criando a lista que será utilizada para armazenar os blocos, além de adicionar o bloco gênesis
        self.difficulty=4 # definindo a dificuldade da mineração - quanto maior o valor, mais tempo para minerar
        self.listaDeVotos = [] #criando um novo arrai para armazenar o somatório dos votos
    
    def generateGenesisBlock(self): #método para a criação de um bloco gênesis
        return Block(0, 'Genesis Block', 'Genesis Block', 'Genesis Block') #retorna um bloco gênesis
    
    def getLastBlock(self): #método para obter o último bloco da cadeia
        return self.chain[-1] #pega o último elemento da lista
    
    def addBlock(self, newBlock): #adicionar novo bloco na cadeia, passando o novo bloco como parâmetro
        newBlock.prevhash=self.getLastBlock().hash # definindo o atributo 'prevhash' como o hash do último bloco da cadeia de blocos
        newBlock.mineBlock(self.difficulty) #calculando o hash do novo bloco
        #newBlock.hash=newBlock.calcHash() #calculando o hash do novo bloco
        #aplicar semaforos no método
        self.chain.append(newBlock) #adicionando o bloco novo na chain (lista da classe Blockchain)
    
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
    def criarBloco(self, eleicao_pk, eleitor_pk, candidato_pk):
        index = len(self.chain)
        bloco = Block(index, eleicao_pk, eleitor_pk, candidato_pk) # criando um bloco 
        #fazer o lock na chain
        #fazer ficar esperando 
        self.addBlock(bloco) # adicionando o bloco na chain
        self.incrementarVotos(eleicao_pk, candidato_pk)
        return True;
    
    @synchronized
    def incrementarVotos(self, eleicao_pk, candidato_pk):
        achou=False
        for i in range(0,len(self.listaDeVotos)): 
            print("Percorrendo a lista de votos ...")
            if (str(self.listaDeVotos[i].eleicao_pk) == str(eleicao_pk)) and (str(self.listaDeVotos[i].candidato_pk) == str(candidato_pk)): 
                print("Achou, incrementando o valor atual do campo votos ...")
                self.listaDeVotos[i].votos+=1
                print(self.listaDeVotos[i].votos)
                achou=True
        if not achou:
            print("Não achou, criando um novo objeto de voto com o valor do campo votos igual a 1 ... ")
            voto = Voto(eleicao_pk, candidato_pk)
            self.listaDeVotos.append(voto)

        return True;

    def getChain(self):
        count = 0 # criando um contador para os blocos
        result = "";
        for bloco in self.chain: #varrer a cadeia de blocos
            result+="\n------------------------------\n"
            result+="           BLOCO " + str(bloco.index) + "\n"
            result+=bloco.__str__() # mostrando as informações do respectivo bloco
            count+=1 # incrementando o contador de blocos
        return result;
        #print("Estado do sistema: ", self.isChainValid()) #verifica a integridade dos blocos e da chain
    
    def get_chain_size(self): # obter o tamanho da cadeia de blocos sem contar o bloco gênesis
        return len(self.chain)-1
    
    def verificaSeJaVotou(self, eleicao_pk, eleitor_pk):
        for bloco in self.chain:
            if (str(bloco.eleitor_pk) == str(eleitor_pk)) and (str(bloco.eleicao_pk) == str(eleicao_pk)):
                return True
        return False
    

#geração de uma blockchain para teste
#blockchain=Blockchain() #criando uma cadeia de votos
#blockchain.addBlock(Block(1, '19/03/2020', 100)) #criando bloco
#blockchain.addBlock(Block(2, '19/03/2020', 50)) #criando bloco
#blockchain.addBlock(Block(3, '19/03/2020', 25)) #criando bloco

#alteração de um bloco -> causando uma inconsistência em um bloco
#blockchain.chain[2].transaction = 5000

#alteração do hash da do bloco para fazer com que o bloco seja válido, porém como o próximo bloco possui o hash do bloco atual, a chain vai se tornar inválida, fazendo com que tenha que ser gerado novos hashes para todos os blocos seguintes ao bloco alterado
#blockchain.chain[2].hash = blockchain.chain[2].calcHash()

#count = 0 # criando um contador para os blocos
#for bloco in blockchain.chain: #varrer a cadeia de blocos
#    print("------------------------------")
#    print("           BLOCO", str(count))
#    print(bloco) # mostrando as informações do respectivo bloco
#    count+=1 # incrementando o contador de blocos

#print("Estado do sistema: ", blockchain.isChainValid()) #verifica a integridade dos blocos e da chain

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
ns.register('obj', uri) # simplificando o nome do objeto

print(uri)

daemon.requestLoop()

