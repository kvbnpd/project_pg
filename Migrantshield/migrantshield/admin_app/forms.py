from django import forms

class RespondQueryForm(forms.Form):
    response = forms.CharField(
        label="Your Response",
        widget=forms.Textarea(attrs={
            'class': 'form-control',          # Bootstrap class
            'rows': 6,
            'placeholder': 'Type your response here...',
            'style': 'margin-top: 10px;'
        }),
        max_length=2000,
    )
