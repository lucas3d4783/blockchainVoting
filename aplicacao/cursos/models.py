from django.db import models
from django.utils import timezone
import hashlib

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=500)
    carga_horaria = models.IntegerField()
    centro = models.CharField(max_length=50) # pensar em criar uma tabela para o centro
    data = models.DateTimeField(default=timezone.now)

    

    def cadastrar(self):
        self.data = timezone.now()
        self.save()

    def __str__(self):
        return self.nome

    def __unicode__(self): #se nao utilizar o matodo, acontece o erro "UnicodeEncodeError: ascii codec can't encode characters in position 0-3: ordinal not in range(128)"
        return self.nome

