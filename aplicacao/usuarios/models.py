from django.db import models
from django.utils import timezone
import hashlib
from django.utils.translation import ugettext_lazy as _
from cursos.models import Cursos

class Usuario(models.Model):
    usuario = models.CharField(max_length=40)
    nome =  models.CharField(max_length=100)
    sobrenome =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=50)
    data = models.DateTimeField(default=timezone.now)

    tipo = models.CharField(max_length=20, choices=(("Administrador", _("Administrador")),  #criação do modelo de opções do tipo de usuário
                                        ("Eleitor", _("Eleitor")),
                                        ("Candidato", _("Candidato"))),
                                default="Eleitor") # vai definir Eleitor como a opção default
 
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, default="") #chave estrangeira da tabela curso

    def cadastrar(self):
        self.data = timezone.now()
        self.save()

    def __str__(self):
        return self.nome

    def __unicode__(self): #se nao utilizar o matodo, acontece o erro "UnicodeEncodeError: ascii codec can't encode characters in position 0-3: ordinal not in range(128)"
        return self.nome


