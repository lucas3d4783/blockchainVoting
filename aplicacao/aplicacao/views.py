# _*_ coding: utf-8 _*_ 
from django.shortcuts import render

def index(request): 
    return render(request, 'index.html')