# Generated by Django 5.0.2 on 2024-04-20 04:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0023_remove_notification_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='incident_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.incidentreport'),
        ),
    ]
