# Generated by Django 5.1.2 on 2024-10-25 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0020_rename_phone_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sms_verification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='losb.smsverification'),
        ),
    ]
