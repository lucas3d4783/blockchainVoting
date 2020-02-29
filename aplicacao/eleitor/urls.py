from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index_eleitor'),
    path('consulta/', views.consulta, name='consulta_eleitor'),
    url(r'^votacao/(?P<pk>[0-9]+)$', views.votacao, name='votacao'),
    url(r'^selecionar_candidato/(?P<eleicao_pk>[0-9]+)_(?P<candidato_pk>[0-9]+)_(?P<eleitor_pk>[0-9]+)$', views.selecionar_candidato, name='selecionar_candidato'),
    
]