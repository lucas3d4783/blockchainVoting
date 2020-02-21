from django.shortcuts import render, redirect, get_object_or_404
from cursos.forms import CadastroForm, EdicaoForm
from cursos.models import Curso

# Create your views here.

def index(request): #quando for solicitado o url index, será encaminhado o index.html
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Cursos'
    context = {
        'title': title,
    }
    return render(request, 'cursos/index.html', context)



def cadastro(request): #  Criação de cursos
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Cadastro de Cursos'
    form = CadastroForm(request.POST or None) # o formulário pode estar vázio ou não, se estiver apenas carregando o formulário
    context = {
        'form': form,
        'title': title,
    } # variável utilizada para encaminhar as informações para a tela de cadastro
    if request.method == 'POST': # se o formulário foi submetido
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            #form.save(commit=False) # tem que atribuir o form para um objeto para poder realizar as manipulações 
            form.save()
            return redirect('consulta_cursos')
    return render(request, 'cursos/cadastro.html', context)


def consulta(request): # Listagem dos cursos criados
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Consulta de Cursos'
    cursos = Curso.objects.filter().order_by('nome') #buscar os cursos no banco e ordenar pelo nome
    context =  {
        'cursos': cursos, 
        'title': title,
    }
    return render(request, 'cursos/consulta.html', context) #chamar o template de consulta, passando a lista de cursos como parâmetro

def edicao(request, pk): # Edição de cursos 
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Edição de Cursos'
    curso = get_object_or_404(Curso, pk=pk)
    form = EdicaoForm(instance=curso)
    if request.method == "POST":
        if request.POST['bt'] == "salvar":
            form = EdicaoForm(request.POST, instance=curso)
            if(form.is_valid()):
                form.save()
                return redirect('consulta_cursos')
        elif request.POST['bt'] == 'remover':
            curso.delete()
            return redirect('consulta_cursos')
    else:
        form = EdicaoForm(instance=curso)
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'cursos/edicao.html', context)
