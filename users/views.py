from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView


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


def profile_view(request):
    """사용자 프로필 페이지"""
    return render(request, 'users/profile.html', {
        'user': request.user
    })