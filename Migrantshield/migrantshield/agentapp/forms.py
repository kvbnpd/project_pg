from django import forms
from .models import*
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = JobDetails
        fields = [ 'startdate', 'description', 'venue']
        widgets = {
            'startdate': forms.DateInput(attrs={'type': 'date'}),
        }
class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ['date', 'migrant', 'jobdetails']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }