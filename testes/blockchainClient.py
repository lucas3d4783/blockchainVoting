import Pyro4 # importando biblioteca

ns = Pyro4.locateNS() # localizando o servidor de nomes
uri = ns.lookup('obj') # obtendo a uri do objeto remoto

o = Pyro4.Proxy(uri) #pegando o objeto remoto


#geração de uma chain para teste
o.criarBloco(1, '19/03/2020', 100) #criando bloco
o.criarBloco(2, '19/03/2020', 100) #criando bloco
print(o.getChain())

#print("Estado do sistema: ", o.getChain()) # chamando um método do objeto remoto