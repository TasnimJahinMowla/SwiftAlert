from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Location, IncidentReport

@receiver(pre_delete, sender=Location)
@receiver(pre_delete, sender=IncidentReport)
def update_location_crime_percentage_on_delete(sender, instance, **kwargs):
    if isinstance(instance, Location):
        location = instance
    elif isinstance(instance, IncidentReport):
        location = instance.location

    update_location_crime_percentage(location)

