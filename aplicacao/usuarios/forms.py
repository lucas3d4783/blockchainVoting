# _*_ coding: utf-8 _*_     #definindo a formatação do arquivo para não apresentar erros

from django import forms 
from .models import Cadastro # importando o modelo post criado para usuários

class CadastroForm(forms.ModelForm): 
    class Meta:
        model = Cadastro #definindo o modelo como Cadastro 
        fields = ('nome', 'sobrenome', 'usuario', 'email', 'senha') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 50}),
        }

class EdicaoForm(forms.ModelForm): 
    class Meta:
        model = Cadastro #definindo o modelo como Cadastro 
        fields = ('nome', 'sobrenome', 'usuario', 'email', 'senha') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 50}),
        }
       


