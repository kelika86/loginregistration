from django.db import models

# Create your models here.
class Pizza(models.Model):
    name= models.CharField(max_length=255)
    price=models.FloatField(max_length=255)
    description=models.TextField()
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
