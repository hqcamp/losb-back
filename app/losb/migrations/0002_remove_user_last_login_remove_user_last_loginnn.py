# Generated by Django 5.1.2 on 2024-10-16 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_loginnn',
        ),
    ]
