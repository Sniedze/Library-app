# Generated by Django 2.2.5 on 2020-03-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isReserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='magazine',
            name='isReserved',
            field=models.BooleanField(default=False),
        ),
    ]
