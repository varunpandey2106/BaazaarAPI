# Generated by Django 4.2.4 on 2023-09-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_profile_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='auth_provider',
            field=models.CharField(default='email', max_length=255),
        ),
    ]
