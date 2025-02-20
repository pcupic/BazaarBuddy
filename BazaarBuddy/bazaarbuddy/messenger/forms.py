from django import forms
from django.forms import Textarea
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)
        widgets = {
            'content': Textarea(attrs={
                'placeholder': 'Enter your message...',
                'rows': 3,  
                'class': 'form-control message-input',
                'style': 'resize: none; padding: 8px; font-size: 14px; width: 100%;',  
            }),
        }