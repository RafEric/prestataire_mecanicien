# Generated by Django 5.1.1 on 2024-10-08 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='user_type',
            field=models.CharField(default='prestataire', max_length=20),
        ),
    ]
