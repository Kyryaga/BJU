from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User 
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'weight', 'height', 'calorie_goal')