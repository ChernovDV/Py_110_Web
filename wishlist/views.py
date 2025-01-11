from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from store.models import DATABASE


# Отображение избранного
@login_required(login_url = 'login.login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]
        products = []
        for id_ in data['products']:
            products.append(DATABASE[str(id_)])

        return render(request, 'wishlist/wishlist.html', context={"products": products})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Отображение в Json
@login_required(login_url = 'login.login_view')
def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(request).get(current_user)
        print(data)
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii':False})

        return JsonResponse({"answer":'Пользователь не авторизован'},  json_dumps_params={'ensure_ascii':False})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Добавление в избранное
@login_required(login_url = 'login.login_view')
def wishlist_add_json(request, id_product):
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#  Удаление из избранного
@login_required(login_url = 'login.login_view')
def wishlist_del_json(request, id_product):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404, json_dumps_params={'ensure_ascii': False})  

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@login_required(login_url = 'login.login_view')
def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return redirect('wishlist:wishlist_view')
        return HttpResponseNotFound("Неудачное удаление из избранного")
