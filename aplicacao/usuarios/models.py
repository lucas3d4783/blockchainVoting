from django.db import models
from django.utils import timezone
import hashlib
from django.utils.translation import ugettext_lazy as _
from cursos.models import Curso
import uuid
import os
from datetime import date

def get_file_path(instance, filename): #função para gerar um nome único para as mídias
    ext = filename.split(".")[-1] #pegar a extensão do arquivo
    data_atual = date.today() # obter data atual
    data = data_atual.strftime('%Y/%m/%d/') # formatar data para ano/mês/dia, onde o mesmo será utilizado na estrutura de diretórios
    filename = "%s%s.%s" % (data, uuid.uuid4(), ext) #gerar o hash da data concatenada com a primeira parte do arquivo e sua respectiva extensão
    return os.path.join("usuarios", filename) # retornar o caminho completo do arquivo

#def handle_uploaded_file(f, caminho):
#    destination = open(caminho, 'wb+')
#    for chunk in f.chunks():
#        destination.write(chunk)
#    destination.close()

class Usuario(models.Model):
    usuario = models.CharField(max_length=40)
    nome =  models.CharField(max_length=100)
    sobrenome =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=50)

    foto = models.FileField(upload_to=get_file_path) #chamando a função de definição de nome para nomear o arquivo recebido

    #para o upload de imagens é necessário instalar o módulo Pill (pip  install pillow)

    tipo = models.CharField(max_length=20, choices=(("Administrador", _("Administrador")),  #criação do modelo de opções do tipo de usuário
                                        ("Eleitor", _("Eleitor")),
                                        ("Candidato", _("Candidato"))),
                                default="Eleitor") # vai definir Eleitor como a opção default
 
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default="") #chave estrangeira da tabela curso

    def __str__(self):
        return self.nome

    def __unicode__(self): #se nao utilizar o matodo, acontece o erro "UnicodeEncodeError: ascii codec can't encode characters in position 0-3: ordinal not in range(128)"
        return self.nome

    #def get_file_path(self, filename): #função para gerar um nome único para as mídias
    #    ext = filename.split(".")[-1] #pegar a extensão do arquivo
    #    data_atual = date.today() # obter data atual
    #    data = data_atual.strftime('%Y/%m/%d/') # formatar data para ano/mês/dia, onde o mesmo será utilizado na estrutura de diretórios
    #    filename = "%s%s.%s" % (data, uuid.uuid4(), ext) #gerar o hash da data concatenada com a primeira parte do arquivo e sua respectiva extensão
    #    return os.path.join("usuarios", filename) # retornar o caminho completo do arquivo

