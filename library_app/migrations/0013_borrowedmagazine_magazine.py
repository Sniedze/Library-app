# Generated by Django 2.2.5 on 2020-03-22 20:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import library_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0012_auto_20200322_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('isAvailable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedMagazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_timestamp', models.DateField(default=datetime.datetime.today)),
                ('deadline', models.DateField(default=library_app.models.get_magazine_deadline)),
                ('isReturned', models.BooleanField(default=False)),
                ('magazine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Magazine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
