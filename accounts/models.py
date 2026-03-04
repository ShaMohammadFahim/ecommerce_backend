from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
   
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(AbstractUser):
  
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        role_name = self.role.name if self.role else "No Role"
        return f"{self.username} ({role_name})"