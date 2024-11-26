from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, DateForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Diary, ProductsDiaries

from .utils.calcs import calculate_total_bju, calculate_each_product_bju, calc_rsk
from datetime import date
from babel.dates import format_date


@login_required
def index(request):
    products = None
    message = None
    enriched_products = None
    total_bju = None

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date_selected = form.cleaned_data['date']
            # обновление параметра date после каждого переключения
            return redirect(f"{reverse('diary:index')}?date={date_selected}")
    else:
        date_selected = request.GET.get('date')
        if date_selected:
            try:
                date_selected = date.fromisoformat(date_selected)
            except ValueError:
                date_selected = date.today() 
        else:
            date_selected = date.today() 
        form = DateForm(initial={'date': date_selected})

    # Проверяем, есть ли дневник на указанную дату
    try:
        diary = Diary.objects.get(user=request.user, date=date_selected)
        products = diary.product_entries.all()  # Получаем все записи продуктов из дневника

        # расчет bju для каждого продукта с учетом веса
        enriched_products = calculate_each_product_bju(products)

        calc_rsk(enriched_products, request.user.rsk)

        # расчет total bju
        total_bju = calculate_total_bju(enriched_products, request.user.calorie_goal)

    except Diary.DoesNotExist:
        message = "Дневник пуст! Добавьте продукты кнопкой +"

    # Отображение даты
    if date_selected == date.today():
        date_display = 'Сегодня'
    else:
        date_display = format_date(date_selected, format="d MMMM yyyy", locale="ru")

    context = {
        'form': form,
        'products': enriched_products,
        'message': message,
        'total_bju': total_bju,
        'date': date_display,
    }
    return render(request, 'diary/diary.html', context)



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                # Получаем значение 'next' из параметра запроса
                next_url = request.GET.get('next')
                if next_url:  # Если параметр 'next' существует
                    return redirect(next_url)
                else:  # Если параметра 'next' нет, перенаправляем на главную страницу дневника
                    return redirect('diary:index')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'diary/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary:login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}

    return render(request, 'diary/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('diary:profile')  
    else:
        profile_form = UserProfileForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'username': request.user.username,
        'email': request.user.email,
        'age': request.user.age,
        'rsk': request.user.rsk,
    }
    return render(request, 'diary/profile.html', context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('diary:index'))


@login_required
def product_edit(request, entry_id):
    entry = get_object_or_404(ProductsDiaries, id=entry_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            entry.delete()
            return redirect(f"{reverse('diary:index')}?date={entry.diary.date}")
        elif 'save' in request.POST:
            entry.weight = request.POST.get('weight')
            entry.save()
            return redirect(f"{reverse('diary:index')}?date={entry.diary.date}")

    if entry.diary.date == date.today():
        display_date = 'Сегодня'
    else:
        display_date = format_date(entry.diary.date, format="d MMMM yyyy", locale="ru")

    context = {'entry': entry,
               'date': display_date,
               }
    return render(request, 'diary/edit.html', context)
