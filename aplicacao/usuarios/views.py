# _*_ coding: utf-8 _*_ 
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from usuarios.forms import CadastroForm
from usuarios.models import Cadastro
from django.utils import timezone
import hashlib
from django.shortcuts import redirect

def cadastro(request): # criando a view para ser acessado 
    form = CadastroForm(request.POST or None) # o formulário pode estar vázio ou não, se estiver apenas carregando o formulário
    context = {'form': form} # variável utilizada para encaminhar as informações para a tela de cadastro
    if request.method == 'POST': # se o formulário foi submetido
        if form.is_valid(): # se todos os campos forem inseridos corretamente
            usuario = form.save(commit=False) # tem que atribuir o form para um objeto para poder realizar as manipulações 
            x = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest() #gerando o hash da senha
            usuario.senha = x
            usuario.save()
            return redirect('consulta')
    return render(request, 'usuarios/cadastro.html', context)

def consulta(request):
    print('usuarios')
    usuarios = Cadastro.objects.filter().order_by('nome') 
    return render(request, 'usuarios/consulta.html', {'usuarios': usuarios})

def edicao(request, pk):
    user = get_object_or_404(Cadastro, pk=pk)
    form = CadastroForm(instance=user)


    if request.method == "POST":
        form = CadastroForm(request.POST, instance=user)
        if(form.is_valid()):
            usuario = form.save(commit=False) # tem que atribuir o form para um objeto para poder realizar as manipulações 
            x = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest() #gerando o hash da senha
            usuario.senha = x
            usuario.save()
            return redirect('consulta')
    else:
        form = CadastroForm(instance=user)
    return render(request, 'usuarios/edicao.html', {'form': form})