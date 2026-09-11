from django.db import models
from migrantapp.models import Migrant,Contractor# Create your models here.
class NOC_application(models.Model):
    migrant=models.ForeignKey('migrantapp.Migrant',on_delete=models.CASCADE)
    applied_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,default="Pending")
class NOC_table(models.Model):
    Migrant=models.ForeignKey('migrantapp.Migrant',on_delete=models.CASCADE)
    issued_date=models.DateTimeField(auto_now_add=True)
    noc=models.FileField(upload_to='NOC/')
   
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Migrant'], name='unique_noc_per_migrant')
        ]

    
    
    
    
    
    
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    migrant_ids = models.TextField()  # Store migrant IDs as CSV

    def __str__(self):
        return f"₹{self.amount} on {self.date.strftime('%Y-%m-%d')}"
from django.db import models
#for work entry


class JobDetails(models.Model):  
    contractor = models.ForeignKey('migrantapp.Contractor', on_delete=models.CASCADE)
    startdate = models.DateField()
    description = models.TextField()
    venue = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,default="Open")
    def __str__(self):
        return f"Job at {self.venue} starting on {self.startdate}"



class WorkEntry(models.Model):
    migrant = models.ForeignKey('migrantapp.Migrant',on_delete=models.CASCADE)
    jobdetails = models.ForeignKey(JobDetails, on_delete=models.CASCADE)

    date = models.DateField()
    

    def __str__(self):
        return f"{self.migrant.full_name} - {self.date}"
    
class SalaryPayment(models.Model):
    migrant = models.ForeignKey('migrantapp.Migrant',on_delete=models.CASCADE)
    contractor = models.ForeignKey('migrantapp.Contractor', on_delete=models.CASCADE)
 
    month = models.IntegerField()  # 1 - January, 2 - February, etc.
    year = models.IntegerField()
    total_days = models.IntegerField()
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Salary for {self.migrant.full_name} - {self.month}/{self.year}"
    
    from django.db import models

class MigrantIDCard(models.Model):
    migrant = models.OneToOneField(Migrant, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='id_cards/', blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
