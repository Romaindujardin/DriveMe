from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    nom = models.CharField(max_length=100)
    fichier = models.FileField(upload_to='documents/')  # Utilisez FileField pour le fichier
    date_ajout = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
