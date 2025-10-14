from django.db import models
from django.contrib.auth.models import User

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
    
    # 평점 관련 메서드들
    def get_average_rating(self):
        """평균 평점 계산"""
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return round(sum(review.rating for review in reviews) / reviews.count(), 1)
    
    def get_rating_count(self):
        """평점 개수"""
        return self.reviews.count()
    
    def get_rating_distribution(self):
        """평점 분포 반환"""
        reviews = self.reviews.all()
        if not reviews.exists():
            return {i: 0 for i in range(1, 6)}
        
        distribution = {i: 0 for i in range(1, 6)}
        for review in reviews:
            distribution[review.rating] += 1
        
        # 퍼센트로 변환
        total = reviews.count()
        return {i: round((count / total) * 100, 1) for i, count in distribution.items()}
    
    def get_recent_reviews(self, limit=5):
        """최근 리뷰 조회"""
        return self.reviews.all()[:limit]
    
    def has_user_reviewed(self, user):
        """사용자가 리뷰를 작성했는지 확인"""
        if not user.is_authenticated:
            return False
        return self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """사용자의 리뷰 조회"""
        if not user.is_authenticated:
            return None
        try:
            return self.reviews.get(user=user)
        except Review.DoesNotExist:
            return None
    
    def get_recent_comments(self, limit=10):
        """최근 댓글 조회"""
        return self.comments.all()[:limit]
    
    def get_comment_count(self):
        """댓글 개수"""
        return self.comments.count()
    
    def get_recent_inquiries(self, limit=5):
        """최근 문의 조회"""
        return self.inquiries.all()[:limit]
    
    def get_inquiry_count(self):
        """문의 개수"""
        return self.inquiries.count()


class Review(models.Model):
    """상품 리뷰 모델"""
    
    # 기본 정보
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="상품")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="작성자")
    
    # 평점 및 리뷰 내용
    rating = models.PositiveIntegerField(
        choices=[(i, f'{i}점') for i in range(1, 6)],
        verbose_name="평점"
    )
    title = models.CharField(max_length=200, verbose_name="리뷰 제목")
    content = models.TextField(verbose_name="리뷰 내용")
    
    # 상태 관리
    is_verified_purchase = models.BooleanField(default=False, verbose_name="구매 인증")
    is_helpful = models.PositiveIntegerField(default=0, verbose_name="도움됨")
    is_reported = models.BooleanField(default=False, verbose_name="신고됨")
    
    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = "리뷰들"
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # 상품당 사용자당 하나의 리뷰만
    
    def __str__(self):
        return f"{self.user.username}의 {self.product.name} 리뷰 ({self.rating}점)"
    
    def get_rating_stars(self):
        """평점을 별로 표시"""
        return '★' * self.rating + '☆' * (5 - self.rating)
    
    def get_helpful_percentage(self):
        """도움됨 비율 계산"""
        if self.is_helpful == 0:
            return 0
        # 실제 구현 시 도움됨/도움안됨 비율 계산
        return 85  # 임시값


class Comment(models.Model):
    """상품 댓글 모델"""
    
    # 기본 정보
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="상품")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="작성자")
    
    # 댓글 내용
    content = models.TextField(verbose_name="댓글 내용")
    
    # 상태 관리
    is_reported = models.BooleanField(default=False, verbose_name="신고됨")
    
    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}의 {self.product.name} 댓글"


class Inquiry(models.Model):
    """상품 문의 모델"""
    
    INQUIRY_TYPES = [
        ('product', '상품 문의'),
        ('shipping', '배송 문의'),
        ('exchange', '교환/반품'),
        ('other', '기타'),
    ]
    
    # 기본 정보
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries', verbose_name="상품")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries', verbose_name="작성자")
    
    # 문의 내용
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, verbose_name="문의 유형")
    title = models.CharField(max_length=200, verbose_name="문의 제목")
    content = models.TextField(verbose_name="문의 내용")
    email = models.EmailField(verbose_name="답변 받을 이메일")
    
    # 답변 관리
    answer = models.TextField(blank=True, verbose_name="답변 내용")
    answered_at = models.DateTimeField(null=True, blank=True, verbose_name="답변일")
    is_answered = models.BooleanField(default=False, verbose_name="답변완료")
    
    # 상태 관리
    is_reported = models.BooleanField(default=False, verbose_name="신고됨")
    
    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "문의"
        verbose_name_plural = "문의들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}의 {self.product.name} 문의: {self.title}"
