"""
Views for accounts app
"""
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'accounts/dashboard.html')


def products(request):
    return render(request, 'accounts/products.html')


def customer(request):
    return render(request, 'accounts/customer.html')
