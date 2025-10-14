# 🚀 Render.com 배포 가이드

## 📋 개요
Railway에서 발생한 데이터베이스 문제를 해결하기 위해 Render.com으로 배포하는 단계별 가이드입니다.

## 🎯 Render.com 선택 이유
- ✅ **무료 PostgreSQL 포함** (데이터베이스 문제 완전 해결)
- ✅ **월 750시간 무료** (24시간/일 사용 가능)
- ✅ **안정적인 성능** (512MB RAM)
- ✅ **자동 배포** (GitHub 연동)
- ✅ **Django 최적화**

## 📝 사전 준비사항
- [x] GitHub 레포지토리 준비 완료
- [x] Django 프로젝트 완성
- [x] requirements.txt 준비 완료
- [x] Procfile 준비 완료
- [x] 환경변수 설정 완료

## 🔧 1단계: 프로젝트 설정 수정

### 1.1 데이터베이스 설정 활성화
```python
# config/settings.py에서 주석 해제
# Railway PostgreSQL 사용 (환경변수가 있으면 PostgreSQL, 없으면 SQLite)
if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(config('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 1.2 정적 파일 설정 확인
```python
# config/settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 1.3 Procfile 확인
```
release: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput
web: gunicorn config.wsgi:application --log-file -
```

## 🌐 2단계: Render.com 계정 설정

### 2.1 회원가입
1. **https://render.com** 접속
2. **"Get Started for Free"** 클릭
3. **GitHub 계정으로 로그인**
4. **이메일 인증 완료**

### 2.2 GitHub 레포지토리 연결
1. **Render 대시보드** 접속
2. **"New +"** 버튼 클릭
3. **"Web Service"** 선택
4. **GitHub 레포지토리 선택**: `useless_mall`

## 🗄️ 3단계: PostgreSQL 데이터베이스 생성

### 3.1 데이터베이스 생성
1. **Render 대시보드**에서 **"New +"** 클릭
2. **"PostgreSQL"** 선택
3. **설정 입력**:
   - **Name**: `uselessmall-db`
   - **Database**: `uselessmall`
   - **User**: `uselessmall_user`
   - **Region**: `Oregon (US West)`
4. **"Create Database"** 클릭

### 3.2 데이터베이스 정보 확인
- **Internal Database URL** 복사 (나중에 사용)
- **External Database URL** 복사 (로컬 테스트용)

## 🚀 4단계: 웹 서비스 생성

### 4.1 웹 서비스 설정
1. **"New +"** → **"Web Service"** 선택
2. **GitHub 레포지토리 연결**: `useless_mall`
3. **설정 입력**:
   - **Name**: `uselessmall-web`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn config.wsgi:application --log-file -`

### 4.2 환경변수 설정
```
SECRET_KEY=-0&au293s!x68rs!marf^h-*yn#-y=+uui*umdh#mntk%2c9dj
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
CSRF_TRUSTED_ORIGINS=https://uselessmall-web.onrender.com
DATABASE_URL=[PostgreSQL Internal Database URL]
```

### 4.3 고급 설정
- **Auto-Deploy**: `Yes` (GitHub 푸시 시 자동 배포)
- **Branch**: `main`
- **Root Directory**: `/` (기본값)

## 🔄 5단계: 배포 및 테스트

### 5.1 배포 실행
1. **"Create Web Service"** 클릭
2. **빌드 로그 확인** (5-10분 소요)
3. **배포 완료 확인**

### 5.2 슈퍼유저 생성
1. **Render Shell** 접속:
   ```bash
   render shell uselessmall-web
   ```
2. **슈퍼유저 생성**:
   ```bash
   python manage.py createsuperuser
   ```

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

#### 빌드 실패
```bash
# 로그 확인
render logs uselessmall-web

# 해결 방법
- requirements.txt 패키지 확인
- Python 버전 호환성 확인
- 의존성 충돌 해결
```

#### 데이터베이스 연결 실패
```bash
# 환경변수 확인
echo $DATABASE_URL

# 해결 방법
- DATABASE_URL 정확성 확인
- PostgreSQL 서비스 상태 확인
```

#### 정적 파일 로딩 실패
```bash
# collectstatic 실행
python manage.py collectstatic --noinput

# 해결 방법
- STATIC_ROOT 설정 확인
- whitenoise 설정 확인
```

### 6.2 로그 모니터링
1. **Render 대시보드** → **"Logs"** 탭
2. **실시간 로그 확인**
3. **에러 메시지 분석**

## 📊 7단계: 성능 최적화

### 7.1 데이터베이스 최적화
```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'CONN_MAX_AGE': 600,
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
- **Render 대시보드** 메트릭 확인
- **응답 시간** 모니터링
- **에러율** 추적

### 9.2 정기 점검
- **주간**: 로그 확인, 성능 체크
- **월간**: 보안 업데이트, 의존성 업데이트
- **분기**: 데이터베이스 최적화

## 🎯 예상 결과

### 성공 지표
- ✅ **배포 성공률**: 100%
- ✅ **응답 시간**: < 2초
- ✅ **가동률**: 99.9%
- ✅ **데이터베이스 안정성**: 100%

### 비용
- **무료 플랜**: 월 750시간
- **PostgreSQL**: 무료 (1GB)
- **총 비용**: $0/월

## 🚨 주의사항

### 무료 플랜 제한
- **월 750시간** (약 24시간/일)
- **512MB RAM**
- **PostgreSQL 1GB**

### 업그레이드 고려사항
- **사용량 증가 시**: 유료 플랜 고려
- **성능 향상 필요 시**: 더 높은 사양 플랜
- **백업 필요 시**: 자동 백업 플랜

## 📞 지원 및 도움

### Render.com 지원
- **문서**: https://render.com/docs
- **커뮤니티**: https://community.render.com
- **이메일**: support@render.com

### 문제 해결 체크리스트
- [ ] GitHub 레포지토리 연결 확인
- [ ] 환경변수 설정 확인
- [ ] PostgreSQL 연결 확인
- [ ] 빌드 로그 확인
- [ ] 배포 로그 확인

---

## 🎉 배포 완료 체크리스트

- [ ] Render.com 계정 생성
- [ ] PostgreSQL 데이터베이스 생성
- [ ] 웹 서비스 생성
- [ ] 환경변수 설정
- [ ] 배포 실행
- [ ] 슈퍼유저 생성
- [ ] 기능 테스트
- [ ] 성능 최적화
- [ ] 보안 설정
- [ ] 모니터링 설정

**예상 소요 시간: 30-45분**
**성공률: 95%+**
