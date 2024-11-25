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

# FOR PROFILE
class WeightForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['weight']

class HeightForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['height']

class CalorieGoalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['calorie_goal']


class DateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'id': 'datePicker',
                                      'name': 'date',
                                      'class': 'date-picker',
                                      }),
        label="Выберите день",
        initial=datetime.date.today
    )


