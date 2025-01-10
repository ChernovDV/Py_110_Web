from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from store.models import DATABASE
from logic.services import filtering_category

# Каталог товара с фильтрацией в Json
def products_view(request):
    if request.method == 'GET':
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE.get(id_), json_dumps_params ={'ensure_ascii':False, 'indent':4 })
            return HttpResponseNotFound("Данного продукта нет в базе данных")
        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        reverse_key = request.GET.get('reverse')
        if ordering_key:
            if str(reverse_key).lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                 data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params ={'ensure_ascii':False, 'indent':4 })


# Страница магазина
def shop_view(request):
    if request.method == 'GET':
        # with open('store/shop.html', 'r', encoding='utf-8') as f:
        #     data = f.read()
        # return HttpResponse(data)
        return render(request, 'store/shop.html', context={'products':DATABASE.values()})


# Страница каждого товара в магазине
def products_page_view(request, page):
    if request.method == 'GET':
        if isinstance(page, str):
            for prod in DATABASE.values():
                if prod['html'] == page:
                    with open (f'store/products/{page}.html', encoding='utf-8') as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            prod = DATABASE.get(str(page))
            if prod:
                with open (f'store/products/{prod["html"]}.html', encoding = 'utf-8') as f:
                    data = f.read()
                return HttpResponse(data)

    return HttpResponseNotFound('Продукта не существует')






# Возвращает JSON с корзиной
def cart_view(request):
    if request.method == "GET":
        data = view_in_cart() # TODO Вызвать ответственную за это действие функцию
        format_for_result = request.GET.get('format')
        if format_for_result and format_for_result.lower() == 'json':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,'indent': 4})

        products = []
        for id_prod, count in data.get('products').items():
            product = DATABASE[id_prod]
            product['count'] = count
            product['price_total'] = round(count * product['price_after'], 2)
            products.append(product)
        return render(request, 'store/cart.html', context={'products': products})


# Добавляет в корзину товар по его id_product
def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

# Удаляет товар из корзины по его id_product
def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

# Создаём купон
def coupon_check_view(request, coupon_code):
    DATA_COUPON = \
    {
        "coupon":
        {
            "value": 10,
            "is_valid": True
        },
        "coupon_old":
        {
            "value": 20,
            "is_valid": False
        },
        "coupon_new":
        {
            "value":30,
            "is_valid":True
        },
    }
    if request.method == "GET":
        if coupon_code in DATA_COUPON:
            coupon = DATA_COUPON[coupon_code]
            data = {
                'discount':coupon['value'],
                'is_valid':coupon['is_valid']
            }
            return  JsonResponse(data)
        return HttpResponseNotFound('Неверный купон')


def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 50},
            "fix_price": 100,
        },
        "Бкларусь":{
            'Минск': {'price': 150},
            'Брест': {'price': 200},
            'fix_price': 250
        }
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        country_in_data = DATA_PRICE.get(country)
        city_in_data = country_in_data.get(city)
        if country_in_data:
            if city_in_data:
                return JsonResponse({'price':city_in_data['price']})
            return JsonResponse({'price':country_in_data['fix_price']})
        return HttpResponseNotFound('Неверные данные')

# Добавляем в корзину при нажатии
def cart_buy_now_view(request, id_product):
    if request.method =='GET':
        result  = add_to_cart(id_product)
        if result:
            return redirect('store:cart_view')
        return HttpResponseNotFound('Неудачное добавление товара')

# Удаляем из корзины при нажатии
def cart_remove_view(request, id_product):
        if request.method == "GET":
            result = remove_from_cart(id_product)  # TODO Вызвать функцию удаления из корзины
            if result:
                return redirect('store:cart_view')  # TODO Вернуть перенаправление на корзину
            return HttpResponseNotFound("Неудачное удаление из корзины")