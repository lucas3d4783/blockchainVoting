
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index_cursos'),
    path('consulta/', views.consulta, name='consulta_cursos'),
    url('cadastro/', views.cadastro, name='cadastro_cursos'),
    url(r'^edit/(?P<pk>[0-9]+)$', views.edicao, name='edicao_cursos'),
    
]