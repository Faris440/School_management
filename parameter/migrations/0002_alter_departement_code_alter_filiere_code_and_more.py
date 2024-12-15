# Generated by Django 5.0.4 on 2024-12-15 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departement',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='filiere',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='niveau',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='semestre',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='ue',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='unitederecherche',
            name='code',
            field=models.CharField(max_length=25, unique=True, verbose_name='Code'),
        ),
    ]