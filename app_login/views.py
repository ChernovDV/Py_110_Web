from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")
    if request.method =='POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data.get('password'))
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'login/login.html', context={'error': 'Неверный логин или пароль'})

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')