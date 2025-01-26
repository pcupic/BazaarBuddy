from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    user_type = forms.ChoiceField(choices=[('regular', 'Regular'), ('moderator', 'Moderator'), ('admin', 'Admin')], required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'user_type']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise forms.ValidationError("Password confirmation does not match.")
        return confirm_password

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Trenutna lozinka")
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Nova lozinka")
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Potvrdi novu lozinku")