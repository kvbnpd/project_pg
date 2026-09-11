from django import forms
from .models import*
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from .models import JobBooking


class ContractorForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    aadhaar_card = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    licenseNo = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #exp_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    district = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Contractor
        exclude = ["status", "login"]  # Excluding 'status' and 'login'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Login.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and not re.match("^[A-Za-z ]+$", name):
            raise forms.ValidationError("Name should contain only alphabets.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not re.match("^[0-9]{10}$", phone):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_licenseNo(self):
        licenseNo = self.cleaned_data.get("licenseNo")
        if licenseNo and not re.match("^[A-Za-z0-9]{5,15}$", licenseNo):
            raise forms.ValidationError("License number should be alphanumeric and 5-15 characters long.")
        return licenseNo
class loginForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control fs-6 py-3 px-4 form-control-lg',
            'placeholder': 'Your Email',
            'required': 'required'
        }),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control fs-6 py-3 px-4 form-control-lg',
            'placeholder': 'Your Password',
            'required': 'required'
        }),
        label="Password"
    )

    class Meta:
        model = Login
        fields = ['email', 'password']
        

# user contact messages---------------------------

class UserQueryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control fs-6 py-3 px-4 form-control-lg',
            'placeholder': 'Your Name',
            'required': 'required'
        }),
        label="Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control fs-6 py-3 px-4 form-control-lg',
            'placeholder': 'Your Email',
            'required': 'required'
        }),
        label="Email"
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control fs-6 py-3 px-4 form-control-lg',
            'placeholder': 'Subject of the Query',
            'required': 'required'
        }),
        label="Subject"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control fs-6 py-3 px-4 form-control-lg',
            'placeholder': 'Your Message',
            'required': 'required',
            'rows': 4
        }),
        label="Message"
    )

    class Meta:
        model = UserQuery
        fields = ['name', 'email', 'subject', 'message']
        
        
class MigrantForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    age = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    aadhaar = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Migrant
        fields = '__all__'
        exclude = ["status", "registered_at","login"]
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Login.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        age = cleaned_data.get("age")
        phone = cleaned_data.get("phone")
        aadhaar = cleaned_data.get("aadhaar")
        full_name = cleaned_data.get("full_name")

        # Validate Password Match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        # Validate Name (Only Alphabets)
        if full_name and not re.match("^[A-Za-z ]+$", full_name):
            self.add_error('full_name', "Name should contain only alphabets")

        # Validate Age (Between 18 and 90)
        if age and (age < 18 or age > 90):
            self.add_error('age', "Age must be between 18 and 90")

        # Validate Phone Number (Exactly 10 Digits)
        if phone and not re.match("^[0-9]{10}$", phone):
            self.add_error('phone', "Phone number must be exactly 10 digits")

        # Validate Aadhaar Number (Exactly 12 Digits)
        if aadhaar and aadhaar.strip():  # Check only if Aadhaar is entered
            if not re.match("^[0-9]{12}$", aadhaar):
                self.add_error('aadhaar', "Aadhaar number must be exactly 12 digits")

        return cleaned_data
class JobBookingForm(forms.ModelForm):
    class Meta:
        model = JobBooking  # Make sure JobBooking is correctly imported
        fields = ['guest_name', 'guest_phone', 'guest_email', 'contractor', 'job_description', 'booked_for']
        widgets = {
            'booked_for': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }