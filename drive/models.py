from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Dossier(models.Model):
    nom = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

def validate_file_size(value):
    limit = 40 * 1024 * 1024  # 40 Mo
    if value.size > limit:
        raise ValidationError(f'Taille de fichier trop grande. La taille maximale est de {limit / (1024 * 1024)} Mo.')
    
    
class Document(models.Model):
    nom = models.CharField(max_length=255)
    type_fichier = models.CharField(max_length=50)
    date_ajout = models.DateTimeField(auto_now_add=True)
    taille_fichier = models.PositiveIntegerField()
    fichier = models.FileField(upload_to='')  # On définira le dossier dynamiquement
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    dossier = models.ForeignKey(Dossier, null=True, blank=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # Si l'utilisateur a un nom, créez un dossier avec son nom et ajoutez le fichier
        if not self.fichier.name.startswith(self.utilisateur.username):
            self.fichier.name = f"{self.utilisateur.username}/{self.fichier.name}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nom