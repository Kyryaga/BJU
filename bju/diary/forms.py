from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from django import forms
import datetime

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User 
        fields = ('username', 'password')
        widgets = {
            'username': forms.NumberInput(attrs={'class': 'form-control'}),
            'password': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'weight', 'height', 'calorie_goal')
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['weight', 'height', 'calorie_goal', 'age']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 20, 'max': 300}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'min': 100, 'max': 250}),
            'calorie_goal': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 7, 'max': 90}),
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



class ProductWeightForm(forms.Form):
    weight = forms.FloatField(
        min_value=1,  
        label="",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите вес в граммах',
            'class': 'weight-input',
        }),
        error_messages={
            'required': 'Это поле обязательно.',
            'min_value': 'Вес должен быть больше 0.',
            'invalid': 'Введите корректное число.',
        }
    )