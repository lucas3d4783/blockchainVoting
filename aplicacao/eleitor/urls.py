from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index_eleitor'),
    path('consulta/', views.consulta, name='consulta_eleitor'),
    url(r'^votacao/(?P<pk>[0-9]+)$', views.votacao, name='votacao'),
    
]