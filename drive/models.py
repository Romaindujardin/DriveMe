from django.db import models
from django.contrib.auth.models import User



class Document(models.Model):
    nom = models.CharField(max_length=255)
    type_fichier = models.CharField(max_length=50)
    date_ajout = models.DateTimeField(auto_now_add=True)
    taille_fichier = models.PositiveIntegerField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom