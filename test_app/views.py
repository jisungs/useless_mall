from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <html>
    <head>
        <title>쓰잘데기 - 테스트 배포 성공!</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success { color: #28a745; font-size: 24px; }
            .info { color: #6c757d; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1 class="success">🎉 쓰잘데기 테스트 배포 성공!</h1>
        <p class="info">Railway 배포가 정상적으로 작동하고 있습니다.</p>
        <p class="info">이제 실제 쇼핑몰 개발을 시작할 수 있습니다!</p>
    </body>
    </html>
    """)