"""
Views for accounts app
"""
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('Home Page')


def products(request):
    return HttpResponse('Products Page')


def customer(request):
    return HttpResponse('Customer Page')
