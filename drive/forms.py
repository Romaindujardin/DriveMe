# forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['fichier',]  # Utilisez 'fichier' pour correspondre au champ dans le modèle
        widgets ={
            #Je vais juste préciser que le champ fichier est un champ input file pour le récupérer plus tard
            'fichier': forms.FileInput(attrs={'id':'file_Input'}),
        }
