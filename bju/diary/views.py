from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, WeightForm, HeightForm, CalorieGoalForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


@login_required
def index(request):
    return render(request, 'diary/diary.html')


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
        # Обработка обновления веса
        if 'update_weight' in request.POST:
            weight_form = WeightForm(request.POST, instance=request.user)
            if weight_form.is_valid():
                weight_form.save()
                return redirect('diary:profile')
        else:
            weight_form = WeightForm(instance=request.user)

        # Обработка обновления роста
        if 'update_height' in request.POST:
            height_form = HeightForm(request.POST, instance=request.user)
            if height_form.is_valid():
                height_form.save()
                return redirect('diary:profile')
        else:
            height_form = HeightForm(instance=request.user)

        # Обработка обновления цели по калориям
        if 'update_calorie_goal' in request.POST:
            calorie_goal_form = CalorieGoalForm(request.POST, instance=request.user)
            if calorie_goal_form.is_valid():
                calorie_goal_form.save()
                return redirect('diary:profile')
        else:
            calorie_goal_form = CalorieGoalForm(instance=request.user)
    else:
        weight_form = WeightForm(instance=request.user)
        height_form = HeightForm(instance=request.user)
        calorie_goal_form = CalorieGoalForm(instance=request.user)

    context = {
        'weight_form': weight_form,
        'height_form': height_form,
        'calorie_goal_form': calorie_goal_form,
        'username': request.user.username,
    }
    return render(request, 'diary/profile.html', context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('diary:index'))