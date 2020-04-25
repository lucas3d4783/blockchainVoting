from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
 
texto = "texto a encriptar"

# Você deve usar a melhor fonte de dados aleatórios que tiver à
# disposição. Pra manter o exemplo mais portável, usaremos o
# RandomPool do próprio PyCrypto:
 
pool = RandomPool(384)
pool.stir()

# randfunc(n) deve retornar uma string de dados aleatórios de
# comprimento n, no caso de RandomPool, o método get_bytes
randfunc = pool.get_bytes

# Se tiver uma fonte segura (como /dev/urandom em sistemas unix), ela
# deve ser usada ao invés de RandomPool

# pool = open("/dev/urandom")
# randfunc = pool.read
 
# Tamanho da chave, em bits
N = 1024
 
# O algoritmo RSA usado aqui não utiliza K, que pode ser uma string
# nula.
K = ""

# Geramos a chave (contendo a chave pública e privada):
key = RSA.generate(N, randfunc)

# Criptografamos o texto com a chave:
enc = key.encrypt(texto, K)
 
# Podemos decriptografar usando a chave:
dec = key.decrypt(enc)

# Separando apenas a chave pública:
pub_key = key.publickey()
 
# Criptografando com a chave pública:
enc = pub_key.encrypt(texto, K)

# Decriptografando com a chave privada:
dec = key.decrypt(enc)

# As informações da chave são compostas de seis atributos: 'n', 'e',
# 'd', 'p', 'q' e 'u'. Se quiser armazenar ou enviar uma chave você
# pode usar pickle ou simplesmente usar esses atributos com o método
# construct. Por exemplo:

# Os atributos 'n' e 'e' correspondem à chave pública:
n, e = key.n, key.e

# E recriamos a chave pública com esses dados:
pub_key = RSA.construct((n, e))