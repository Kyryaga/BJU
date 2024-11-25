from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from django import forms
import datetime

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User 
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'weight', 'height', 'calorie_goal')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['weight', 'height', 'calorie_goal']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'calorie_goal': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class DateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'id': 'datePicker',
                                      'name': 'date',
                                      'class': 'date-picker',
                                      }),
        label="Выберите день",
        initial=datetime.date.today
    )


