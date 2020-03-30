import Pyro4 # importando biblioteca

ns = Pyro4.locateNS() # localizando o servidor de nomes
uri = ns.lookup('obj') # obtendo a uri do objeto remoto
o = Pyro4.Proxy(uri) #pegando o objeto remoto

#geração de uma chain para teste
o.criarBloco(1,2,3) #criando bloco
o.criarBloco(4,5,6) #criando bloco
print(o.getChain())
print("Quantidade de Votos: ", o.get_chain_size())



#print("Estado do sistema: ", o.getChain()) # chamando um método do objeto remoto