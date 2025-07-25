# Generated by Django 5.2.4 on 2025-07-12 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrescriptionAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='prescription_attachments/')),
                ('attachment_type', models.CharField(choices=[('lab_report', 'Lab Report'), ('imaging_scan', 'Imaging Scan'), ('other', 'Other')], default='other', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='prescriptions.prescription')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_prescription_attachments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Prescription Attachment',
                'verbose_name_plural': 'Prescription Attachments',
                'db_table': 'prescription_attachments',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
