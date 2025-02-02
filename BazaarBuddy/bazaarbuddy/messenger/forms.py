from django import forms
from django.forms import Textarea
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)
        widgets = {
            'content': Textarea(attrs={'placeholder': 'Enter your message here...', 'rows': 5}),
        }