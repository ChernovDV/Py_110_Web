from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from store.models import DATABASE


# Create your views here.
def products_view(request):
    if request.method == 'GET':
        return JsonResponse(DATABASE, json_dumps_params ={'ensure_ascii':False, 'indent':4 })

def shop_view(request):
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            data = f.read()
    return HttpResponse(data)