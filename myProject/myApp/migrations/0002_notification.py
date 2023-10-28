# Generated by Django 4.2.6 on 2023-10-28 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                ("alert_message", models.CharField(max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "crime_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myApp.crimetype",
                    ),
                ),
            ],
        ),
    ]