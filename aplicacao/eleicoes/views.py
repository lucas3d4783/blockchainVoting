from django.shortcuts import render, get_object_or_404, redirect
from .models import Eleicao, Eleicao_candidato, Eleicao_eleitor
from .forms import CadastroForm, EdicaoForm, CadastroFormEleicao_candidatos, CadastroFormEleicao_eleitores

def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'eleicoes/index.html')

def cadastro(request): #  Criação de eleições 
    if request.method == 'POST': # se o formulário foi submetido
        form = CadastroForm(request.POST) # Criar o formulário
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            form.save()
            return redirect('consulta_eleicoes')
    else:
        form = CadastroForm()
    
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form
        } 
    
    return render(request, 'eleicoes/cadastro.html', context)


def consulta(request): # Listagem das eleições criadas
    eleicoes = Eleicao.objects.filter().order_by('nome') #buscar as eleições no banco e ordenar pelo nome
    return render(request, 'eleicoes/consulta.html', {'eleicoes': eleicoes}) #chamar o template de consulta, passando a lista de eleições como parâmetro


def edicao(request, pk): # Edição de Eleições 
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
    return render(request, 'eleicoes/edicao.html', {'form': form, 'eleicao': eleicao})

def cadastro_eleicao_candidatos(request, pk): #  ligação entre as tabelas eleições e seus respectivos candidatos
    eleicao = get_object_or_404(Eleicao, pk=pk) # criando um objeto de eleicao para ser utilizado na tela de adição de candidatos
    eleicao_candidatos = Eleicao_candidato.objects.all() # buscando os objetos referentes aos candidatos da eleição objeto de candidatos para ser utilizado na tela de adição de candidatos
    existe=False
    #Eleicao_candidato.objects.all().delete() #limpar a tabela
    if request.method == 'POST': # se o formulário foi submetido
        form = CadastroFormEleicao_candidatos(request.POST) # Criar o formulário
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            aux = form.save(commit=False)
            aux.eleicao = eleicao # realizando a ligação da tabela eleição com Eleicao_eleitores
            for e_c in eleicao_candidatos: #só permitir um cadastro de cada eleitor
                if e_c.candidato.pk == aux.candidato.pk and e_c.eleicao.pk == eleicao.pk: #teste para verificar se já há o registro no banco
                    existe = True; # caso exista, existe vira true
            if request.POST['bt'] == "adicionar":
                print('adicionar')
                if not existe: # realiza o commit apenas se não existir o registro no banco
                    aux.save();
            if request.POST['bt'] == "remover": #caso seja clicado no botão remover, será deletado o registro que contém o respectivo eleitor na respectiva eleição
                Eleicao_candidato.objects.filter(eleicao__pk=pk, candidato=aux.candidato).delete() #encontrar o respectiva linha na tabela e depois deletar a mesma
            return redirect('addCandidatos', pk)
    else:
        form = CadastroFormEleicao_candidatos()
    
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form, 
        'eleicao': eleicao,
        'eleicao_candidatos': eleicao_candidatos,
    } 
    
    return render(request, 'eleicoes/addCandidatos.html', context)

def cadastro_eleicao_eleitores(request, pk): #  ligação entre as tabelas eleições e seus respectivos candidatos
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
                print('adicionar')
                if not existe: # realiza o commit apenas se não existir o registro no banco
                    aux.save();
            if request.POST['bt'] == "remover": #caso seja clicado no botão remover, será deletado o registro que contém o respectivo eleitor na respectiva eleição
                print('remover')
                Eleicao_eleitor.objects.filter(eleicao__pk=pk, eleitor=aux.eleitor).delete() #encontrar o respectiva linha na tabela e depois deletar a mesma


            return redirect('addEleitores', pk)
    else:
        form = CadastroFormEleicao_eleitores()

    eleicao_eleitores = Eleicao_eleitor.objects.filter(eleicao__pk=pk)
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form, 
        'eleicao': eleicao,
        'eleicao_eleitores': eleicao_eleitores,
    } 

    return render(request, 'eleicoes/addEleitores.html', context)