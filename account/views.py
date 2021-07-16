from django.shortcuts import render
from .models import *
from django.http import HttpResponse

def loginView(request):
    return HttpResponse('<h1 style="color: red"> Test </h1>')