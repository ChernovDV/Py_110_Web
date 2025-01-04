import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def datetime_view(request):
    if request.method == 'GET':
        return HttpResponse(datetime.datetime.now())