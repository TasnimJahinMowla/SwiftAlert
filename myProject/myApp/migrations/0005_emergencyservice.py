# Generated by Django 4.2.6 on 2023-10-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0004_notification_is_read"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmergencyService",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("service_type", models.CharField(max_length=100)),
                ("contact_information", models.CharField(max_length=255)),
            ],
        ),
    ]
