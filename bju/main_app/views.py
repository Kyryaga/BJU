from django.shortcuts import render
from .models import *
from django.http import HttpResponse


# тест всей функциональности созданной базы данных перед началом программирования бэка
# 1) Добавление продуктов админом                               (+)
# 2) Создание юзером дневника дня                               (+)
# 3) Добавление в дневник продуктов                             (+)
# 4) Добавление к дневнику уже существующего продукта           (+)
# ...

# Diary: READ
def diary_tab(request):
    return HttpResponse('<h1>ДНЕВНИК</h1>')

# Profile: READ
def profile_tab(request):
    return HttpResponse('<h1>Профиль</h1>')

# Add product: READ
def add_product_tab(request):
    return HttpResponse('<h1>Добавить</h1>')