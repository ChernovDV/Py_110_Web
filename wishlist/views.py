from django.contrib.auth import get_user
from django.http import JsonResponse
from django.shortcuts import render

from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from store.models import DATABASE


# from logic.services import view_in_wishlist


# Отображение избранного

def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist()
        format_for_result = request.GET.get('format')

        products = []
        for id_prod  in data.get('products').items():
            product = DATABASE.get[id_prod]
            products.append(product)
        # TODO сформировать список словарей продуктов с их характеристиками
    return render(request, 'wishlist/wishlist.html', context={"products": products})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(request)  # TODO получите данные о списке товаров в избранном у пользователя
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii':False})  # TODO верните JsonResponse c data

        return JsonResponse({"answer":'Пользователь не авторизован'},  json_dumps_params={'ensure_ascii':False})  # TODO верните JsonResponse с ключом "answer" и значением "Пользователь не авторизирован" и параметром status=404

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Добавление в избранное
def wishlist_add_json(request, id_product: str):
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)  # TODO вызовите обработчик из services.py добавляющий продукт в избранное
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Продукт успешно добавлен в избранное"

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Неудачное добавление в избранное" и параметром status=404


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#  Удаление из избранного
def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO вызовите обработчик из services.py удаляющий продукт из избранного
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Продукт успешно удалён из избранного"

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404, json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Неудачное удаление из избранного" и параметром status=404

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

