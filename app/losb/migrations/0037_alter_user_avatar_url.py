# Generated by Django 5.1.2 on 2025-01-14 20:27

import losb.api.v1.services.unique_naming
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0036_phoneverificationsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(blank=True, max_length=512, null=True, upload_to=losb.api.v1.services.unique_naming.unique_upload_to, verbose_name='Аватар'),
        ),
    ]
