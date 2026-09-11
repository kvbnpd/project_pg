from django import forms

from agentapp.models import NOC_application

class NOCApplicationForm(forms.ModelForm):
    class Meta:
        model = NOC_application
        fields = []  # No fields, just displaying migrant/contractor details
