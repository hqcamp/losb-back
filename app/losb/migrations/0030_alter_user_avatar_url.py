# Generated by Django 5.1.2 on 2024-11-07 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0029_alter_phone_number_alter_user_avatar_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(blank=True, max_length=512, null=True, upload_to='user/avatar/', verbose_name='Аватар'),
        ),
    ]
