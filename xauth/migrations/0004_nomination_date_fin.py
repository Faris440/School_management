# Generated by Django 5.0.4 on 2024-11-14 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xauth', '0003_nomination_is_desactivate'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='date_fin',
            field=models.DateField(null=True),
        ),
    ]
