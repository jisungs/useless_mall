from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='product_search'),
    
    # 리뷰 관련 URL
    path('products/<int:product_id>/review/', views.submit_review, name='submit_review'),
    path('products/<int:product_id>/review/edit/', views.edit_review, name='edit_review'),
    path('products/<int:product_id>/review/delete/', views.delete_review, name='delete_review'),
    path('products/<int:product_id>/rating-data/', views.get_product_rating_data, name='get_product_rating_data'),
    
    # 관리자용 리뷰 관리 URL
    path('products/<int:product_id>/review/<int:review_id>/admin-edit/', views.admin_edit_review, name='admin_edit_review'),
    path('products/<int:product_id>/review/<int:review_id>/admin-delete/', views.admin_delete_review, name='admin_delete_review'),
    
    # 댓글 관련 URL
    path('products/<int:product_id>/comment/', views.submit_comment, name='submit_comment'),
    path('products/<int:product_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # 문의 관련 URL
    path('products/<int:product_id>/inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('products/<int:product_id>/inquiry/<int:inquiry_id>/edit/', views.edit_inquiry, name='edit_inquiry'),
    path('products/<int:product_id>/inquiry/<int:inquiry_id>/delete/', views.delete_inquiry, name='delete_inquiry'),
]
