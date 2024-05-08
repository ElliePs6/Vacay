# Generated by Django 5.0.3 on 2024-05-08 08:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VacayVue', '0005_alter_leavetype_reset_month_delete_leavebalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_days', models.PositiveIntegerField(default=0)),
                ('used_days', models.PositiveIntegerField(default=0)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VacayVue.leavetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
