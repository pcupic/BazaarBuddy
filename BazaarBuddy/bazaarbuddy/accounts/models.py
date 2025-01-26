from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPES = [
        ('regular', 'Regular'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='regular')

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"