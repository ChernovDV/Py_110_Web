from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from logic.services import add_users_to_cart, add_users_to_wishlist


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method =='POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data.get('password'))
        if user:
            login(request, user)
            add_users_to_cart(request, user.username)
            add_users_to_wishlist(request, user.username)
            return redirect('/')
        return render(request, 'login/login.html', context={'error': 'Неверный логин или пароль'})

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')