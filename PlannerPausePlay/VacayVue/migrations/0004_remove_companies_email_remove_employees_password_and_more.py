# Generated by Django 5.0.3 on 2024-03-21 11:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0003_remove_employees_firstname_remove_employees_lastname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='Password',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='Role',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='Username',
        ),
        migrations.AddField(
            model_name='companies',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employees',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('company', 'Company')], default='employee', max_length=20),
        ),
    ]
