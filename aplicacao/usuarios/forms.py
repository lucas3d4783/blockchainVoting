# _*_ coding: utf-8 _*_     #definindo a formatação do arquivo para não apresentar erros

from django import forms 
from .models import Usuario # importando o modelo post criado para usuários

class CadastroForm(forms.ModelForm): 
    class Meta:
        model = Usuario #definindo o modelo como Usuario 
        fields = ('tipo', 'curso', 'nome', 'sobrenome', 'usuario', 'email', 'senha') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 50}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'maxlenght': 20}), #select para uma lista predefinida no model
            'curso': forms.Select(attrs={'class': 'form-control', 'maxlenght': 50}), #select para selecionar o curso de outra tabela (a chave estrangeira foi definida no model)
        }

class EdicaoForm(forms.ModelForm): 
    class Meta:
        model = Usuario #definindo o modelo como Usuario 
        fields = ('tipo', 'curso', 'nome', 'sobrenome', 'usuario', 'email') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'maxlenght': 20}), #select para uma lista predefinida no model
            'curso': forms.Select(attrs={'class': 'form-control', 'maxlenght': 50}), #select para selecionar o curso de outra tabela (a chave estrangeira foi definida no model)
            
        }
       
class AlterarSenhaForm(forms.ModelForm):
    class Meta:
        model = Usuario #definindo o modelo como Usuario 
        fields = ('senha', 'senha') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 50}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 50}),
            
            
        }