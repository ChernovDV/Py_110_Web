import json
import os

from django.contrib.auth import get_user
from store.models import DATABASE

# Фильтр товара
def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [prod for prod in DATABASE.values() if prod['category'] == category_key]  #  TODO При помощи фильтрации в list comprehension профильтруйте товары по категории (ключ 'category') в продукте database. Или можете использовать
        # обычный цикл или функцию filter. Допустим фильтрацию в list comprehension можно сделать по следующему шаблону
        # [product for product in database.values() if ...] подумать, что за фильтрующее условие можно применить.
        # Сравните значение категории продукта со значением category_key
    else:
        result = [prod for prod in DATABASE.values()] #  TODO Трансформируйте словарь словарей database в список словарей
        # В итоге должен быть [dict, dict, dict, ...], где dict - словарь продукта из database
    if ordering_key is not None:
        ... #  TODO Проведите сортировку result по ordering_key и параметру reverse
        # Так как result будет списком, то можно применить метод sort, но нужно определиться с тем по какому элементу сортируем и в каком направлении
        # result.sort(key=lambda ..., reverse=reverse)
        # Вспомните как можно сортировать по значениям словаря при помощи lambda функции

        result.sort(key=lambda x: x.get(ordering_key), reverse=reverse)
    return result
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Просмотреть содержимое корзины
def view_in_cart(request) -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)
    user = get_user(request).username
    cart = {user:{'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Добавить товар в корзину
def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # Текущая корзина

    # ! Обратите внимание, что в переменной cart находится словарь с ключом products.
    # ! Именно в cart["products"] лежит словарь гдк по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой id_product товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.
    if id_product not in cart['products']:
        if not DATABASE.get(id_product):
            return False
    # TODO Если товар существует, то увеличиваем его количество на 1

        cart['products'][id_product] = 1   # Если товара еще нет в корзине, добавляем его с количеством 1
    else:
        cart['products'][id_product] += 1  # Иначе +1
    # TODO Не забываем записать обновленные данные cart в 'cart.json'. Так как именно из этого файла мы считываем данные и если мы не запишем изменения, то считать измененные данные не получится.
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)
    return True

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Удаляет товар из корзины
def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)  # TODO Помните, что у вас есть уже реализация просмотра корзины,
    cart = cart_users[get_user(request).username]
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # С переменной cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.
    if id_product not in cart["products"]:
        return False  # Товара нет в корзине, удаление невозможно
    # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].
    cart["products"].pop(id_product)  # Удаляем товар из корзины
    # TODO Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)
    return True
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def add_users_to_cart(request, username):
    cart_users = view_in_cart(request)
    cart = cart_users.get(username)

    if not cart:
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products':{}}
            json.dump(cart_users, f)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def add_users_to_wishlist(request, username):
    wishlist_users = view_in_cart(request)
    wishlist = wishlist_users.get(username)

    if not wishlist:
        with open('cart.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products':{}}
            json.dump(wishlist_users, f)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





def view_in_wishlist(request):
    """
    Просматривает содержимое wishlist.json

    :return: Содержимое 'wishlist.json'
    """
    if os.path.exists('wishlist.json'):  # Если файл существует
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username
    wishlist = {user: {'products': []}}  # Создаём пустой лист
    with open('wishlist.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(wishlist, f)

    return wishlist
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def add_to_wishlist(request, id_product):
    user_wishlist = view_in_wishlist(request)
    wishlist = user_wishlist[get_user(request).username]
    if id_product not in wishlist['products']:
        if not DATABASE.get(id_product):
            return False
        wishlist['products'].append(id_product)   # Если товара еще нет в корзине, добавляем его с количеством 1
    else:
        return False
    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(user_wishlist, f)
    return True
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
def remove_from_wishlist(request, id_product):
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра листа,

    # TODO Проверьте, а существует ли такой товар в листе, если нет, то возвращаем False.
    if id_product not in wishlist["products"]:
        return False  # Товара нет в листе, удаление невозможно

    wishlist['products'].remove(id_product)

    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)
    return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def add_user_to_wishlist(request, username):
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users.get(username)

    if not wishlist:
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products':[]}
            json.dump(wishlist_users, f)