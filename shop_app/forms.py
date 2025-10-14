from django import forms
from .models import Review, Comment, Inquiry

class ReviewForm(forms.ModelForm):
    """리뷰 작성 폼"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i}점') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '리뷰 제목을 입력해주세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '상품에 대한 솔직한 리뷰를 작성해주세요'
            })
        }
    
    def clean_rating(self):
        """평점 검증"""
        rating = self.cleaned_data.get('rating')
        if rating not in range(1, 6):
            raise forms.ValidationError("평점은 1점부터 5점까지 선택할 수 있습니다.")
        return rating
    
    def clean_title(self):
        """제목 검증"""
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError("제목은 5자 이상 입력해주세요.")
        return title
    
    def clean_content(self):
        """내용 검증"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 10:
            raise forms.ValidationError("리뷰 내용은 10자 이상 입력해주세요.")
        return content


class CommentForm(forms.ModelForm):
    """댓글 작성 폼"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '댓글을 작성해주세요...'
            })
        }
    
    def clean_content(self):
        """내용 검증"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 5:
            raise forms.ValidationError("댓글은 5자 이상 입력해주세요.")
        return content


class InquiryForm(forms.ModelForm):
    """문의 작성 폼"""
    
    class Meta:
        model = Inquiry
        fields = ['inquiry_type', 'title', 'content', 'email']
        widgets = {
            'inquiry_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '문의 제목을 입력해주세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '문의 내용을 입력해주세요'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '답변 받을 이메일을 입력해주세요'
            })
        }
    
    def clean_title(self):
        """제목 검증"""
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError("제목은 5자 이상 입력해주세요.")
        return title
    
    def clean_content(self):
        """내용 검증"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 10:
            raise forms.ValidationError("문의 내용은 10자 이상 입력해주세요.")
        return content
