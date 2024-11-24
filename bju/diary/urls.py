from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path("", views.index, name='index'),
    path('login/', views.login, name='login')
]