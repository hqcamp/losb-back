# Generated by Django 5.1.2 on 2024-12-09 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0031_messagelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='TGVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.CharField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='tg_verification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='losb.tgverification'),
        ),
    ]
