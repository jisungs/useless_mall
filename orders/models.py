from django.db import models
from django.contrib.auth.models import User
from shop_app.models import Product


class Order(models.Model):
    """주문 모델"""
    
    STATUS_CHOICES = [
        ('pending', '결제 대기'),
        ('paid', '결제 완료'),
        ('shipped', '배송 중'),
        ('delivered', '배송 완료'),
        ('cancelled', '주문 취소'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="주문자")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="총 금액")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="주문 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="주문일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    # 배송 정보
    shipping_name = models.CharField(max_length=100, verbose_name="받는 사람")
    shipping_address = models.TextField(verbose_name="배송 주소")
    shipping_phone = models.CharField(max_length=20, verbose_name="연락처")
    
    class Meta:
        verbose_name = "주문"
        verbose_name_plural = "주문들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"주문 #{self.id} - {self.user.username} ({self.get_status_display()})"
    
    def get_formatted_total(self):
        """총 금액을 원화 형식으로 반환"""
        return f"₩{self.total:,.0f}"


class OrderItem(models.Model):
    """주문 상품 모델"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="주문")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    quantity = models.PositiveIntegerField(verbose_name="수량")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="단가")
    
    class Meta:
        verbose_name = "주문 상품"
        verbose_name_plural = "주문 상품들"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        """상품별 총 금액"""
        return self.quantity * self.price
    
    def get_formatted_price(self):
        """단가를 원화 형식으로 반환"""
        return f"₩{self.price:,.0f}"
    
    def get_formatted_total(self):
        """총 금액을 원화 형식으로 반환"""
        return f"₩{self.get_total_price():,.0f}"