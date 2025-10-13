from django.db import models

# Create your models here.

class Category(models.Model):
    """상품 카테고리 모델"""
    name = models.CharField(max_length=100, verbose_name="카테고리명")
    description = models.TextField(blank=True, verbose_name="설명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리들"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """상품 모델 - 계획서에 따라 정적 이미지 경로 사용"""
    name = models.CharField(max_length=200, verbose_name="상품명")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="가격")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="배송비")
    description = models.TextField(verbose_name="상품 설명")
    image_path = models.CharField(max_length=200, verbose_name="이미지 파일명")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="카테고리")
    is_active = models.BooleanField(default=True, verbose_name="판매 중")
    stock_quantity = models.PositiveIntegerField(default=999, verbose_name="재고 수량")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "상품"
        verbose_name_plural = "상품들"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_image_url(self):
        """정적 이미지 URL 반환"""
        return f"/static/img/{self.image_path}"
    
    def get_formatted_price(self):
        """가격을 원화 형식으로 반환"""
        return f"₩{self.price:,.0f}"
    
    def get_formatted_shipping_fee(self):
        """배송비를 원화 형식으로 반환"""
        if self.shipping_fee == 0:
            return "무료배송"
        return f"₩{self.shipping_fee:,.0f}"
    
    def get_total_price(self):
        """상품 가격 + 배송비 총액 반환"""
        return self.price + self.shipping_fee
    
    def get_formatted_total_price(self):
        """총 가격을 원화 형식으로 반환"""
        return f"₩{self.get_total_price():,.0f}"
    
    def get_stock_status(self):
        """재고 상태를 반환"""
        if self.stock_quantity == 0:
            return "품절"
        elif self.stock_quantity <= 10:
            return "재고부족"
        elif self.stock_quantity <= 50:
            return "재고적음"
        else:
            return "충분"
    
    def get_stock_status_class(self):
        """재고 상태에 따른 CSS 클래스 반환"""
        status = self.get_stock_status()
        if status == "품절":
            return "bg-danger"
        elif status == "재고부족":
            return "bg-warning"
        elif status == "재고적음":
            return "bg-info"
        else:
            return "bg-success"
    
    def is_in_stock(self):
        """재고가 있는지 확인"""
        return self.stock_quantity > 0
    
    def is_low_stock(self):
        """재고가 부족한지 확인 (10개 이하)"""
        return self.stock_quantity <= 10
    
    def can_purchase(self, quantity=1):
        """지정된 수량만큼 구매 가능한지 확인"""
        return self.stock_quantity >= quantity
    
    def reduce_stock(self, quantity):
        """재고 차감 (주문 시 사용)"""
        if self.can_purchase(quantity):
            self.stock_quantity -= quantity
            self.save()
            return True
        return False
    
    def add_stock(self, quantity):
        """재고 추가 (관리자가 재고 보충 시 사용)"""
        self.stock_quantity += quantity
        self.save()
        return True
