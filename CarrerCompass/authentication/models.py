from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# User model
class User(AbstractUser):
    # Create a user model that contains (username, email, image and type)
    username = models.CharField(max_length=20, unique=False, blank=False, null=False)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=[
        ('employee', 'Employee'),
        ('employer', 'Employer')
    ], default='employee')
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    
    # Defining username filed
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    # string representation
    def __str__(self):
        return f"{self.username} {self.email} {self.user_type}"
    