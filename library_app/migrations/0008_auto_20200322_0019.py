# Generated by Django 2.2.5 on 2020-03-21 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0007_auto_20200322_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowed',
            name='borrowed_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
