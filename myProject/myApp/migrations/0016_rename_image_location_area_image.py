# Generated by Django 4.2.6 on 2023-11-01 20:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0015_location_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="location",
            old_name="image",
            new_name="area_image",
        ),
    ]