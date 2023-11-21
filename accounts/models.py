
from django.db import models
from django.contrib.auth.models import AbstractUser


# Extend the User model with additional fields like "role"
class CustomUser(AbstractUser):
    # Define your roles here, you can add more as needed
    ROLE_CHOICES = (

        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('user', 'User'),
        ('educational_center', 'Educational Center'),
    )

    # Add a field to store the role of the user
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Add any other custom fields or methods related to users here

