from django.shortcuts import get_object_or_404
from shop_app.models import Product


class Cart:
    """세션 기반 장바구니 클래스"""
    
    def __init__(self, request):
        """장바구니 초기화"""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """상품을 장바구니에 추가"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product):
        """상품을 장바구니에서 제거"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """장바구니 아이템들을 반복"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """장바구니에 있는 총 상품 수량"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """장바구니 총 금액"""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """장바구니 비우기"""
        del self.session['cart']
        self.save()
    
    def save(self):
        """세션에 장바구니 저장"""
        self.session.modified = True
