# Generated by Django 5.1.2 on 2024-10-16 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0005_alter_user_bday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
