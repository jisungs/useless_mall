from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from shop_app.models import Product
from .cart import Cart


def cart_detail(request):
    """장바구니 상세 페이지"""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """장바구니에 상품 추가"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    
    messages.success(request, f'{product.name}이(가) 장바구니에 추가되었습니다!')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """장바구니에서 상품 제거"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    
    messages.success(request, f'{product.name}이(가) 장바구니에서 제거되었습니다.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """장바구니 상품 수량 업데이트"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    
    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    """장바구니 비우기"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, '장바구니가 비워졌습니다.')
    return redirect('cart:cart_detail')