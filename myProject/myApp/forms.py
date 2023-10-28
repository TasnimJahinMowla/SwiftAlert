# forms.py

from django import forms
from .models import *

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['description', 'timestamp', 'anonymity_status', 'location', 'crime_type']
