# Generated by Django 5.0.3 on 2024-03-11 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0004_alter_companies_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requests',
            name='EmployID',
        ),
        migrations.AddField(
            model_name='employees',
            name='RequestID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VacayVue.requests'),
        ),
    ]
