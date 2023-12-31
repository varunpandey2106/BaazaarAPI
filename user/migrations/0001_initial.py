# Generated by Django 4.2.4 on 2023-08-25 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('profile_picture', models.ImageField(blank=True, upload_to=user.models.user_directory_path)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('birth_date', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
