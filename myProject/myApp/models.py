from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    #profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Location(models.Model):
    area_code = models.CharField(max_length=10)
    area_name = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100)  # You can use a more suitable field type.
    
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
    crime_type = models.ForeignKey(CrimeType, on_delete=models.CASCADE)
    alert_message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alert_message
