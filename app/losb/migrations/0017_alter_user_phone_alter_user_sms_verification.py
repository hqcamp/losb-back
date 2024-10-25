# Generated by Django 5.1.2 on 2024-10-25 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0016_smsverification_remove_user_verification_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='losb.phone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sms_verification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='losb.smsverification'),
        ),
    ]
