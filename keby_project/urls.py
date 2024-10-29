"""
URL configuration for keby_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include,path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/',include('polls.urls')),
]


#Ici puisque l'on est dans le projet principal on doit creer un url vers notre application polls  en utilisant include et en lui passant le chemin de l'application polls.urls
#Pour que lorsque l'on tape http://polls/ on soit redirigé vers l'application polls et non pas vers le projet principal ainsi que les urls de polls.urls