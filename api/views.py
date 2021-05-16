from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.


def apiOverView(request):
    return JsonResponse("API BASE POINT", safe=False)
