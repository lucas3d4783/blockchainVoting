# _*_ coding: utf-8 _*_ 
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Usuario
from django.http import HttpResponse
import hashlib
from django.core.exceptions import ObjectDoesNotExist


def index(request): #quando for solicitado o url index, será encaminhado o index.html
    #try:
        if not request.session.get('logado'): # se não estiver logado
            #print(request.session.get('user'))
            return redirect('login')
        return render(request, 'index.html')
        
    #except:
    #    return redirect(request, 'login')

def contato(request): #quando for solicitado o url contato, será encaminhado o index.html
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Contato'
    context = {
        'title': title,
    }
    return render(request, 'contato.html', context)


def sobre(request): #quando for solicitado o url sobre, será encaminhado o index.html
    if not request.session.get('logado'): # se não estiver logado
        return redirect('login') # redireciona para a tela de login
    title = 'Sobre'
    context = {
        'title': title,
    }
    return render(request, 'sobre.html', context)



#https://django-portuguese.readthedocs.io/en/1.0/topics/http/sessions.html
#https://docs.djangoproject.com/en/3.0/topics/http/sessions/

def login(request):
    title = "Login"
    erro = ''
    if request.method == "POST":
        try: 
            u = Usuario.objects.get(usuario=request.POST['usuario']) # tenta encontrar o usuário no banco
            senha = hashlib.sha256(request.POST['senha'].encode('utf-8')).hexdigest()# gerar o hash da senha informada 
            if u.senha == senha: # compara com o hash armazenado no banco
                request.session['user'] = u.nome + " " + u.sobrenome # armazenar o nome do usuário
                request.session['user_pk'] = u.pk
                request.session['logado'] = True
                return redirect('index') # redireciona para a página inicial
            else: # caso a senha não esja errada 
                erro = 'Senha incorreta!'

        except ObjectDoesNotExist: # Caso o usuário não exista no banco, será gerado uma excessão
            erro = 'Usuário não cadastrado!'
            context = {
                'erro': erro,
                'title': title,
            }
            return render(request, 'login.html', context)
        except:
            erro = 'Erro!'
            context = {
                'erro': erro,
                'title': title,
            }
            return render(request, 'login.html', context)


    if erro != '': #caso ocorra algum erro
        context = {
            'erro': erro,
            'title': title,
        }
        return render(request, 'login.html', context)

    context = {
        'title': title,
    }
    return render(request, 'login.html', context)

        
    

def logout(request):
    try:
        del request.session['logado']
    except KeyError:
        pass
    return redirect('login')

