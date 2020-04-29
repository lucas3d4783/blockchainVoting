
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index_blockchain'),
    path('addBloco/', views.add_bloco_generico, name='add_bloco_generico'),
    path('consulta/', views.consulta, name='consulta_blockchain'),
    #url(r'^edit/(?P<pk>[0-9]+)$', views.edicao, name='edicao_cursos'),
    
]