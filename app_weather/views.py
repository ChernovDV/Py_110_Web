from django.http import JsonResponse
from django.shortcuts import render
from weather_api import current_weather_api


# Create your views here.
def weather_view(request):
    if request.method == "GET":
        city = request.GET.get('city')
        if city:
            data = current_weather_api(city)
        else:
            data = current_weather_api('Saint-Petersburg')
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})