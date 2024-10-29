from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'), #une fois la vue index créée on y a  accociée une url dans le dossier polls/urls.py
    path('hello/', views.hello, name='hello'), #Ici également on va associée une url au template hello.html
]

# On a créé un fichier urls.py dans le dossier polls pour y définir les URL de l'application polls.
# Avecc le path('') on indique que la vue de l'index sera celle qui sera visionnée a la racine de l'appli soit http://polls/