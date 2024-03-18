from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .models import MyUser


@login_required(login_url='/auth/login')
def logout_view(request):
    logout(request)
    return redirect('/auth/login')


def login_view(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            _next = request.GET.get('next', '/')
            return redirect(_next)

    return render(request, 'signin.html')


def register_view(request):
    if request.method == "POST":
        data = request.POST
        if data['password1'] != data['password2']:
            return render(request, 'signup.html')
        user = User.objects.create(username=data['username'], password=make_password(data['password1']))
        user.save()
        user = MyUser.objects.create(user_id=user.id)
        user.save()
        return redirect('/auth/login')

    return render(request, 'signup.html')
