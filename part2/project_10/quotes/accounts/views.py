from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


def register(request):
    print(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return HttpResponse('Такий користувач вже існує')

        user = User.objects.create_user(username=username, email=email, password=password)

        login(request, user)

        return redirect('home')
    else:
        return render(request, 'registration/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Невірні данні')
    else:
        return render(request, 'registration/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('home')