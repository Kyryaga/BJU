from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return HttpResponse("<h3>index</h3>")


def login(request):
    return HttpResponse("<p>Страница логина</p>")