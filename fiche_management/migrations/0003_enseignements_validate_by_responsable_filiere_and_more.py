# Generated by Django 5.0.4 on 2024-11-15 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_management', '0002_sheet_validate_by_responsable_filiere_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enseignements',
            name='validate_by_responsable_filiere',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='enseignements',
            name='validate_by_responsable_ufr',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='enseignements',
            name='validate_by_vice_presient',
            field=models.BooleanField(null=True),
        ),
    ]