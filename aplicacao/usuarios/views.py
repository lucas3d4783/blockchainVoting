# _*_ coding: utf-8 _*_ 
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from usuarios.forms import CadastroForm, EdicaoForm, AlterarSenhaForm
from usuarios.models import Usuario
from django.utils import timezone
import hashlib
from django.shortcuts import redirect
from django.db import models



def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'usuarios/index.html')

def cadastro(request): #  Criação de usuários 
    if request.method == 'POST': # se o formulário foi submetido
        form = CadastroForm(request.POST, request.FILES) # Criar o formulário
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            usuario = form.save(commit=False) # tem que atribuir o form para um objeto para poder realizar as manipulações 
            usuario.senha = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest() #gerando o hash da senha
            usuario.save()
            return redirect('consulta')
    else:
        form = CadastroForm()
    
    context = { # variável utilizada para encaminhar as informações para a tela de cadastro
        'form': form
        } 
    
    return render(request, 'usuarios/cadastro.html', context)

def consulta(request): # Listagem dos usuários criados
    usuarios = Usuario.objects.filter().order_by('nome') #buscar os usuários no banco e ordenar pelo nome
    return render(request, 'usuarios/consulta.html', {'usuarios': usuarios}) #chamar o template de consulta, passando a lista de usuários como parâmetro

def edicao(request, pk): # Edição de usuários 
    user = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        if request.POST['bt'] == "salvar":
            #user.foto = request.POST['foto']
            form = EdicaoForm(request.POST, request.FILES, instance=user) 
            if(form.is_valid()):
                #usuario = form.save(commit=False)
                #usuario.foto = Usuario.get_file_path(user, request.POST['foto'])
                #usuario.save() # não está conseguindo alterar a foto do perfil
                form.save()
                return redirect('consulta')
        elif request.POST['bt'] == 'remover':
            user.delete()
            return redirect('consulta')

    else:
        form = EdicaoForm(instance=user)
    return render(request, 'usuarios/edicao.html', {'form': form, 'user': user})

def alterar_senha(request, pk): # Alteração de senha 
    user = get_object_or_404(Usuario, pk=pk)
    form = AlterarSenhaForm(instance=user)
    
    if request.method == "POST":
        if request.POST['bt'] == "salvar":
            form = AlterarSenhaForm(request.POST, instance=user)
            usuario = form.save(commit=False) # tem que atribuir o form para um objeto para poder realizar as manipulações 
            usuario.senha = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest() #gerando o hash da senha
            usuario.save()
            return redirect('consulta')
                         
    else:
        usuario = form.save(commit=False) 
        form = AlterarSenhaForm(instance=user)

    return render(request, 'usuarios/alterar_senha.html', {'form': form, 'user': user}) # enviando o objeto user para manipular no template -> mostrar o nome do usuário neste caso