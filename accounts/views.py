"""
Views for accounts app
"""
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(
                request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password are incorrect.')

        context = {}
        return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_user(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
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


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {"products": products})


@login_required(login_url='login')
def customer(request, customer_pk):
    customer = Customer.objects.get(id=customer_pk)
    orders = customer.order_set.all()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'my_filter': my_filter
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def create_order(request, customer_pk):
    order_form_set = inlineformset_factory(
        Customer, Order, fields=('product', 'status', 'note'), extra=10)
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_order(request, order_pk):
    order = Order.objects.get(id=order_pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
