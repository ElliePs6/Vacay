# Generated by Django 5.0.3 on 2024-03-21 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0004_remove_companies_email_remove_employees_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employees',
            name='join_date',
        ),
    ]
