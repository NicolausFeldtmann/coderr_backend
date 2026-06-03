from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Defines UserProfiles and containing informations."""

    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, default="")
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=30, default="", blank=True)
    tel = models.CharField(max_length=30, default="", blank=True)
    description = models.TextField(max_length=100, default="", blank=True)
    working_hours = models.CharField(max_length=20, default="", blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username