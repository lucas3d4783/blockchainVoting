from django.shortcuts import render, get_object_or_404, redirect
from .models import Eleicao, Eleicao_candidato, Eleicao_eleitor
from .forms import CadastroForm, EdicaoForm, CadastroFormEleicao_candidatos, CadastroFormEleicao_eleitores
from usuarios.models import Usuario

def index(request): #quando for solicitado o url index, será encaminhado o index.html
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    if request.session.get('user_tipo') != 'Administrador': # se não for administrador
        erro = "Apenas administradores do sistema podem realizar manipulações deste tipo!"
        context = {
            'erro': erro,
        }
        return render(request, 'eleicoes/index.html', context) # mensagem de erro

    title = 'Eleições' # Definir título da página
    context = {
        'title': title,
    }
    return render(request, 'eleicoes/index.html', context)

def cadastro(request): #  Criação de eleições 
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    if request.session.get('user_tipo') != 'Administrador': # se não for administrador
        erro = "Apenas administradores do sistema podem realizar manipulações deste tipo!"
        context = {
            'erro': erro,
        }
        return render(request, 'eleicoes/cadastro.html', context) # mensagem de erro
        
    title = 'Cadastro de Eleições' # Definir título da página
    if request.method == 'POST': # se o formulário foi submetido
        form = CadastroForm(request.POST) # Criar o formulário
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            form.save()
            return redirect('consulta_eleicoes')
    else:
        form = CadastroForm()
    
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form,
        'title': title,
        }
    
    return render(request, 'eleicoes/cadastro.html', context)


def consulta(request): # Listagem das eleições criadas
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    if request.session.get('user_tipo') != 'Administrador': # se não for administrador
        erro = "Apenas administradores do sistema podem realizar manipulações deste tipo!"
        context = {
            'erro': erro,
        }
        return render(request, 'eleicoes/consulta.html', context) # mensagem de erro
        
    title = 'Consulta de Eleições' # Definir título da página
    eleicoes = Eleicao.objects.filter().order_by('nome') #buscar as eleições no banco e ordenar pelo nome
    context =  {
        'eleicoes': eleicoes,
        'title': title,
        }
    return render(request, 'eleicoes/consulta.html', context) #chamar o template de consulta, passando a lista de eleições como parâmetro


def edicao(request, pk): # Edição de Eleições 
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    if request.session.get('user_tipo') != 'Administrador': # se não for administrador
        erro = "Apenas administradores do sistema podem realizar manipulações deste tipo!"
        context = {
            'erro': erro,
        }
        return render(request, 'eleicoes/edicao.html', context) # mensagem de erro
        
    title = 'Edição de Eleições'
    eleicao = get_object_or_404(Eleicao, pk=pk)
    if request.method == "POST":
        if request.POST['bt'] == "salvar":
            form = EdicaoForm(request.POST, instance=eleicao) 
            if(form.is_valid()):
                form.save()
                return redirect('consulta_eleicoes')
        elif request.POST['bt'] == 'remover':
            eleicao.delete()
            return redirect('consulta_eleicoes')

    else:
        form = EdicaoForm(instance=eleicao)
    context = {
        'form': form, 
        'eleicao': eleicao,
        'title': title,
        }
    return render(request, 'eleicoes/edicao.html', context)

def cadastro_eleicao_candidatos(request, pk): #  ligação entre as tabelas eleições e seus respectivos candidatos
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    if request.session.get('user_tipo') != 'Administrador': # se não for administrador
        erro = "Apenas administradores do sistema podem realizar manipulações deste tipo!"
        context = {
            'erro': erro,
        }
        return render(request, 'eleicoes/edCandidatos.html', context) # mensagem de erro
    title = 'Gerência de Candidatos - Eleições'
    eleicao = get_object_or_404(Eleicao, pk=pk) # criando um objeto de eleicao para ser utilizado na tela de adição de candidatos
    eleicao_candidatos = Eleicao_candidato.objects.all() # buscando os objetos referentes aos candidatos da eleição objeto de candidatos para ser utilizado na tela de adição de candidatos
    existe=False
    #Eleicao_candidato.objects.all().delete() #limpar a tabela
    if request.method == 'POST': # se o formulário foi submetido
        form = CadastroFormEleicao_candidatos(request.POST) # Criar o formulário
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            aux = form.save(commit=False)
            #print(aux.candidato)
            aux.eleicao = eleicao # realizando a ligação da tabela eleição com Eleicao_eleitores
            for e_c in eleicao_candidatos: #só permitir um cadastro de cada eleitor 
                if e_c.candidato.pk == aux.candidato.pk and e_c.eleicao.pk == eleicao.pk: #teste para verificar se já há o registro no banco
                    existe = True; # caso exista, existe vira true
            if request.POST['bt'] == "adicionar":
                #print('adicionar')
                if not existe: # realiza o commit apenas se não existir o registro no banco
                    aux.save();
            if request.POST['bt'] == "remover": #caso seja clicado no botão remover, será deletado o registro que contém o respectivo eleitor na respectiva eleição
                Eleicao_candidato.objects.filter(eleicao__pk=pk, candidato=aux.candidato).delete() #encontrar o respectiva linha na tabela e depois deletar a mesma
            return redirect('edCandidatos', pk)
    else:
        form = CadastroFormEleicao_candidatos()

    candidatos = Usuario.objects.filter(tipo='Candidato')

    eleicao_candidatos = Eleicao_candidato.objects.filter(eleicao__pk=pk) # deve ser criado a lista dos candidatos da respectiva eleição 
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form, # informando o formulário para o gerenciamento de candidatos
        'eleicao': eleicao, # passando as informações da eleição atual
        'eleicao_candidatos': eleicao_candidatos, # passando a lista de candidatos
        'candidatos': candidatos, # passando uma lista de candidatos para ser realizado a seleção de candidatos
        'title': title,
    } 
    
    return render(request, 'eleicoes/edCandidatos.html', context)

def cadastro_eleicao_eleitores(request, pk): #  ligação entre as tabelas eleições e seus respectivos candidatos
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    if request.session.get('user_tipo') != 'Administrador': # se não for administrador
        erro = "Apenas administradores do sistema podem realizar manipulações deste tipo!"
        context = {
            'erro': erro,
        }
        return render(request, 'eleicoes/edEleitores.html', context) # mensagem de erro
    title = 'Gerência de Eleitores - Eleições'
    eleicao = get_object_or_404(Eleicao, pk=pk) # criando um objeto de eleicao para ser utilizado na tela de adição de candidatos
    eleicao_eleitores = Eleicao_eleitor.objects.all() # buscando os objetos referentes aos candidatos da eleição objeto de candidatos para ser utilizado na tela de adição de candidatos
    existe=False
    #Eleicao_eleitor.objects.all().delete() #limpar a tabela
    if request.method == 'POST': # se o formulário foi submetido
        form = CadastroFormEleicao_eleitores(request.POST) # Criar o formulário
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            aux = form.save(commit=False)
            aux.eleicao = eleicao # realizando a ligação da tabela eleição com Eleicao_eleitores
            for e_e in eleicao_eleitores: #só permitir um cadastro de cada eleitor
                #print(e_e.eleicao.pk)
                #print(eleicao.pk)
                #print(e_e.eleitor.pk)
                #print(aux.eleitor.pk)
                if e_e.eleitor.pk == aux.eleitor.pk and e_e.eleicao.pk == eleicao.pk : #teste para verificar se já há o registro no banco
                    existe = True; # caso exista, existe vira true
            if request.POST['bt'] == "adicionar":
                #print('adicionar')
                if not existe: # realiza o commit apenas se não existir o registro no banco
                    aux.save();
            if request.POST['bt'] == "remover": #caso seja clicado no botão remover, será deletado o registro que contém o respectivo eleitor na respectiva eleição
                #print('remover')
                Eleicao_eleitor.objects.filter(eleicao__pk=pk, eleitor=aux.eleitor).delete() #encontrar o respectiva linha na tabela e depois deletar a mesma


            return redirect('edEleitores', pk)
    else:
        form = CadastroFormEleicao_eleitores()
    eleitores = Usuario.objects.filter(tipo='Eleitor')
    eleicao_eleitores = Eleicao_eleitor.objects.filter(eleicao__pk=pk)
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form, # informando o formulário para o gerenciamento de eleitores
        'eleicao': eleicao, # passando as informações da eleição atual
        'eleicao_eleitores': eleicao_eleitores, # passando a lista de eleitores
        'eleitores': eleitores, # passando uma lista de eleitores para ser realizado a seleção de eleitores
        'title': title,
    } 

    return render(request, 'eleicoes/edEleitores.html', context)

