from django.shortcuts import render

def index(request): #quando for solicitado o url index, será encaminhado o index.html
    return render(request, 'eleicoes/index.html')