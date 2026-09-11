from django.db import models
from migrantapp.models import Migrant
# Create your models here.
class CrimeReport(models.Model):
    firnumber=models.CharField(max_length=255)
    migrant = models.ForeignKey('migrantapp.Migrant', on_delete=models.CASCADE)
    crime_type = models.CharField(max_length=255)  # Type of crime (e.g., Theft, Violence, Fraud)
    description = models.TextField()  # Details about the crime
    date_reported = models.DateField(auto_now_add=True)  # Auto-set to the current date
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Under Investigation', 'Under Investigation'),
            ('Resolved', 'Resolved')
        ],
        default='Pending'
    )
    reported_by = models.CharField(max_length=255)  # Name of the person/authority reporting
    reported_at =models.CharField(max_length=255) # Name of the police station reporting
    resolving_note=models.TextField(blank=True, null=True) 
    def __str__(self):
        return f"Crime Report: {self.migrant.full_name} - {self.crime_type}"
