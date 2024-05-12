# forms.py
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


password         = RegexValidator(r"^(?=.*\d)(?=.*[a-zA-Z]).{8,100}$", "Minimum eight characters,must contain one digit and one alphabet")
phone_number     = RegexValidator(r"^(\+?[0-9]{10,15})$", "Please enter valid mobile number")



class SignInForm(forms.Form):
    email        =       forms.EmailField(required=True)
    password     =       forms.CharField(required=True)

    def clean_password(self):
        password    =   self.cleaned_data['password']
        user        =   User.objects.filter(password = password).count()
        if user == 0 and '<script>' in password.lower() or '<>' in password.lower():
            raise forms.ValidationError("Password not contain <script> characters.")        
        return password

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','password', 'name', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PostBlogForm(forms.ModelForm):
    class Meta:
        model = PostBlog
        fields = ['place_name', 'image', 'discription']
    
