from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review, Comment, Inquiry

# Register your models here.

# Register your models here.

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'shipping_fee', 'stock_status_display', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'shipping_fee', 'stock_quantity', 'is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'category', 'price', 'shipping_fee', 'description')
        }),
        ('이미지', {
            'fields': ('image_path',)
        }),
        ('재고 관리', {
            'fields': ('stock_quantity', 'is_active'),
            'description': '재고 상태: 품절(0), 재고부족(1-10), 재고적음(11-50), 충분(51+)'
        }),
    )
    
    def stock_status_display(self, obj):
        """재고 상태를 색상과 함께 표시"""
        status = obj.get_stock_status()
        css_class = obj.get_stock_status_class()
        return format_html(
            '<span class="badge {}">{} ({}개)</span>',
            css_class,
            status,
            obj.stock_quantity
        )
    stock_status_display.short_description = '재고 상태'
    
    def stock_status_filter(self, obj):
        """재고 상태별 필터링을 위한 메서드"""
        return obj.get_stock_status()
    stock_status_filter.short_description = '재고 상태'
    
    def get_queryset(self, request):
        """관리자 페이지에서 사용할 쿼리셋"""
        return super().get_queryset(request)
    
    actions = ['add_stock_action', 'mark_out_of_stock']
    
    def add_stock_action(self, request, queryset):
        """선택된 상품들의 재고를 일괄 추가"""
        for product in queryset:
            product.add_stock(50)  # 50개씩 추가
        self.message_user(request, f"{queryset.count()}개 상품의 재고를 50개씩 추가했습니다.")
    add_stock_action.short_description = "선택된 상품 재고 50개 추가"
    
    def mark_out_of_stock(self, request, queryset):
        """선택된 상품들을 품절 처리"""
        updated = queryset.update(stock_quantity=0)
        self.message_user(request, f"{updated}개 상품을 품절 처리했습니다.")
    mark_out_of_stock.short_description = "선택된 상품 품절 처리"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'title', 'is_verified_purchase', 'is_reported', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'is_reported', 'created_at']
    search_fields = ['user__username', 'product__name', 'title', 'content']
    list_editable = ['is_verified_purchase', 'is_reported']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'product', 'rating', 'title', 'content')
        }),
        ('상태 관리', {
            'fields': ('is_verified_purchase', 'is_helpful', 'is_reported'),
            'description': '리뷰 상태 관리'
        }),
    )
    
    def rating_display(self, obj):
        """평점을 별로 표시"""
        return format_html(
            '<span style="color: #ffc107;">{}</span>',
            obj.get_rating_stars()
        )
    rating_display.short_description = '평점'
    
    actions = ['mark_verified', 'mark_reported', 'delete_reported']
    
    def mark_verified(self, request, queryset):
        """선택된 리뷰들을 구매 인증 처리"""
        updated = queryset.update(is_verified_purchase=True)
        self.message_user(request, f"{updated}개 리뷰를 구매 인증 처리했습니다.")
    mark_verified.short_description = "선택된 리뷰 구매 인증 처리"
    
    def mark_reported(self, request, queryset):
        """선택된 리뷰들을 신고 처리"""
        updated = queryset.update(is_reported=True)
        self.message_user(request, f"{updated}개 리뷰를 신고 처리했습니다.")
    mark_reported.short_description = "선택된 리뷰 신고 처리"
    
    def delete_reported(self, request, queryset):
        """신고된 리뷰들을 삭제"""
        reported_reviews = queryset.filter(is_reported=True)
        count = reported_reviews.count()
        reported_reviews.delete()
        self.message_user(request, f"{count}개의 신고된 리뷰를 삭제했습니다.")
    delete_reported.short_description = "신고된 리뷰 삭제"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'content_preview', 'is_reported', 'created_at']
    list_filter = ['is_reported', 'created_at']
    search_fields = ['user__username', 'product__name', 'content']
    list_editable = ['is_reported']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'product', 'content')
        }),
        ('상태 관리', {
            'fields': ('is_reported',),
            'description': '댓글 상태 관리'
        }),
    )
    
    def content_preview(self, obj):
        """댓글 내용 미리보기"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '댓글 내용'
    
    actions = ['mark_reported', 'delete_reported']
    
    def mark_reported(self, request, queryset):
        """선택된 댓글들을 신고 처리"""
        updated = queryset.update(is_reported=True)
        self.message_user(request, f"{updated}개 댓글을 신고 처리했습니다.")
    mark_reported.short_description = "선택된 댓글 신고 처리"
    
    def delete_reported(self, request, queryset):
        """신고된 댓글들을 삭제"""
        reported_comments = queryset.filter(is_reported=True)
        count = reported_comments.count()
        reported_comments.delete()
        self.message_user(request, f"{count}개의 신고된 댓글을 삭제했습니다.")
    delete_reported.short_description = "신고된 댓글 삭제"


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'title', 'inquiry_type', 'is_answered', 'created_at']
    list_filter = ['inquiry_type', 'is_answered', 'created_at']
    search_fields = ['user__username', 'product__name', 'title', 'content']
    list_editable = ['is_answered']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'product', 'inquiry_type', 'title', 'content', 'email')
        }),
        ('답변 관리', {
            'fields': ('answer', 'is_answered', 'answered_at'),
            'description': '문의 답변 관리'
        }),
        ('상태 관리', {
            'fields': ('is_reported',),
            'description': '문의 상태 관리'
        }),
    )
    
    actions = ['mark_answered', 'mark_reported', 'delete_reported']
    
    def mark_answered(self, request, queryset):
        """선택된 문의들을 답변완료 처리"""
        from django.utils import timezone
        updated = queryset.update(is_answered=True, answered_at=timezone.now())
        self.message_user(request, f"{updated}개 문의를 답변완료 처리했습니다.")
    mark_answered.short_description = "선택된 문의 답변완료 처리"
    
    def mark_reported(self, request, queryset):
        """선택된 문의들을 신고 처리"""
        updated = queryset.update(is_reported=True)
        self.message_user(request, f"{updated}개 문의를 신고 처리했습니다.")
    mark_reported.short_description = "선택된 문의 신고 처리"
    
    def delete_reported(self, request, queryset):
        """신고된 문의들을 삭제"""
        reported_inquiries = queryset.filter(is_reported=True)
        count = reported_inquiries.count()
        reported_inquiries.delete()
        self.message_user(request, f"{count}개의 신고된 문의를 삭제했습니다.")
    delete_reported.short_description = "신고된 문의 삭제"
