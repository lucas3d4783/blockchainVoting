import threading

class Minhathread(threading.Thread):
    def __init__(self, meuId, cont, mutex):
        self.meuId = meuId
        self.cont = cont
        self.mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        for i in range(self.cont):
            with self.mutex: # para evitar que mais de uma thread use o print ao mesmo tempo
                print('[%s]  => %s' % (self.meuId, i))

stdoutmutex = threading.Lock()
threads = []

for i in range(10):
    thread = Minhathread(i, 100, stdoutmutex)
    thread.start() # método da classe pai, dar iniciar a thread, vai criar operações básicas para poder usar 
    threads.append(thread)

for thread in threads:
    print('executando a Thread')
    thread.join() # método da classe pai, este método espera até a threading terminar quando ela teminar ele executa o print
    

print('saindo da Thread principal')