
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index_usuario'),
    path('consulta/', views.consulta, name='consulta'),
    url('cadastro/', views.cadastro, name='cadastro'),
    url(r'^edit/(?P<pk>[0-9]+)$', views.edicao, name='edicao'),
]