from django.db import models
from migrantapp.models import Contractor,Migrant
# Create your models here.
from django.db import models

class Application_request(models.Model):
    contractor = models.ForeignKey('migrantapp.Contractor', on_delete=models.CASCADE)
    migrant = models.ForeignKey('migrantapp.Migrant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revoked','Revoked')
        ],
        default='pending'
    )

    def __str__(self):
        return f"Application {self.id} - {self.status}"
