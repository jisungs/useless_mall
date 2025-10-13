from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

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
