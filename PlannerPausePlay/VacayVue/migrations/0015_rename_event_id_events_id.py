# Generated by Django 5.0.3 on 2024-03-15 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0014_alter_requests_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='event_id',
            new_name='id',
        ),
    ]
