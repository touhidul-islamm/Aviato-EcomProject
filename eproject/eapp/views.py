from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    catagory=Catagory.objects.all()
    product=Product.objects.all()
    context={
        'catagory': catagory,
        'product': product
    }
    return render(request, 'index.html', context)


def productdetails(request, pk):
    product_d=Product.objects.get(pk=pk)
    related_product=Product.objects.filter(Q(catagory__name= product_d.catagory.name)|Q(brand=product_d.brand)).exclude(pk=pk)
    context={
        'product_d':product_d,
        
        'related_product': related_product
    }
    return render(request, 'product-details.html', context)


def product_search(request):
    query= request.GET['q']
    product_s=Product.objects.filter(Q(name__icontains=query)|Q(catagory__name__icontains=query)|Q(price_range__icontains=query))

    context={
        'product_s': product_s

    }
    return render(request, 'product_search.html', context)

@login_required(login_url='login')
def add_to_cart(request,pk):
    product=get_object_or_404(Product, pk=pk)
    cart_item, created=Cart_product.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item.quantity +=1
            cart_item.save()
            messages.info(request, 'This item was add to cart')
            return redirect('productdetails', pk=pk)
        else:
            order.cart_product.add(cart_item)
            messages.info(request, 'This item was add to cart')
            return redirect('productdetails', pk=pk)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.cart_product.add(cart_item)
        messages.info(request, 'This item quantity was updated')
        return redirect('productdetails', pk=pk)
    

def remove_cart(request,pk):
    product=get_object_or_404(Product, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item=Cart_product.objects.filter(user=request.user, ordered=False)[0]
            cart_item.delete()
            messages.info(request,'product is deleted')
            return redirect('cart_summary')
    else:
        messages.info(request,'The product is empty')
        return redirect('/')


def cart_increment(request,pk):
    product=get_object_or_404(Product, pk=pk)
    cart_item, created=Cart_product.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item.quantity +=1
            cart_item.save()
            messages.info(request,'The product quantity is updated')
            return redirect('cart_summary')

    else:
        messages.info(request, 'The product quantity was updated')
        return redirect('cart_summary')
    
def cart_decrement(request,pk):
    product=get_object_or_404(Product, pk=pk)
    cart_item, created=Cart_product.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk,).exists():
            if cart_item.quantity>1:
                cart_item.quantity -=1
                cart_item.save()
                messages.info(request,'The product quantity is removed')
                return redirect('cart_summary')
            else:
                cart_item.delete()
                messages.info(request,'The product is deleted')
                return redirect('cart_summary')
            

    

@login_required(login_url='login')
def cart_summary(request):
    try:
        order=Order.objects.get(user=request.user, ordered=False)
        context={
            'order':order
        }
        return render(request, 'cart_summary.html', context)
    except ObjectDoesNotExist:
        messages.error(request,'Your cart is empty')
        return redirect('/')
    
