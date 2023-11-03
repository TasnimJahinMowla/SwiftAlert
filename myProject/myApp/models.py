from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver



class Location(models.Model):
    area_code = models.CharField(max_length=10)
    area_name = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100)
    crime_percentage = models.FloatField(default=0)
    status = models.CharField(max_length=20, default="Safe")

    def __str__(self):
        return self.area_name




class CrimeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class IncidentReport(models.Model):
    description = models.TextField()
    timestamp = models.DateTimeField()
    anonymity_status = models.BooleanField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    crime_type = models.ForeignKey(CrimeType, on_delete=models.CASCADE)

    def __str__(self):
        return f"Incident: {self.description}"

class Notification(models.Model):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE,default="No Report")
    crime_type = models.ForeignKey(CrimeType, on_delete=models.CASCADE)
    alert_message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.alert_message

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='img/%Y', default="No Picture")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    # Add a many-to-many relationship with notifications
    notifications = models.ManyToManyField('Notification', related_name='user_profiles', blank=True)

    def __str__(self):
        return self.user.username

class EmergencyService(models.Model):
    service_type = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=255)
    availability = models.CharField(max_length=50, default="24/7")
    description = models.TextField(default="Emergency Service")
    image = models.ImageField(upload_to='img/%y', default="No Picture")
    email = email = models.EmailField(max_length=255, default="No email")

    def __str__(self):
        return self.service_type

class Criminal(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    criminal_history = models.TextField()
    image = models.ImageField(upload_to='img/%y', default="No Picture")
