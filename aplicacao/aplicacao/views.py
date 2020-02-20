# _*_ coding: utf-8 _*_ 
from django.shortcuts import render
from usuarios.models import Usuario
from django.http import HttpResponse


def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'index.html')

def contato(request): #quando for solicitado o url contato, será encaminhado o index.html
    title = 'Contato'
    context = {
        'title': title,
    }
    return render(request, 'contato.html', context)

def sobre(request): #quando for solicitado o url sobre, será encaminhado o index.html
    title = 'Sobre'
    context = {
        'title': title,
    }
    return render(request, 'sobre.html', context)


#https://django-portuguese.readthedocs.io/en/1.0/topics/http/sessions.html
#https://docs.djangoproject.com/en/3.0/topics/http/sessions/

def login(request):
    u = Usuario.objects.get(usuario=request.POST['usuario'])
    if u.senha == request.POST['senha']:
        request.session['member_id'] = u.pk
        return HttpResponse(u"Você está autenticado.")
    else:
        return HttpResponse(u"Seu nome de usuário e senha não conferem.")

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse(u"Você saiu.")

