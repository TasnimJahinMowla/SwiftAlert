# forms.py

from django import forms
from .models import *
from django.forms import modelform_factory
from django.apps import apps

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['description', 'timestamp', 'anonymity_status', 'location', 'crime_type']



def get_dynamic_model_form(model):
    return modelform_factory(model, exclude=['id'])

# Add any custom form methods, validations, or widgets here

# Example of using a custom form
class CustomIncidentReportForm(forms.ModelForm):
    # Add any custom form methods, validations, or widgets here

    class Meta:
        model = IncidentReport
        exclude = ['id']