# Generated by Django 4.2.6 on 2023-11-01 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0018_remove_location_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="status",
            field=models.CharField(default="Safe", max_length=20),
        ),
    ]
