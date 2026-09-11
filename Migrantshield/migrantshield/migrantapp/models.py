from django.db import models
from datetime import date
class Login(models.Model):
    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, default="contractor")

class PoliceStations(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Contractor(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)  # Foreign key to Login table
    name = models.CharField(max_length=100)
    licenseNo = models.CharField(max_length=15)
   # exp_date = models.DateField()
    aadhaar_card = models.FileField(upload_to="aadhaar_cards/")
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    status = models.CharField(max_length=10, default="Pending")
    work_description=models.TextField()
    police_station=models.ForeignKey('PoliceStations',on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    
    
class UserQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    


STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]


class Migrant(models.Model):
    # Personal Information
    login = models.ForeignKey(Login, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    state = models.CharField(max_length=50,choices=STATE_CHOICES)  # e.g., Kerala
    aadhaar = models.CharField(max_length=12, blank=True, null=True)
    #pcc = models.CharField(max_length=100, blank=True, null=True)  # Police Clearance Certificate
    pcc = models.FileField(upload_to="pcc/")
    photo=models.ImageField(upload_to="photos/")
    # Internal Information (visible only in backend)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Active', 'Active'), ('Inactive', 'Inactive')]) 

    def __str__(self):
        return self.full_name
    
    

class JobBooking(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_phone = models.CharField(max_length=20)
    guest_email = models.EmailField(blank=True, null=True)
    job_description = models.TextField()
    location= models.CharField(max_length=20,)
    landmark= models.TextField()
    booking_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    booked_for=models.DateField(default=date.today)
    def __str__(self):
        return f"Booking by {self.guest_name} for {self.contractor.name}"
    
    
class JobRequest(models.Model):
    public_name = models.CharField(max_length=100)
    public_phone = models.CharField(max_length=15)
    public_email = models.EmailField(blank=True, null=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    description = models.TextField()
    startdate = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.public_name} - {self.contractor.name}"
    
