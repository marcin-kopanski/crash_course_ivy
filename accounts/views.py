"""
Views for accounts app
"""
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from .forms import OrderForm


def home(request):
    orders_all = Order.objects.all()
    orders_last_five = orders_all.order_by('-date_created', '-id')[:5]
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


def customer(request, customer_pk):
    customer = Customer.objects.get(id=customer_pk)
    orders = customer.order_set.all()

    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'accounts/customer.html', context)


def create_order(request, customer_pk):
    order_form_set = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=customer_pk)
    formset = order_form_set(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = order_form_set(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, order_pk):
    order = Order.objects.get(id=order_pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, order_pk):
    order = Order.objects.get(id=order_pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
