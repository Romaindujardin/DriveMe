from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Q
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import FileResponse
from django.http import HttpResponse
from .models import Dossier, Document
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
from django.db.models import Sum
from django.conf import settings
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend non interactif pour matplotlib
def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('home')  # Redirige vers la page d'accueil ou une autre page de ton choix


def home(request):
    if request.user.is_authenticated:
        return redirect('main')  # Remplacez 'main' par le nom correct de votre URL
    return render(request, 'home.html')  # Remplacez 'home.html' par le nom de votre template pour la page d'accueil


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

def upload_file(request): #NE MARCHE PAS 
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

    # Filtrer les documents par utilisateur, exclure ceux associés à un dossier (dossier_id est null), et éventuellement par type de fichier
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
            document.type_fichier = document.fichier.name.split('.')[-1]  # Extension de fichier

            # Utiliser le nom du fichier pour le champ `nom`
            document.nom = document.fichier.name  # Attribue le nom du fichier

            # Créer un dossier pour chaque utilisateur dans le répertoire de stockage
            user_directory = os.path.join(settings.MEDIA_ROOT, request.user.username)
            os.makedirs(user_directory, exist_ok=True)

            # Enregistrer le fichier dans le dossier de l'utilisateur
            document.fichier.name = os.path.join(request.user.username, document.fichier.name)
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



@login_required
def stats(request):
    # Calcul de l'espace utilisé en Mo
    used_space = get_user_storage_usage(request.user) / (1024 * 1024)  # Convertir en Mo
    total_space = 100  # Espace total disponible en Mo (à ajuster selon vos besoins)

    # Statistiques des types de fichiers
    documents = Document.objects.all()
    file_type_counts = {}
    for doc in documents:
        if doc.fichier:
            file_type = doc.fichier.name.split('.')[-1]
            file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
    
    # Générer l'histogramme avec Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(file_type_counts.keys(), file_type_counts.values())
    plt.xlabel('Type de fichier')
    plt.ylabel('Nombre de fichiers')
    plt.title('Nombre de fichiers par type de fichier')
    
    # Sauvegarder le graphique dans un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encoder le graphique en base64
    graph = base64.b64encode(image_png).decode('utf-8')

    # Préparer le contexte
    context = {
        'graph': f'data:image/png;base64,{graph}',
        'used_storage': round(used_space, 2),
        'total_storage': total_space,
        'used_space': used_space

    }
    
    return render(request, 'stats.html', context)
# def stats(request):
#     # Création d'un graphique avec matplotlib
#     plt.figure()
#     x = [1, 2, 3, 4, 5]
#     y = [10, 15, 13, 17, 19]
#     plt.plot(x, y)
#     plt.xlabel('Temps')
#     plt.ylabel('Valeur')
#     plt.title('Statistiques d"upload')
    
#     # Sauvegarder le graphique dans un buffer en mémoire
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close()
#     buffer.seek(0)
    
#     # Convertir l'image en URL de données et l'insérer dans le HTML
#     image_png = buffer.getvalue()
#     image_data = base64.b64encode(image_png).decode('utf-8')
#     image_uri = f"data:image/png;base64,{image_data}"

#     return render(request, 'stats.html', {'graph': image_uri})   
@login_required 
def files_view(request):
    documents = Document.objects.filter(utilisateur=request.user, dossier__isnull=True)
    used_space = get_user_storage_usage(request.user) / (1024 * 1024)
    
    return render(request, 'files.html', {
        'documents': documents,
        'used_space': used_space
    })

@login_required
def folder_view(request):
    dossiers = Dossier.objects.filter(utilisateur=request.user)
    documents = Document.objects.filter(utilisateur=request.user)
    used_space = get_user_storage_usage(request.user) / (1024 * 1024)
    
    return render(request, 'folder.html', {
        'dossiers': dossiers,
        'documents': documents, 
        'used_space': used_space
    })



def search_documents(request):
    used_space = get_user_storage_usage(request.user) / (1024 * 1024)
    query = request.GET.get('q', '')
    file_type = request.GET.get('type', '')
    
    # Initialiser avec des QuerySets vides
    documents = Document.objects.none()
    dossiers = Dossier.objects.none()
    
    # Ne faire la recherche que si une requête est présente
    if query:
        documents = Document.objects.all()
        dossiers = Dossier.objects.all()
        
        # Appliquer les filtres de recherche
        documents = documents.filter(
            Q(nom__icontains=query) |
            Q(utilisateur__username__icontains=query)
        )
        dossiers = dossiers.filter(nom__icontains=query)
        
        # Appliquer le filtre de type si spécifié
        if file_type:
            if file_type == 'image':
                documents = documents.filter(
                    type_fichier__in=['jpg', 'png', 'gif', 'PNG']
                )
            else:
                documents = documents.filter(type_fichier=file_type)
    
    context = {
        'documents': documents,
        'dossiers': dossiers,
        'query': query,
        'file_type': file_type,
        'show_results': bool(query)  # Nouveau flag pour le template
    }
    
    context['used_space'] = used_space
    return render(request, 'search.html', context)

