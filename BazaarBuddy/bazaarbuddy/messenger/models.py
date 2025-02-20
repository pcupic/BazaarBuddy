from django.contrib.auth.models import User
from django.db import models

from core.models import Product

class Chat(models.Model):
    product = models.ForeignKey(Product, related_name='chats', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-modified_at',)
        
    def __str__(self):
        return f"Chat for {self.product.title}"
    
    @staticmethod
    def get_user_chats(user):
        return Chat.objects.filter(members=user).all()
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)