# forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'type_fichier',]  # Utilisez 'fichier' pour correspondre au champ dans le modèle
