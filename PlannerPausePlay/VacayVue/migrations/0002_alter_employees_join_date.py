# Generated by Django 5.0.3 on 2024-03-28 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='join_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
