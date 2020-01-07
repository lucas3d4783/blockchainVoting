from django.db import models
from django.utils import timezone
import hashlib

class Cadastro(models.Model):
    usuario = models.CharField(max_length=40)
    nome =  models.CharField(max_length=100)
    sobrenome =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=50)
    data = models.DateTimeField(default=timezone.now)

    def cadastrar(self):
        self.data = timezone.now()
        h = hashlib.sha256(self.senha).hexdigest()
        self.senha = h
        self.save()

    def __str__(self):
        return self.nome

    def __unicode__(self): #se nao utilizar o matodo, acontece o erro "UnicodeEncodeError: ascii codec can't encode characters in position 0-3: ordinal not in range(128)"
        return self.nome

