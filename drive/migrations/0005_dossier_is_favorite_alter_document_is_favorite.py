# Generated by Django 5.1.3 on 2024-11-07 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0004_alter_document_fichier'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossier',
            name='is_favorite',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='is_favorite',
            field=models.BooleanField(default=True),
        ),
    ]