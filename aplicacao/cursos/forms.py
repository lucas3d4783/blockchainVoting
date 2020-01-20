# _*_ coding: utf-8 _*_     #definindo a formatação do arquivo para não apresentar erros

from django import forms 
from .models import Cursos # importando o modelo post criado para usuários

class CadastroForm(forms.ModelForm): 
    class Meta:
        model = Cursos #definindo o modelo como o de curso 
        fields = ('nome', 'descricao', 'carga_horaria', 'centro') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 500}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'maxlenght': 4}),
            'centro': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40}),

        }

