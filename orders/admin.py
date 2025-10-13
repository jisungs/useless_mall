from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """주문 상품 인라인"""
    model = OrderItem
    extra = 0
    readonly_fields = ['get_formatted_price', 'get_formatted_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """주문 관리"""
    list_display = ['id', 'user', 'get_formatted_total', 'status', 'shipping_name', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_name', 'shipping_address']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('주문 정보', {
            'fields': ('user', 'total', 'status', 'created_at', 'updated_at')
        }),
        ('배송 정보', {
            'fields': ('shipping_name', 'shipping_address', 'shipping_phone')
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        """결제 완료로 변경"""
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated}개의 주문이 결제 완료로 변경되었습니다.')
    mark_as_paid.short_description = "선택된 주문을 결제 완료로 변경"
    
    def mark_as_shipped(self, request, queryset):
        """배송 중으로 변경"""
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated}개의 주문이 배송 중으로 변경되었습니다.')
    mark_as_shipped.short_description = "선택된 주문을 배송 중으로 변경"
    
    def mark_as_delivered(self, request, queryset):
        """배송 완료로 변경"""
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated}개의 주문이 배송 완료로 변경되었습니다.')
    mark_as_delivered.short_description = "선택된 주문을 배송 완료로 변경"
    
    def mark_as_cancelled(self, request, queryset):
        """주문 취소로 변경"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated}개의 주문이 취소로 변경되었습니다.')
    mark_as_cancelled.short_description = "선택된 주문을 취소로 변경"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """주문 상품 관리"""
    list_display = ['order', 'product', 'quantity', 'get_formatted_price', 'get_formatted_total']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__user__username', 'product__name']