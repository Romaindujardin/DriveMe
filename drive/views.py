from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import DocumentForm

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('home')  # Redirige vers la page d'accueil ou une autre page de ton choix



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')  # Remplace 'main' par le nom de ta vue principale
        else:
            # Gestion de l'échec de la connexion (optionnel)
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # Connecte l'utilisateur immédiatement
            return redirect('main')  # Redirige vers la page principale
        else:
            error_message = "Les mots de passe ne correspondent pas."
            return render(request, 'signin.html', {'error_message': error_message})

    return render(request, 'signin.html')

def home_view(request):
    return render(request, 'home.html')

def upload_file(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        print("Titre du document:", title)
        print("Fichier reçu:", file)

        if title and file:
            document = Document(title=title, file=file)
            document.save()
            print("Document enregistré avec succès !")
        else:
            print("Les données sont manquantes ou incorrectes.")
    return render(request, 'add_document.html')

@login_required  # Appliquer le décorateur ici
def main_view(request):
    return render(request, 'main.html')

