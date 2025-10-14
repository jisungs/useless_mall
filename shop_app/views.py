from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Review, Comment, Inquiry
from .forms import ReviewForm, CommentForm, InquiryForm

def home(request):
    """홈페이지 - 모든 활성 상품 표시"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'home.html', context)

def product_list(request):
    """상품 목록 페이지"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'product_list.html', context)

def product_detail(request, product_id):
    """상품 상세 페이지"""
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

def product_search(request):
    """상품 검색 페이지"""
    query = escape(request.GET.get('q', '').strip())
    products = Product.objects.filter(is_active=True)
    
    # 검색어 길이 제한
    if len(query) > 100:
        query = query[:100]
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    context = {
        'products': products,
        'query': query,
        'results_count': products.count()
    }
    return render(request, 'product_search.html', context)


# 리뷰 관련 뷰들
@login_required
def submit_review(request, product_id):
    """리뷰 제출"""
    product = get_object_or_404(Product, id=product_id)
    
    # 이미 리뷰를 작성했는지 확인
    if product.has_user_reviewed(request.user):
        messages.warning(request, '이미 이 상품에 대한 리뷰를 작성하셨습니다.')
        return redirect('product_detail', product_id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            messages.success(request, '리뷰가 성공적으로 등록되었습니다!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'shop_app/review_form.html', context)


@login_required
def edit_review(request, product_id):
    """리뷰 수정"""
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(Review, product=product, user=request.user)
    
    # 관리자가 아닌 경우 본인 리뷰만 수정 가능
    if not request.user.is_staff and review.user != request.user:
        messages.error(request, '본인의 리뷰만 수정할 수 있습니다.')
        return redirect('product_detail', product_id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, '리뷰가 성공적으로 수정되었습니다!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'product': product,
        'form': form,
        'review': review
    }
    return render(request, 'shop_app/review_form.html', context)


@login_required
@require_POST
def delete_review(request, product_id):
    """리뷰 삭제"""
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(Review, product=product, user=request.user)
    
    # 관리자가 아닌 경우 본인 리뷰만 삭제 가능
    if not request.user.is_staff and review.user != request.user:
        messages.error(request, '본인의 리뷰만 삭제할 수 있습니다.')
        return redirect('product_detail', product_id=product_id)
    
    review.delete()
    messages.success(request, '리뷰가 삭제되었습니다.')
    return redirect('product_detail', product_id=product_id)


# 관리자용 리뷰 관리 뷰들
@login_required
def admin_edit_review(request, product_id, review_id):
    """관리자 리뷰 수정"""
    if not request.user.is_staff:
        messages.error(request, '관리자만 접근할 수 있습니다.')
        return redirect('product_detail', product_id=product_id)
    
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(Review, id=review_id, product=product)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, '리뷰가 성공적으로 수정되었습니다!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'product': product,
        'form': form,
        'review': review,
        'is_admin': True
    }
    return render(request, 'shop_app/review_form.html', context)


@login_required
@require_POST
def admin_delete_review(request, product_id, review_id):
    """관리자 리뷰 삭제"""
    if not request.user.is_staff:
        messages.error(request, '관리자만 접근할 수 있습니다.')
        return redirect('product_detail', product_id=product_id)
    
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(Review, id=review_id, product=product)
    
    review.delete()
    messages.success(request, '리뷰가 삭제되었습니다.')
    return redirect('product_detail', product_id=product_id)


@csrf_exempt
def get_product_rating_data(request, product_id):
    """상품 평점 데이터 AJAX 조회"""
    product = get_object_or_404(Product, id=product_id)
    
    data = {
        'average_rating': product.get_average_rating(),
        'rating_count': product.get_rating_count(),
        'rating_distribution': product.get_rating_distribution(),
        'has_user_reviewed': product.has_user_reviewed(request.user) if request.user.is_authenticated else False,
        'user_review': None
    }
    
    if request.user.is_authenticated:
        user_review = product.get_user_review(request.user)
        if user_review:
            data['user_review'] = {
                'rating': user_review.rating,
                'title': user_review.title,
                'content': user_review.content,
                'created_at': user_review.created_at.strftime('%Y.%m.%d')
            }
    
    return JsonResponse(data)


# 댓글 관련 뷰들
@login_required
@require_POST
def submit_comment(request, product_id):
    """댓글 제출"""
    product = get_object_or_404(Product, id=product_id)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        
        messages.success(request, '댓글이 성공적으로 등록되었습니다!')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
    
    return redirect('product_detail', product_id=product_id)


@login_required
@require_POST
def delete_comment(request, product_id, comment_id):
    """댓글 삭제"""
    product = get_object_or_404(Product, id=product_id)
    comment = get_object_or_404(Comment, id=comment_id, product=product, user=request.user)
    
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('product_detail', product_id=product_id)


# 문의 관련 뷰들
@login_required
def submit_inquiry(request, product_id):
    """문의 제출"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.user = request.user
            inquiry.save()
            
            messages.success(request, '문의가 성공적으로 등록되었습니다! 빠른 시일 내에 답변드리겠습니다.')
            return redirect('product_detail', product_id=product_id)
    else:
        form = InquiryForm()
    
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'shop_app/inquiry_form.html', context)


@login_required
def edit_inquiry(request, product_id, inquiry_id):
    """문의 수정"""
    product = get_object_or_404(Product, id=product_id)
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, product=product, user=request.user)
    
    if inquiry.is_answered:
        messages.warning(request, '이미 답변된 문의는 수정할 수 없습니다.')
        return redirect('product_detail', product_id=product_id)
    
    if request.method == 'POST':
        form = InquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, '문의가 성공적으로 수정되었습니다!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = InquiryForm(instance=inquiry)
    
    context = {
        'product': product,
        'form': form,
        'inquiry': inquiry
    }
    return render(request, 'shop_app/inquiry_form.html', context)


@login_required
@require_POST
def delete_inquiry(request, product_id, inquiry_id):
    """문의 삭제"""
    product = get_object_or_404(Product, id=product_id)
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, product=product, user=request.user)
    
    inquiry.delete()
    messages.success(request, '문의가 삭제되었습니다.')
    return redirect('product_detail', product_id=product_id)