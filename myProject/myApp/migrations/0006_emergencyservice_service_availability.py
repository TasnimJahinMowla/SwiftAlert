# Generated by Django 4.2.6 on 2023-10-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0005_emergencyservice"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencyservice",
            name="service_availability",
            field=models.CharField(default="24/7", max_length=50),
        ),
    ]