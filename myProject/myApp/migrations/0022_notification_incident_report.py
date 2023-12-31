# Generated by Django 4.2.6 on 2023-11-03 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0021_userprofile_notifications_alter_userprofile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="incident_report",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="myApp.incidentreport",
            ),
        ),
    ]
