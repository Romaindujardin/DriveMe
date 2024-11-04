from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import DocumentForm
from django.http import FileResponse
from .models import Dossier, Document
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
from django.db.models import Sum
from django.conf import settings
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
            return redirect('document_list')  # Remplace 'main' par le nom de ta vue principale
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
            return redirect('document_list')  # Redirige vers la page principale
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

@login_required
def document_list(request):
    file_type = request.GET.get('type')  # Récupère le type de fichier depuis les paramètres de l'URL

    # Filtrer les documents par utilisateur, exclure ceux associés à un dossier, et éventuellement par type de fichier
    if file_type:
        documents = Document.objects.filter(utilisateur=request.user, dossier__isnull=True, type_fichier=file_type).order_by('-date_ajout')
    else:
        documents = Document.objects.filter(utilisateur=request.user, dossier__isnull=True).order_by('-date_ajout')

    # Récupérer les dossiers de l'utilisateur
    dossiers = Dossier.objects.filter(utilisateur=request.user)

    # Récupérer l'espace utilisé par l'utilisateur
    used_space = get_user_storage_usage(request.user) / (1024 * 1024)  # Convertir en Mo

    # Convertir la taille des documents en Mo
    for document in documents:
        document.taille_fichier_mo = document.taille_fichier / 1024  # Conversion de Ko à Mo

    return render(request, 'main.html', {
        'dossiers': dossiers,
        'documents': documents,
        'used_space': used_space
    })





@login_required
def create_folder(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        Dossier.objects.create(nom=nom, utilisateur=request.user)
        return redirect('document_list')  # Redirige vers la liste des documents
    return render(request, 'create_folder.html')

@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Dossier, id=folder_id, utilisateur=request.user)
    folder.delete()
    return redirect('document_list')

@login_required
def rename_folder(request, folder_id):
    folder = get_object_or_404(Dossier, id=folder_id, utilisateur=request.user)
    if request.method == 'POST':
        new_name = request.POST.get('nom')
        folder.nom = new_name
        folder.save()
        return redirect('document_list')
    return render(request, 'rename_folder.html', {'folder': folder})


@login_required
def upload_folder(request, folder_id):
    # Récupérer le dossier dans lequel on est
    dossier = get_object_or_404(Dossier, id=folder_id, utilisateur=request.user)

    # Récupérer tous les documents de l'utilisateur qui n'ont pas de dossier affilié
    documents = Document.objects.filter(utilisateur=request.user, dossier_id__isnull=True)

    return render(request, 'upload_folder.html', {'dossier': dossier, 'documents': documents})

@login_required
def affilier_document(request, document_id):
    if request.method == "POST":
        dossier_id = request.POST.get('dossier_id')
        
        # Récupérer le document
        document = get_object_or_404(Document, id=document_id, utilisateur=request.user)

        # Assigner le dossier
        document.dossier_id = dossier_id
        document.save()

        # Rediriger vers la page du dossier ou une page de confirmation
        return redirect('upload_folder', folder_id=dossier_id)

    return redirect('upload_folder', folder_id=dossier_id)

@login_required
def folder_document_list(request, folder_id):
    dossier = get_object_or_404(Dossier, id=folder_id, utilisateur=request.user)  # Récupère le dossier
    documents = Document.objects.filter(dossier_id=dossier.id)  # Filtrer les documents par dossier

    return render(request, 'folder_documents.html', {'dossier': dossier, 'documents': documents})

def download_file(request, file_id):
    document = get_object_or_404(Document, id=file_id)
    response = FileResponse(open(document.file.path, 'rb'))  # Assurez-vous que le chemin du fichier est correct
    response['Content-Disposition'] = f'attachment; filename="{document.nom}"'
    return response

def folder_list(request):
    dossiers = Dossier.objects.all()  # Récupère tous les dossiers
    return render(request, 'your_template.html', {'dossiers': dossiers})


def get_user_storage_usage(user):
    # Calcule l'espace utilisé par l'utilisateur en utilisant l'agrégation
    total_size = Document.objects.filter(utilisateur=user).aggregate(Sum('taille_fichier'))['taille_fichier__sum'] or 0
    return total_size

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.utilisateur = request.user  # Associe le document à l'utilisateur connecté
            document.taille_fichier = document.fichier.size
            document.type_fichier = document.fichier.name.split('.')[-1]  # Ext. de fichier

            # Créer un dossier pour chaque utilisateur dans le répertoire de stockage
            user_directory = os.path.join(settings.MEDIA_ROOT, request.user.username)
            os.makedirs(user_directory, exist_ok=True)
            
            # Enregistrer le fichier dans le dossier de l'utilisateur
            document.fichier.name = f"{request.user.username}/{document.fichier.name}"
            document.save()

            return redirect('document_list')  # Redirige vers une vue listant les documents

    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

@login_required
def rename_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Nom du document modifié avec succès.")
            return redirect('document_list')  # Redirige vers la liste des documents
    else:
        form = DocumentForm(instance=document)

    return render(request, 'rename_document.html', {'form': form})
@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, utilisateur=request.user)
    document.delete()
    messages.success(request, 'Document supprimé avec succès.')
    return redirect('document_list')
