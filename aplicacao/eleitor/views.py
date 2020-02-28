from django.shortcuts import render, redirect, get_object_or_404
from eleicoes.models import Eleicao, Eleicao_eleitor
from usuarios.models import Usuario

def index(request): #quando for solicitado o url index, será encaminhado o index.html
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Eleitor' # Definir título da página
    context = {
        'title': title,
    }
    return render(request, 'eleitor/index.html', context)

def consulta(request): #quando for solicitado o url index, será encaminhado o index.html
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Consulta' # Definir título da página
    pk = request.session.get('user_pk')
    #print(pk)
    usuario = get_object_or_404(Usuario, pk=pk) # realizar a instância do objeto que corresponde ao usuário logado
    #print(usuario.nome + " " + usuario.sobrenome)
    if usuario.tipo == "Eleitor": # testa se o usuário é eleitor ou não 
        eleicoes_eleitor = Eleicao_eleitor.objects.filter(eleitor__pk=pk) #
        context = {
            'title': title,
            'eleicoes_eleitor': eleicoes_eleitor,
        }
        return render(request, 'eleitor/consulta.html', context) 

    erro="Só eleitores tem permissão de acessar esta página!"
    context = {
        'title': title,
        'erro': erro
    } 

    return render(request, 'eleitor/consulta.html', context) #retorna mensagem de erro, pois o candidato não tem o direito de votar

def votacao(request, pk): # Realização do voto 
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    
    return render(request, 'eleitor/votacao.html') 
    # deve ser direcionado para uma página para selecionar o respectivo candidato da respectiva eleição

    
