from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='نام')
    last_name = forms.CharField(max_length=30, required=True, label='نام خانوادگی')
    email = forms.EmailField(required=True, label='ایمیل')
    phone = forms.CharField(max_length=11, required=True, label='تلفن همراه')
    address = forms.CharField(widget=forms.Textarea, required=False, label='آدرس')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری یا ایمیل')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'رمز عبور'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone': 'تلفن',
            'address': 'آدرس',
        }
