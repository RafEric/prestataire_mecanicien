# Generated by Django 5.1.1 on 2024-10-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_clientprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientprofile',
            name='user_type',
            field=models.CharField(max_length=20),
        ),
    ]
