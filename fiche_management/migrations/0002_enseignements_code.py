# Generated by Django 5.0.4 on 2024-10-31 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enseignements',
            name='code',
            field=models.CharField(max_length=25, null=True, unique=True, verbose_name='code'),
        ),
    ]
