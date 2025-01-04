from django.http import JsonResponse
from django.shortcuts import render
from weather_api import current_weather_api


# Create your views here.
def weather_view(request):
    if request.method == "GET":
        data = current_weather_api('Moscow')  # Результат работы функции current_weather
        # А возвращаем объект JSON. Параметр json_dumps_params используется, чтобы передать ensure_ascii=False
        # как помните это необходимо для корректного отображения кириллицы
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})