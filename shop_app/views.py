from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.utils.html import escape
from .models import Product, Category

def home(request):
    """홈페이지 - 모든 활성 상품 표시"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')
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

def product_search(request):
    """상품 검색 페이지"""
    query = escape(request.GET.get('q', '').strip())
    products = Product.objects.filter(is_active=True)
    
    # 검색어 길이 제한
    if len(query) > 100:
        query = query[:100]
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    context = {
        'products': products,
        'query': query,
        'results_count': products.count()
    }
    return render(request, 'product_search.html', context)