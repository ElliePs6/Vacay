# Generated by Django 5.0.3 on 2024-03-29 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0005_alter_employee_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
