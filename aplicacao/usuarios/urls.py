
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.consulta, name='consulta'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),

]