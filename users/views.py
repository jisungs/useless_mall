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
        try:
            response = super().form_valid(form)
            login(self.request, self.object)
            messages.success(self.request, '회원가입이 완료되었습니다!')
            
            # next 파라미터가 있으면 해당 페이지로 리다이렉트 (안전한 방식)
            next_url = self.request.GET.get('next')
            if next_url:
                # URL 검증 (보안)
                if next_url.startswith('/orders/direct-purchase/'):
                    return redirect(next_url)
                else:
                    messages.warning(self.request, '잘못된 리다이렉트 URL입니다.')
            
            return response
        except Exception as e:
            messages.error(self.request, f'회원가입 중 오류가 발생했습니다: {str(e)}')
            return redirect('signup')


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