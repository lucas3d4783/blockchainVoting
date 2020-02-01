from django.shortcuts import render, get_object_or_404, redirect
from .models import Eleicao
from .forms import CadastroForm, EdicaoForm

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
