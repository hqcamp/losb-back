# Generated by Django 5.1.2 on 2025-03-06 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0038_user_tg_link_user_vk_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tg_link',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на канал в Telegram'),
        ),
        migrations.AlterField(
            model_name='user',
            name='vk_link',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на канал в VK'),
        ),
    ]
