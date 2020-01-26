"""aplicacao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('', views.index, name='index'), # usa-se o name para poder invocar a url posteriormente em algum link (href)
    path('contato', views.contato, name='contato'),
    path('sobre', views.sobre, name='sobre'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('cursos/', include('cursos.urls'))
   
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




