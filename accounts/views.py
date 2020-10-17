"""
Views for accounts app
"""
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def home(request):
    orders_all = Order.objects.all()
    orders_last_five = orders_all.order_by('-date_created')[:5]
    customers = Customer.objects.all()

    total_orders = orders_all.count()
    delivered = orders_all.filter(status='DELIVERED').count()
    pending = orders_all.filter(status='PENDING').count()

    context = {
        'orders_last_five': orders_last_five,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {"products": products})


def customer(request):
    return render(request, 'accounts/customer.html')
