from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Category, ProductImage

class ProductForm(forms.ModelForm):
    images = forms.CharField(
        required = True,
        widget = forms.Textarea(attrs={'placeholder': 'Add one URL per line', 'rows': 4}),
        help_text = "Provide one or more image URLs, one per line."
    )

    class Meta:
        model = Product
        fields = ['title','description','category','price','condition']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_images(self):
        """Validate the 'images' field to ensure it contains at least one valid URL."""
        data = self.cleaned_data['images']
        image_list = [url.strip() for url in data.splitlines() if url.strip()]
        if not image_list:
            raise forms.ValidationError("Please provide at least one image URL.")
        return image_list

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))