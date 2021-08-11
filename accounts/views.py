from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

orders = Order.objects.all()
products = Product.objects.all()
customers = Customer.objects.all()

# Create your views here.


@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, "accounts/index.html", context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    total_price = 0
    for product in products:
        total_price = product.price + total_price
    context = {
        'products': products,
        'total_price': total_price
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def customers(request, id):
    selected_customer = Customer.objects.get(id=id)
    orders_by_customer = Order.objects.filter(
        customer=selected_customer.id).count()

    orders = Order.objects.filter(customer=selected_customer.id).all()

    # # the filtering
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    # context
    context = {
        'selected_customer': selected_customer,
        'orders_by_customer': orders_by_customer,
        # 'products': products,
        'orders': orders,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    selected_customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),
                           instance=selected_customer)
    form = OrderForm(initial={'customer': selected_customer})
    # checking for submission
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=selected_customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset,
        'selected_customer': selected_customer
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def update_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def create_customer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


# confirming delete decision

@login_required(login_url='login')
def confirm_delete(request, pk):
    order = Order.objects.get(id=pk)
    context = {
        'order': order
    }
    return render(request, 'accounts/delete_confirm.html', context)


@login_required(login_url='login')
def delete(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('/')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"Account Created for {username}")
                return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password Incorrect')
        return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')
