# 🐍 PythonAnywhere 배포 가이드

## 📋 개요
Python 전용 플랫폼인 PythonAnywhere를 사용한 Django 프로젝트 배포 가이드입니다.

## 🎯 PythonAnywhere 선택 이유
- ✅ **Python 전용 플랫폼** (Django 최적화)
- ✅ **무료 플랜 제공** (월 100초 CPU)
- ✅ **간단한 설정** (GUI 기반)
- ✅ **안정적인 성능**
- ✅ **풍부한 Python 생태계**

## 📝 사전 준비사항
- [x] GitHub 레포지토리 준비 완료
- [x] Django 프로젝트 완성
- [x] requirements.txt 준비 완료
- [x] 정적 파일 설정 완료

## 🔧 1단계: 프로젝트 설정 수정

### 1.1 데이터베이스 설정 (SQLite 사용)
```python
# config/settings.py - SQLite 사용 (PythonAnywhere 무료 플랜)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 1.2 정적 파일 설정
```python
# config/settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# PythonAnywhere용 설정
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

### 1.3 ALLOWED_HOSTS 설정
```python
# config/settings.py
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,*.pythonanywhere.com', cast=lambda v: [s.strip() for s in v.split(',')])
```

### 1.4 CSRF 설정
```python
# config/settings.py
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='https://*.pythonanywhere.com', cast=lambda v: [s.strip() for s in v.split(',')])
```

## 🌐 2단계: PythonAnywhere 계정 설정

### 2.1 회원가입
1. **https://www.pythonanywhere.com** 접속
2. **"Sign up for a free account"** 클릭
3. **사용자명 입력** (예: `uselessmall`)
4. **이메일 주소 입력**
5. **비밀번호 설정**
6. **이메일 인증 완료**

### 2.2 계정 확인
- **사용자명**: `uselessmall`
- **도메인**: `uselessmall.pythonanywhere.com`
- **무료 플랜**: 월 100초 CPU 시간

## 📁 3단계: 프로젝트 업로드

### 3.1 GitHub에서 클론
1. **Consoles** 탭 클릭
2. **Bash** 콘솔 열기
3. **프로젝트 클론**:
   ```bash
   cd ~
   git clone https://github.com/[사용자명]/useless_mall.git
   cd useless_mall
   ```

### 3.2 가상환경 설정
```bash
# 가상환경 생성
python3.10 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3.3 데이터베이스 설정
```bash
# 마이그레이션 실행
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic --noinput

# 슈퍼유저 생성
python manage.py createsuperuser
```

## 🌐 4단계: 웹 앱 설정

### 4.1 웹 앱 생성
1. **Web** 탭 클릭
2. **"Add a new web app"** 클릭
3. **"Manual configuration"** 선택
4. **Python 버전 선택**: `Python 3.10`
5. **"Next"** 클릭

### 4.2 WSGI 파일 설정
1. **WSGI configuration file** 클릭
2. **기존 내용 삭제 후 다음 코드 입력**:
```python
import os
import sys

# 프로젝트 경로 추가
path = '/home/uselessmall/useless_mall'
if path not in sys.path:
    sys.path.append(path)

# Django 설정
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Django 애플리케이션 로드
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 4.3 환경변수 설정
1. **Web** 탭에서 **"Environment variables"** 클릭
2. **다음 변수들 추가**:
```
SECRET_KEY=-0&au293s!x68rs!marf^h-*yn#-y=+uui*umdh#mntk%2c9dj
DEBUG=False
ALLOWED_HOSTS=uselessmall.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://uselessmall.pythonanywhere.com
```

## 🔄 5단계: 배포 및 테스트

### 5.1 웹 앱 재시작
1. **Web** 탭에서 **"Reload"** 버튼 클릭
2. **배포 완료 확인**

### 5.2 도메인 확인
- **URL**: `https://uselessmall.pythonanywhere.com`
- **접속 테스트** 진행

### 5.3 기능 테스트
- [ ] 홈페이지 접속
- [ ] 상품 목록 확인
- [ ] 상품 상세 페이지
- [ ] 회원가입/로그인
- [ ] 장바구니 기능
- [ ] 주문 기능
- [ ] 리뷰/댓글 기능
- [ ] 관리자 페이지

## 🛠️ 6단계: 문제 해결

### 6.1 일반적인 문제들

#### 웹 앱 로딩 실패
```bash
# 로그 확인
tail -f /var/log/uselessmall.pythonanywhere.com.error.log

# 해결 방법
- WSGI 파일 문법 확인
- 환경변수 설정 확인
- 패키지 설치 확인
```

#### 정적 파일 로딩 실패
```bash
# 정적 파일 수집 재실행
python manage.py collectstatic --noinput

# 해결 방법
- STATIC_ROOT 설정 확인
- 파일 권한 확인
```

#### 데이터베이스 오류
```bash
# 마이그레이션 재실행
python manage.py migrate

# 해결 방법
- 데이터베이스 파일 권한 확인
- 마이그레이션 상태 확인
```

### 6.2 로그 모니터링
1. **Web** 탭 → **"Error log"** 클릭
2. **실시간 에러 로그 확인**
3. **문제 분석 및 해결**

## 📊 7단계: 성능 최적화

### 7.1 데이터베이스 최적화
```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}
```

### 7.2 캐싱 설정
```python
# config/settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### 7.3 정적 파일 최적화
```python
# config/settings.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## 🔒 8단계: 보안 설정

### 8.1 환경변수 보안
- **SECRET_KEY**: 강력한 랜덤 키 사용
- **DEBUG**: 프로덕션에서는 False
- **ALLOWED_HOSTS**: 정확한 도메인 설정

### 8.2 HTTPS 설정
```python
# config/settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📈 9단계: 모니터링 및 유지보수

### 9.1 성능 모니터링
- **PythonAnywhere 대시보드** 메트릭 확인
- **CPU 사용량** 모니터링
- **에러율** 추적

### 9.2 정기 점검
- **주간**: 로그 확인, 성능 체크
- **월간**: 보안 업데이트, 의존성 업데이트
- **분기**: 데이터베이스 최적화

## 🎯 예상 결과

### 성공 지표
- ✅ **배포 성공률**: 95%
- ✅ **응답 시간**: < 3초
- ✅ **가동률**: 99%
- ✅ **데이터베이스 안정성**: 95%

### 비용
- **무료 플랜**: 월 100초 CPU
- **도메인**: 무료
- **총 비용**: $0/월

## 🚨 주의사항

### 무료 플랜 제한
- **월 100초 CPU 시간** (제한적)
- **1개 웹 앱**
- **제한된 도메인**

### 업그레이드 고려사항
- **CPU 시간 부족 시**: 유료 플랜 고려
- **성능 향상 필요 시**: 더 높은 사양 플랜
- **백업 필요 시**: 자동 백업 플랜

## 📞 지원 및 도움

### PythonAnywhere 지원
- **문서**: https://help.pythonanywhere.com
- **커뮤니티**: https://www.pythonanywhere.com/forums
- **이메일**: support@pythonanywhere.com

### 문제 해결 체크리스트
- [ ] 계정 생성 확인
- [ ] 프로젝트 업로드 확인
- [ ] 가상환경 설정 확인
- [ ] 웹 앱 설정 확인
- [ ] 환경변수 설정 확인
- [ ] WSGI 파일 설정 확인

---

## 🎉 배포 완료 체크리스트

- [ ] PythonAnywhere 계정 생성
- [ ] 프로젝트 업로드
- [ ] 가상환경 설정
- [ ] 데이터베이스 설정
- [ ] 웹 앱 생성
- [ ] WSGI 파일 설정
- [ ] 환경변수 설정
- [ ] 배포 실행
- [ ] 슈퍼유저 생성
- [ ] 기능 테스트
- [ ] 성능 최적화
- [ ] 보안 설정
- [ ] 모니터링 설정

**예상 소요 시간: 45-60분**
**성공률: 90%+**

## 🔄 업데이트 방법

### 코드 업데이트
```bash
# 콘솔에서 실행
cd ~/useless_mall
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### 웹 앱 재시작
1. **Web** 탭에서 **"Reload"** 버튼 클릭
2. **업데이트 완료 확인**

## 📊 Render.com vs PythonAnywhere 비교

| 항목 | Render.com | PythonAnywhere |
|------|------------|----------------|
| **데이터베이스** | PostgreSQL 무료 | SQLite만 무료 |
| **CPU 시간** | 750시간/월 | 100초/월 |
| **설정 난이도** | 중간 | 쉬움 |
| **성능** | 높음 | 중간 |
| **안정성** | 높음 | 높음 |
| **비용** | 무료 | 무료 |

**추천**: Render.com (더 많은 리소스와 PostgreSQL 지원)
