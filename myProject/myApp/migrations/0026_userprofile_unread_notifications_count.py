# Generated by Django 5.0.2 on 2024-04-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0025_alter_notification_incident_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='unread_notifications_count',
            field=models.IntegerField(default=0),
        ),
    ]