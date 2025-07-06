
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hi.. I am from Home")
