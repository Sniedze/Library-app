# Generated by Django 2.2.5 on 2020-03-27 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowedbook',
            old_name='book',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='borrowedmagazine',
            old_name='magazine',
            new_name='article',
        ),
    ]
