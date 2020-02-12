from django import forms
from .models import Eleicao, Eleicao_candidato, Eleicao_eleitor

class CadastroForm(forms.ModelForm): 
    data_ini = forms.DateField(widget=forms.SelectDateWidget()) #posteriormente melhorar a estilização
    data_fim = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Eleicao #definindo o modelo como Usuario 
        fields = ('tipo', 'nome', 'descricao', 'data_ini', 'data_fim') # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo o campo senha como sendo de senha
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 40, 'placeholder': 'Digite um nome para a Eleição', 'title': 'Nome da Eleição', 'required': True}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'maxlenght': 100, 'placeholder': 'Descreva a Eleição', 'title': 'Descrição da Eleição', 'required': True}),
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
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'maxlenght': 100, 'placeholder': 'Descreva a Eleição', 'title': 'Descrição da Eleição', 'required': True}),
            'tipo': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 20, 'title': 'Tipo de Eleição', 'required': True}), #select para uma lista predefinida no model
        }


class CadastroFormEleicao_candidatos(forms.ModelForm): 
    class Meta:
        model = Eleicao_candidato #definindo o modelo
        fields = ('candidato',) # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo
            #'eleicao': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 50}), #select para selecionar a eleição de outra tabela (a chave estrangeira foi definida no model)
            'candidato': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 50}), #select para selecionar o candidato de outra tabela (a chave estrangeira foi definida no model)
        }

        error_messages = { #pesquisar melhor sobre tipos de erros para deixar mais funcional
            #'eleicao': {
            #    'required': 'O campo nome é obrigatório'
            #},
            'candidato': {
                'required': 'O campo candidato é obrigatório'
            },
        }


class CadastroFormEleicao_eleitores(forms.ModelForm): 
    class Meta:
        model = Eleicao_eleitor #definindo o modelo
        fields = ('eleitor',) # selecionando os campos do modelo que serão utilizados
        widgets = { #estilizando os campos com css e definindo
            #'eleicao': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 50}), #select para selecionar a eleição de outra tabela (a chave estrangeira foi definida no model)
            'eleitor': forms.Select(attrs={'class': 'custom-select', 'maxlenght': 50}), #select para selecionar o eleitor de outra tabela (a chave estrangeira foi definida no model)
        }

        error_messages = { #pesquisar melhor sobre tipos de erros para deixar mais funcional
            #'eleicao': {
            #    'required': 'O campo nome é obrigatório'
            #},
            'eleitor': {
                'required': 'O campo sobrenome é obrigatório'
            },
        }
