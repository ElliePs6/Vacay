# Generated by Django 5.0.3 on 2024-03-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='Lastname',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
