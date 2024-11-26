from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, DateForm, ProductWeightForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Diary, ProductsDiaries, Product

from .utils.calcs import calculate_total_bju, calculate_each_product_bju, calc_rsk
from datetime import date, datetime
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
        print(date_selected)
        if date_selected:
            try:
                date_selected = date.fromisoformat(date_selected)
            except ValueError:
                date_selected = datetime.strptime(date_selected, "%b. %d, %Y").date()
        else:
            date_selected = date.today() 
        form = DateForm(initial={'date': date_selected})

    # Проверяем, есть ли дневник на указанную дату
    try:
        diary = Diary.objects.get(user=request.user, date=date_selected)

        if not diary.product_entries.exists():
            diary.delete()
            print(f"Удален пустой дневник за {diary.date}")
        else: 
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

    # Счётчик дней, где достигнута или превышена цель калорий
    calorie_goal_days = 0

    for diary in request.user.diaries.all():
        total_calories = sum(
            entry.product.calories * entry.weight / 100 for entry in diary.product_entries.all()
        )
        if total_calories >= request.user.calorie_goal:
            calorie_goal_days += 1

    # Счетчик средних калорий в день
    total_calories_by_day = 0
    for diary in request.user.diaries.all():
        total_calories_by_day += sum(
            entry.product.calories * entry.weight / 100 for entry in diary.product_entries.all()
        )

    try:
        avg_calories = total_calories_by_day / request.user.diaries.count()
    except ZeroDivisionError:
        avg_calories = 0

    context = {
        'profile_form': profile_form,
        'username': request.user.username,
        'email': request.user.email,
        'age': request.user.age,
        'rsk': request.user.rsk,
        'days_filled': request.user.diaries.count(),
        'goal_riched_days': calorie_goal_days,
        'avg_calories': avg_calories,
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


@login_required
def add_product(request):
    date_selected = request.GET.get('date')
    
    if not date_selected:
        date_selected = date.today()
    else:
        try:
            date_selected = datetime.strptime(date_selected, "%b. %d, %Y").date()
        except ValueError:
            print("НЕКОРЕКТНАЯ ДАТА: ", date_selected)
            return redirect('diary:index')  # Вернуться на страницу дневника, если дата некорректна

    diary, created = Diary.objects.get_or_create(user=request.user, date=date_selected)

    if 'search' in request.GET:
        query = request.GET.get('search')
        print(f"Поисковый запрос: {query}")
        products = Product.objects.filter(name__icontains=query)
        
    else:
        products = Product.objects.all()

    # Отображение даты
    if date_selected == date.today():
        date_display = 'Сегодня'
    else:
        date_display = format_date(date_selected, format="d MMMM yyyy", locale="ru")
   
    context = {
        'date': date_selected,
        'products': products,
        'date_display': date_display,
    }
    return render(request, 'diary/add_product.html', context)


@login_required
def product_card(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    date_selected = request.GET.get('date')
    date_selected = datetime.strptime(date_selected, "%b. %d, %Y").date()

    if request.method == 'POST':
        diary = request.user.diaries.get(date=date_selected)
        form = ProductWeightForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            ProductsDiaries.objects.create(
                diary = diary,
                product=product,
                weight=weight
            )

            return redirect(f"{reverse('diary:index')}?date={date_selected}")
    else:
        form = ProductWeightForm()

    context = {
        'product': product,
        'date': date_selected,
        'form': form,
    }

    return render(request, 'diary/product_card.html', context)