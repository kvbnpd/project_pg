from django.db import models

# Create your models here.
class TypeOfWork(models.Model):  # Class name should follow PascalCase
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
