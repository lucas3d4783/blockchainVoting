from django.db import models
from usuarios.models import Usuario
from django.utils.translation import ugettext_lazy as _


class Eleicao(models.Model):
    nome = models.CharField(max_length=40)
    descricao =  models.CharField(max_length=100)
    data_ini =  models.DateField()
    data_fim = models.DateField() #configurar para pegar a data da criação da eleição e desativar o campo, ou deixar para programar uma data e hora e efetuar os devidos tratamentos
    #hora_ini =
    #hora_fim =  
    tipo = models.CharField(max_length=20, choices=(("eleicao", _("Eleição")),  #criação do modelo de opções do tipo de Eleicao
                                        ("votacao", _("Votação"))),
                                default="Eleição")

    def __str__(self):
        return self.nome

    def __unicode__(self): #se nao utilizar o método, acontece o erro "UnicodeEncodeError: ascii codec can't encode characters in position 0-3: ordinal not in range(128)"
        return self.nome
