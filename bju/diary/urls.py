from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path("", views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('product_edit/<int:entry_id>/', views.product_edit, name='product_edit'),
    path('add_product/', views.add_product, name='add_product'),
]