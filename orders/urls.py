from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.order_create, name='order_create'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('direct-purchase/<int:product_id>/', views.direct_purchase_create, name='direct_purchase_create'),
]
