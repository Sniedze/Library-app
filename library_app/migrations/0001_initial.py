# Generated by Django 2.2.5 on 2020-03-27 14:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import library_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(blank=True, max_length=150)),
                ('isAvailable', models.BooleanField(default=True)),
                ('isReserved', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(blank=True, max_length=150)),
                ('isAvailable', models.BooleanField(default=True)),
                ('isReserved', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BorrowedMagazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_timestamp', models.DateField(default=datetime.datetime.today)),
                ('deadline', models.DateField(default=library_app.models.get_magazine_deadline)),
                ('status', models.CharField(default='', max_length=15)),
                ('magazine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Magazine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_timestamp', models.DateField(default=datetime.datetime.today)),
                ('deadline', models.DateField(default=library_app.models.get_deadline)),
                ('status', models.CharField(default='', max_length=15)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
