# Generated by Django 4.2.6 on 2023-10-28 20:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0010_emergencyservice_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emergencyservice",
            name="image",
            field=models.ImageField(default="No Picture", upload_to="static/images/"),
        ),
    ]
