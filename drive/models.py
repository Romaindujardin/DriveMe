from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Dossier(models.Model):
    nom = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    #booléen pour savoir si le dossier est en favoris
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

def validate_file_size(value):
    limit = 40 * 1024 * 1024  # 40 Mo
    if value.size > limit:
        raise ValidationError(f'Taille de fichier trop grande. La taille maximale est de {limit / (1024 * 1024)} Mo.')
    
    
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class Document(models.Model):
    nom = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    type_fichier = models.CharField(max_length=50)
    date_ajout = models.DateTimeField(auto_now_add=True)
    taille_fichier = models.PositiveIntegerField()
    fichier = models.FileField(upload_to='', null=True, blank=True)  # On définira le dossier dynamiquement
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    dossier = models.ForeignKey('Dossier', null=True, blank=True, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si l'utilisateur a un nom, créez un dossier avec son nom et ajoutez le fichier
        if self.nom and not self.nom.startswith(self.utilisateur.username):
            self.nom = f"{self.utilisateur.username}/{self.fichier.name}"

        # Si le fichier existe, définissez l'URL
        if self.fichier:
            # Créez l'URL complète pour accéder au fichier
            self.url = self.fichier.url  # L'URL du fichier sera automatiquement gérée par Django

        super().save(*args, **kwargs)
    
    def get_nom_fichier(self):
        return os.path.basename(self.nom)

    def __str__(self):
        return self.nom
