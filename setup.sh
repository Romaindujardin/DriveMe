#!/bin/bash

# 1. Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# 2. Installer les dépendances à partir du fichier requirements.txt
echo "Installation des dépendances..."
pip install -r requirements.txt

# 3. Effectuer les migrations pour initialiser la base de données
echo "Exécution des migrations..."
python manage.py migrate

# 4. Charger les données de démo dans la base de données SQLite
echo "Chargement des données de démo..."


echo "Setup terminé !"
