from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category

def home(request):
    """홈페이지 - 최신 8개 상품 표시"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    context = {
        'products': products
    }
    return render(request, 'home.html', context)

def product_list(request):
    """상품 목록 페이지"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'product_list.html', context)

def product_detail(request, product_id):
    """상품 상세 페이지"""
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)