from django.contrib.auth.models import User
from django.db import models
    
class UserProfile(models.Model):
    USER_TYPES = [
        ('regular', 'Regular'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='regular')
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default='pending')

    def __str__(self):
        return f"{self.user.username} ({self.user_type}) - {self.approval_status}"
    
    def is_approved(self):
        return self.approval_status == 'approved'

    def is_moderator(self):
        return self.user_type == 'moderator'