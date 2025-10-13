from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from orders.models import Order


class SignUpView(CreateView):
    """회원가입 뷰"""
    form_class = UserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """폼이 유효할 때 사용자 생성 및 로그인"""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '회원가입이 완료되었습니다!')
        return response


@login_required
def profile_view(request):
    """사용자 프로필 페이지"""
    # 사용자의 주문 정보 가져오기
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]  # 최근 5개 주문만
    total_orders = Order.objects.filter(user=request.user).count()
    
    # 총 주문 금액 계산
    total_spent = 0
    for order in Order.objects.filter(user=request.user, status__in=['paid', 'shipped', 'delivered']):
        total_spent += float(order.total)
    
    context = {
        'user': request.user,
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'users/profile.html', context)