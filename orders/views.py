from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.html import escape
from decimal import Decimal
from .models import Order, OrderItem
from cart.cart import Cart


@login_required
def order_create(request):
    """주문 생성"""
    cart = Cart(request)
    
    if not cart:
        messages.warning(request, '장바구니가 비어있습니다.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        # 배송 정보 수집 및 검증
        shipping_name = escape(request.POST.get('shipping_name', '').strip())
        shipping_address = escape(request.POST.get('shipping_address', '').strip())
        shipping_phone = escape(request.POST.get('shipping_phone', '').strip())
        
        # 입력 검증
        if not all([shipping_name, shipping_address, shipping_phone]):
            messages.error(request, '모든 배송 정보를 입력해주세요.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        # 길이 제한 검증
        if len(shipping_name) > 100:
            messages.error(request, '받는 사람 이름은 100자 이하로 입력해주세요.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        if len(shipping_address) > 500:
            messages.error(request, '배송 주소는 500자 이하로 입력해주세요.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        if len(shipping_phone) > 20:
            messages.error(request, '연락처는 20자 이하로 입력해주세요.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        # 주문 생성 (트랜잭션 사용)
        try:
            with transaction.atomic():
                # 주문 총액 계산
                total = cart.get_total_price()
                
                # 주문 생성
                order = Order.objects.create(
                    user=request.user,
                    total=total,
                    shipping_name=shipping_name,
                    shipping_address=shipping_address,
                    shipping_phone=shipping_phone
                )
                
                # 주문 상품 생성
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['price']
                    )
                
                # 장바구니 비우기
                cart.clear()
                
                messages.success(request, f'주문이 성공적으로 생성되었습니다! 주문번호: #{order.id}')
                return redirect('orders:order_detail', order_id=order.id)
                
        except Exception as e:
            messages.error(request, f'주문 생성 중 오류가 발생했습니다: {str(e)}')
            return render(request, 'orders/checkout.html', {'cart': cart})
    
    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    """주문 상세"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    """주문 목록"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def payment_success(request, order_id):
    """결제 성공 페이지 (가짜 결제)"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # 주문 상태를 결제 완료로 변경
    if order.status == 'pending':
        order.status = 'paid'
        order.save()
        messages.success(request, '결제가 완료되었습니다!')
    
    return render(request, 'orders/payment_success.html', {'order': order})