from django.urls import path
from . import views

app_name = "main_app"

urlpatterns = [
    path('diary/', views.diary_tab, name='diary'),
    path('profile/', views.profile_tab, name='profile'),
    path('add_product/', views.add_product_tab, name='add_product'),
]