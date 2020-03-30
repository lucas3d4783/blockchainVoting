import Pyro4

chain = Pyro4.Proxy("PYRO:obj_4a28db319d364a198fb4f6e01f08cc80@localhost:34773")

chain.get_genesis_block()
#percorrendo os blocos da chain
for bloco in chain.blocks:
    print("------------------ BLOCO "+str(bloco.index)+" ------------------")
    print("INDEX: "+str(bloco.index))
    print("TIMESTAMP: "+str(bloco.timestamp))
    print("DADOS: "+str(bloco.data))
    print("HASH DO BLOCO ANTERIOR: "+str(bloco.previous_hash))
    print("HASH DO BLOCO: "+str(bloco.hash))
    print("---------------------------------------------\n")
