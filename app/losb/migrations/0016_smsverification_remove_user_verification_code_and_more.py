# Generated by Django 5.1.2 on 2024-10-24 23:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0015_verificationcode_remove_phone_vc_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('attempts', models.SmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
        migrations.AddField(
            model_name='user',
            name='sms_verification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user', to='losb.smsverification'),
        ),
        migrations.DeleteModel(
            name='VerificationCode',
        ),
    ]
