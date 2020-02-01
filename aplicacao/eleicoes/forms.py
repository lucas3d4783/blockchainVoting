from django import forms
from .models import Eleicao

class CadastroForm(forms.ModelForm): 
    data_ini = forms.DateField(widget=forms.SelectDateWidget()) #posteriormente melhorar a estilização
    data_fim = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Eleicao #definindo o modelo como Usuario 
        fields = ('tipo', 'nome', 'descricao', 'data_ini', 'data_fim') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40, 'placeholder': 'Digite um nome para a Eleição', 'title': 'Nome da Eleição', 'required': True}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100, 'placeholder': 'Descreva a Eleição', 'title': 'Descrição da Eleição', 'required': True}),
            'tipo': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 20, 'title': 'Tipo de Eleição', 'required': True}), #select para uma lista predefinida no model
        }

        error_messages = {   #verificar o porquê de não estar funcionando
            'nome':{'required': 'O campo nome é obrigatório'},
            'descricao':{'required': 'O campo sobrenome é obrigatório'},
        }

class EdicaoForm(forms.ModelForm): 
    data_ini = forms.DateField(widget=forms.SelectDateWidget()) #posteriormente melhorar a estilização
    data_fim = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Eleicao #definindo o modelo como Usuario 
        fields = ('tipo', 'nome', 'descricao', 'data_ini', 'data_fim') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40, 'placeholder': 'Digite um nome para a Eleição', 'title': 'Nome da Eleição', 'required': True}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 100, 'placeholder': 'Descreva a Eleição', 'title': 'Descrição da Eleição', 'required': True}),
            'tipo': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 20, 'title': 'Tipo de Eleição', 'required': True}), #select para uma lista predefinida no model
        }
