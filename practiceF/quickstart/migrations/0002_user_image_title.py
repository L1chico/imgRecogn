# Generated by Django 4.2.7 on 2023-11-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_image',
            name='title',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]