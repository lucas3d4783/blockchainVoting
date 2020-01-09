# _*_ coding: utf-8 _*_ 
from django.shortcuts import render


def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'index.html')

def contato(request): #quando for solicitado o url contato, será encaminhado o index.html
    return render(request, 'contato.html')

def sobre(request): #quando for solicitado o url sobre, será encaminhado o index.html
    return render(request, 'sobre.html')

