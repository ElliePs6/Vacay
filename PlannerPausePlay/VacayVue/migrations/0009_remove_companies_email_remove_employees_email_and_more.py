# Generated by Django 5.0.3 on 2024-03-22 14:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0008_rename_employid_employees_employeeid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='email',
        ),
        migrations.AddField(
            model_name='companies',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='companies_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
