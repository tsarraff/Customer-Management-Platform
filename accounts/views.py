from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.
def loginPage(request):
    context = {}
    return render(request,'accounts/login.html', context)

def registerPage(request):
    context = {}
    return render(request, 'accounts/register.html', context)

def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {'orders':orders,'customer':customer, 'total_orders':total_orders,'delivered':delivered,'orders_pending':orders_pending}
    return render(request,'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html', {'products': products})

def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customers':customers,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet= inlineformset_factory(Customer, Order, fields=('product','status'), extra=10)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset= Order.objects.none(), instance=customer)
    if request.method=='POST':
        #print('Printing POST :', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {'item':order}
    if request.method =='POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)