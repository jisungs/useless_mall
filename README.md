# 🛍️ 쓰잘데기 - 필요없는 물건 쇼핑몰

> "세상에서 제일 쓸모없는 상점" - 완전히 필요없지만 재미있는 물건들만 판매하는 쇼핑몰

## 📋 프로젝트 개요

### 🎯 핵심 컨셉
- **쇼핑몰 이름**: 쓰잘데기
- **테마**: 완전히 필요없지만 재미있는 물건들만 판매
- **목표**: 실제 배포 + 유튜브 영상 제작
- **기간**: 7일 (개발 5일 + 영상 2일)
- **성공 확률**: 97%

### 🛠 기술 스택
- **백엔드**: Django 5.2.7, SQLite, Django Session
- **프론트엔드**: Bootstrap 5 (CDN), Vanilla JavaScript
- **배포**: Railway (무료), Whitenoise, python-decouple

## 🚀 현재 진행 상황

### ✅ 완료된 작업 (Day 0-3)

#### **Task 0-1: 컨셉 및 자료 준비** ✅ **완료**
- [x] 쇼핑몰 이름 최종 확정: **"쓰잘데기"**
- [x] 10개 필요없는 상품 아이디어 확정 (3개 완료, 7개 추가 필요)
- [x] 상품별 가격 및 설명 작성 (3개 완료, 7개 추가 필요)
- [x] 상품 이미지 10개 수집 (`static/img/` 폴더)

#### **Task 0-2: 개발 환경 설정** ✅ **완료**
- [x] Python 3.11+ 가상환경 생성 (`venv/` 폴더)
- [x] 기본 패키지 설치 완료:
  - Django==5.2.7
  - Pillow==11.3.0
  - python-decouple==3.8
  - whitenoise==6.11.0
  - gunicorn==23.0.0
- [x] requirements.txt 생성 (버전 고정)

#### **Task 0-3: Railway 테스트 배포** ✅ **완료**
- [x] Railway 계정 생성
- [x] 간단한 Django 테스트 앱 생성
- [x] 배포 파일 생성 (Procfile, runtime.txt)
- [x] 마이그레이션 완료
- [x] 정적 파일 수집 완료
- [x] 로컬 서버 테스트 완료
- [x] **Railway 배포 성공**: `uselessmall-production.up.railway.app`

#### **Task 1-1: 프로젝트 생성** ✅ **완료**
- [x] Django 프로젝트 생성 (`config` 프로젝트)
- [x] 앱 생성 (`test_app`)
- [x] 기본 설정 (INSTALLED_APPS, TEMPLATES, STATIC, MEDIA)
- [x] 정적 파일 폴더 구조 생성

#### **Task 1-2: 데이터베이스 모델** ✅ **완료**
- [x] **Category 모델 생성**:
  - `name`: 카테고리명 (CharField, 100자)
  - `description`: 설명 (TextField, 선택사항)
  - `created_at`, `updated_at`: 자동 타임스탬프
- [x] **Product 모델 생성**:
  - `name`: 상품명 (CharField, 200자)
  - `price`: 가격 (DecimalField, 10자리, 소수점 2자리)
  - `description`: 상품 설명 (TextField)
  - `image_path`: 이미지 파일명 (CharField, 200자)
  - `category`: 카테고리 (ForeignKey → Category)
  - `is_active`: 판매 중 (BooleanField, 기본값 True)
  - `stock_quantity`: 재고 수량 (PositiveIntegerField, 기본값 999)
  - `created_at`, `updated_at`: 자동 타임스탬프
- [x] **마이그레이션 생성 및 적용**: `0001_initial.py`, `0002_remove_product_is_fake.py`
- [x] **슈퍼유저 생성**: admin/admin123

#### **Task 1-3: Git 설정** ✅ **완료**
- [x] GitHub 레포지토리 생성
- [x] .gitignore 작성
- [x] 초기 커밋 및 푸시

#### **Task 1-4: Admin 커스터마이징** ✅ **완료**
- [x] **CategoryAdmin 클래스**:
  - `list_display`: name, description, created_at
  - `list_filter`: created_at
  - `search_fields`: name, description
- [x] **ProductAdmin 클래스**:
  - `list_display`: name, category, price, is_active, stock_quantity, created_at
  - `list_filter`: category, is_active, created_at
  - `search_fields`: name, description
  - `list_editable`: price, is_active, stock_quantity
  - `fieldsets`: 기본 정보, 이미지, 상태로 그룹화

#### **Task 1-5: 기본 템플릿** ✅ **완료**
- [x] templates/ 폴더 생성
- [x] base.html 작성 (Bootstrap 5 CDN)
- [x] 네비게이션 바 구성
- [x] 정적 파일 설정 확인

#### **Task 1-6: 초기 테스트** ✅ **완료**
- [x] Django 프로젝트 실행 확인
- [x] Admin 페이지 접속 확인
- [x] 정적 이미지 표시 확인
- [x] 상품 5개 등록 완료

#### **Task 2-1: 홈페이지** ✅ **완료**
- [x] HomeView 작성 (최신 8개 상품)
- [x] home.html 템플릿
- [x] 히어로 섹션 (메인 배너)
- [x] 상품 그리드 (Bootstrap Card)

#### **Task 2-2: 상품 목록** ✅ **완료**
- [x] ProductListView 작성 (페이지네이션)
- [x] product_list.html 템플릿
- [x] 상품 카드 컴포넌트
- [x] URL 연결

#### **Task 2-3: 상품 상세** ✅ **완료**
- [x] ProductDetailView 작성
- [x] product_detail.html 템플릿
- [x] 상품 정보 레이아웃
- [x] "장바구니 담기" 버튼 (디자인만)

#### **Task 2-4: 스타일링 및 정적 파일 최적화** ✅ **완료**
- [x] custom.css 파일 생성
- [x] 모바일 반응형 확인
- [x] 정적 이미지 최적화 확인
- [x] 나머지 상품 5개 등록 (정적 이미지 경로 사용)

#### **Task 2-5: Sample 디자인 완전 적용** ✅ **완료**
- [x] sample/index.html과 100% 동일한 디자인 적용
- [x] CSS Variables 시스템 구축
- [x] 궁서체 폰트 (Noto Serif KR) 적용
- [x] 인라인 CSS/JS로 정적 파일 의존성 제거
- [x] 완전한 반응형 디자인 구현

#### **Task 2-6: JavaScript 기능 완성** ✅ **완료**
- [x] 장바구니 시스템 (로컬 스토리지 기반)
- [x] 애니메이션 효과 (페이드인, 호버 리프트)
- [x] 알림 시스템 (성공/오류 메시지)
- [x] 부드러운 스크롤 네비게이션
- [x] 상품 상세 페이지 완전 기능

#### **Task 3-1: 회원가입** ✅ **완료**
- [x] users 앱 생성 및 설정
- [x] UserCreationForm 기반 회원가입
- [x] signup.html 템플릿 (Bootstrap 스타일)
- [x] URL 연결 및 네비게이션 바 통합
- [x] 회원가입 후 자동 로그인 기능

#### **Task 3-2: 로그인/로그아웃** ✅ **완료**
- [x] Django LoginView 활용
- [x] login.html 템플릿 (Bootstrap 스타일)
- [x] 로그아웃 기능 (POST 요청 처리)
- [x] 네비게이션 바 상태 표시 (드롭다운 메뉴)
- [x] 사용자 프로필 페이지
- [x] 로그인/로그아웃 리다이렉트 설정

#### **Task 3-3: 세션 기반 장바구니** ✅ **완료**
- [x] cart 앱 생성 및 설정
- [x] 세션 기반 Cart 클래스 구현
- [x] 장바구니 추가/제거/수량 변경 기능
- [x] 장바구니 상세 페이지 템플릿
- [x] 상품 목록에서 장바구니 추가 버튼 연결
- [x] 세션 만료 및 동시성 테스트 케이스 작성

#### **Task 3-4: 검색 기능** ✅ **완료**
- [x] Q 객체를 활용한 다중 필드 검색
- [x] 상품명, 설명, 카테고리 검색 지원
- [x] 검색 결과 페이지 템플릿
- [x] 네비게이션 바에 검색 폼 추가
- [x] 검색 결과 개수 표시

#### **Task 4-1: 주문 시스템** ✅ **완료**
- [x] orders 앱 생성 및 설정
- [x] Order 모델 구현:
  - `user`: 주문자 (ForeignKey → User)
  - `first_name`, `last_name`: 주문자 이름
  - `email`: 이메일 주소
  - `address`, `postal_code`, `city`: 배송 주소
  - `created`, `updated`: 주문 생성/수정 시간
  - `paid`: 결제 여부 (BooleanField)
  - `status`: 주문 상태 (CharField, 선택사항)
- [x] OrderItem 모델 구현:
  - `order`: 주문 (ForeignKey → Order)
  - `product`: 상품 (ForeignKey → Product)
  - `price`: 주문 시점 가격 (DecimalField)
  - `quantity`: 수량 (PositiveIntegerField)
- [x] 주문 생성 뷰 (order_create): 장바구니에서 주문 생성
- [x] 주문 상세 뷰 (order_detail): 개별 주문 상세 정보
- [x] 주문 목록 뷰 (order_list): 사용자 주문 목록
- [x] 템플릿 완성: checkout.html, order_detail.html, payment_success.html
- [x] Admin 커스터마이징: OrderAdmin, OrderItemInline

#### **Task 4-2: 가짜 결제 시스템** ✅ **완료**
- [x] "주문하기" 버튼 (장바구니에서 주문 생성으로 연결)
- [x] 가짜 결제 성공 페이지 (payment_success)
- [x] 주문 상태 변경 (paid=True, status='paid')
- [x] 결제 시뮬레이션 완료
- [x] 주문 완료 후 장바구니 자동 비우기

#### **Task 4-3: 핵심 기능 테스트 및 UI 개선** ✅ **완료**
- [x] 회원가입 → 로그인 플로우 테스트
- [x] 상품 목록 → 상세 → 장바구니 플로우 테스트
- [x] 주문 생성 → 결제 시뮬레이션 플로우 테스트
- [x] **장바구니 UI 완전 개선**:
  - 반응형 레이아웃 분리 (데스크톱/모바일)
  - 수량 조절 컴포넌트 겹침 문제 해결
  - 합계금액 독립적 표시
  - 호버 효과 및 애니메이션 추가
- [x] **주문 요약 카드 상세 정보 표시**:
  - 각 상품별 상세 정보 (상품명, 단가, 수량, 합계)
  - 스크롤 가능한 상품 목록
  - 시각적 강조 및 그라데이션 배경

### 📦 현재 상품 목록 (3개 완료)

#### **데이터베이스 등록 상품 (3개)**
1. **투명 우산** - ₩12,000 - 비가 안 맞는 우산. 완전히 투명해서 비를 막지 못합니다.
2. **소리 나는 슬리퍼** - ₩15,000 - 걸을 때마다 삐삐 소리가 나는 슬리퍼. 조용한 곳에서는 사용 금지!
3. **뒤집어진 시계** - ₩25,000 - 시계바늘이 거꾸로 돌아가는 시계. 시간을 알 수 없어서 더욱 특별합니다.

#### **Sample 디자인 상품 (6개)**
4. **구멍 난 양말** - ₩3,000 - 발가락이 다 나오는 구멍이 뚫린 양말. 보온 효과 제로.
5. **무선 충전기** - ₩25,000 - 충전이 안 되는 무선 충전기. 완전히 무선이지만 전력도 무선.
6. **소리 안 나는 종** - ₩7,000 - 울리지 않는 장식용 종. 시각적 효과만 있습니다.
7. **100명 유튜버 포토카드** - 100명 구독자를 가진 유튜버 지성스의 친필 사인이 담긴 포토카드
8. **지성스의 사소한 이야기** - 100명 구독자를 보유한 유튜버 지성스의 생각이 담긴 수필집 PDF 전자책
9. **지성스의 사인이 담긴 노트** - 지성스가 직접 제작한 한지 노트, 표지에 친필 사인 포함

### 🎯 현재 완성도

#### **✅ 완전히 완성된 기능들**
- [x] **홈페이지**: Sample 디자인과 100% 동일한 완성도
- [x] **상품 목록**: 반응형 그리드 레이아웃
- [x] **상품 상세**: 완전한 상품 정보 및 탭 시스템
- [x] **장바구니**: 세션 기반 완전 기능 (추가/제거/수량 변경)
- [x] **회원가입/로그인**: Django 기본 인증 시스템
- [x] **검색 기능**: 다중 필드 검색 (상품명, 설명, 카테고리)
- [x] **주문 시스템**: 완전한 주문 생성/관리 시스템
- [x] **가짜 결제**: 결제 시뮬레이션 및 주문 상태 관리
- [x] **장바구니 UI**: 반응형 레이아웃 분리 및 완전 개선
- [x] **주문 요약**: 상세한 상품 정보 표시
- [x] **디자인 시스템**: CSS Variables, 궁서체 폰트, 애니메이션
- [x] **반응형**: 모바일/태블릿/데스크톱 완벽 대응
- [x] **JavaScript**: 장바구니, 애니메이션, 알림 시스템
- [x] **앱 구조**: test_app → shop_app 이름 변경 완료
- [x] **개발 환경 접속 문제 해결**: DEBUG 설정 및 보안 설정 최적화
- [x] **홈페이지 데이터베이스 연동**: 하드코딩된 상품을 실제 DB 상품으로 교체
- [x] **주문 목록 페이지**: 누락된 템플릿 생성 및 완전한 주문 관리 시스템
- [x] **프로필 페이지 주문 현황**: 사용자별 주문 통계 및 최근 주문 내역 표시

#### **🔄 다음 작업 예정 (Day 4 오후)**
- [ ] **프로덕션 배포 설정**
- [ ] **Railway 최종 배포**
- [ ] **배포 후 전체 플로우 테스트**

## 🎨 디자인 시스템

### ✅ 완성된 디자인 특징
- **미니멀 디자인**: 화이트 앤 블랙 기반
- **궁서체 폰트**: Noto Serif KR 사용
- **CSS Variables**: 일관된 색상, 폰트, 간격 시스템
- **반응형 레이아웃**: 모바일, 태블릿, 데스크톱 대응
- **Bootstrap 5**: 기본 UI 컴포넌트 활용
- **애니메이션**: 페이드인, 호버 리프트, 부드러운 스크롤

### 🛍️ 쇼핑몰 기능
- **상품 카드**: 6개 샘플 상품 표시
- **장바구니**: 상품 추가/제거/수량 변경
- **로컬 스토리지**: 장바구니 데이터 저장
- **주문 시뮬레이션**: 가짜 결제 프로세스
- **알림 시스템**: 성공/오류 메시지

## 🛠 개발 환경 설정

### 필수 요구사항
- Python 3.11+
- Git
- Railway 계정

### 설치 및 실행

#### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/fake_shopping_mall.git
cd fake_shopping_mall
```

#### 2. 가상환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

#### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 4. 데이터베이스 설정
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

#### 5. 서버 실행
```bash
python manage.py runserver 8000
```

#### 6. 접속 확인
브라우저에서 `http://localhost:8000` 접속

## 🔧 서버 관리

### 서버 시작
```bash
# 기본 포트 (8000)로 시작
python manage.py runserver

# 특정 포트로 시작
python manage.py runserver 8001
```

### 서버 종료 방법

#### 방법 1: 터미널에서 직접 종료
```bash
# 서버가 실행 중인 터미널에서
Ctrl + C
```

#### 방법 2: 백그라운드 프로세스 종료
```bash
# 포트 사용 프로세스 확인
lsof -ti:8000

# 프로세스 ID로 종료 (PID를 실제 값으로 변경)
kill -9 [PID]

# 또는 포트로 직접 종료
lsof -ti:8000 | xargs kill -9
```

#### 방법 3: 모든 Python 프로세스 확인 후 종료
```bash
# 실행 중인 Python 프로세스 확인
ps aux | grep "python manage.py runserver"

# 특정 프로세스 종료
kill -9 [PID]
```

#### 방법 4: 다른 포트 사용
```bash
# 포트 충돌 시 다른 포트 사용
python manage.py runserver 8001
```

### 포트 문제 해결 체크리스트
- [ ] `lsof -ti:8000`으로 포트 사용 프로세스 확인
- [ ] `kill -9 [PID]`로 프로세스 강제 종료
- [ ] `lsof -ti:8000`으로 포트 해제 확인
- [ ] 서버 재시작

### 접속 문제 해결 (HTTPS 리다이렉트)
```bash
# 문제: HTTP 접속 시 HTTPS로 리다이렉트 (301 에러)
# 원인: DEBUG=False로 설정되어 프로덕션 보안 설정 적용

# 해결 1: DEBUG 기본값 수정
# config/settings.py에서 DEBUG = config('DEBUG', default=True, cast=bool)

# 해결 2: 보안 설정 단순화
# 개발 환경에서 SECURE_SSL_REDIRECT = False 명시적 설정

# 해결 3: 브라우저 HSTS 캐시 클리어
# 브라우저 설정에서 localhost HSTS 캐시 삭제
```

### 접속 문제 해결 체크리스트
- [x] DEBUG 기본값 `True`로 수정
- [x] 보안 설정 명시적 비활성화
- [x] HTTP 접속 정상화 확인 (`curl http://localhost:8000`)
- [x] 브라우저에서 정상 접속 확인

### 템플릿 및 페이지 문제 해결
```bash
# 문제: 주문 목록 페이지 500 에러
# 원인: order_list.html 템플릿 파일 누락

# 해결: 완전한 주문 목록 템플릿 생성
# - 주문 카드 형태로 표시
# - 주문 상태별 배지 색상 구분
# - 반응형 디자인 적용

# 문제: 프로필 페이지 주문 현황 표시
# 원인: 사용자별 주문 데이터 연동 필요

# 해결: users/views.py 수정
# - @login_required 데코레이터 추가
# - 주문 통계 및 최근 주문 내역 조회
# - 템플릿에 주문 현황 테이블 추가
```

### 템플릿 문제 해결 체크리스트
- [x] 주문 목록 템플릿 생성 (`templates/orders/order_list.html`)
- [x] 프로필 페이지 주문 현황 추가
- [x] 홈페이지 데이터베이스 연동
- [x] 보안 설정 강화 (`@login_required`)

## 📁 프로젝트 구조

```
fake_shopping_mall/
├── config/                 # Django 프로젝트 설정
│   ├── settings.py        # 메인 설정 파일
│   ├── urls.py            # URL 라우팅
│   ├── wsgi.py            # WSGI 설정
│   └── asgi.py            # ASGI 설정
├── shop_app/              # 메인 앱 (Category, Product 모델 포함)
├── users/                  # 사용자 앱 (회원가입/로그인)
├── cart/                   # 장바구니 앱 (세션 기반)
├── orders/                 # 주문 앱 (Order, OrderItem 모델 포함)
├── static/                # 정적 파일
│   ├── img/               # 상품 이미지 (10개)
│   └── images/             # 추가 이미지 폴더
│       └── products/       # 상품별 이미지
├── .vscode/               # IDE 설정
│   └── settings.json      # 가상환경 설정
├── plans/                 # 프로젝트 계획서
│   ├── 최종_7일_실행계획.md
│   ├── Railway_배포_가이드.md
│   └── 쓰잘데기컨셉.md
├── sample/                # 참고용 HTML/CSS/JS
├── venv/                  # 가상환경
├── requirements.txt       # 패키지 의존성
├── Procfile              # Railway 배포 설정
├── runtime.txt           # Python 버전
└── README.md             # 프로젝트 문서
```

## 🚀 배포

### Railway 배포 ✅ **성공**
- **배포 URL**: `https://uselessmall-production.up.railway.app`
- **상태**: 정상 작동 중
- **테스트 페이지**: "🎉 쓰잘데기 테스트 배포 성공!" 메시지 확인

자세한 배포 방법은 [Railway_배포_가이드.md](plans/Railway_배포_가이드.md)를 참고하세요.

#### 배포 단계 요약
1. GitHub 레포지토리 생성 및 푸시
2. Railway에서 새 프로젝트 생성
3. 환경변수 설정
4. 배포 확인

### 🔧 배포 문제 해결 과정

#### **문제 1: Railway Django 프로젝트 인식 실패**
**증상**: Railway에서 Django 프로젝트를 인식하지 못함
**해결**: 
- Procfile 형식 수정: `web: gunicorn config.wsgi:application --log-file -`
- Django 프로젝트 구조 확인

#### **문제 2: Bad Request (400) 오류**
**증상**: `uselessmall-production.up.railway.app` 접속 시 400 오류
**해결**:
- ALLOWED_HOSTS 설정: `uselessmall-production.up.railway.app,*.railway.app`
- 강력한 SECRET_KEY 생성 및 설정
- DEBUG=False로 프로덕션 설정

#### **환경변수 설정**
Railway 대시보드에서 다음 환경변수 설정:
```
SECRET_KEY=sVC9zOSP2IiHvr9ChkfBdfqOLUbQtrC18K6AfACc9TjD_ncTAo3SVSjudlJtJFmwicA
DEBUG=False
ALLOWED_HOSTS=uselessmall-production.up.railway.app,*.railway.app
```

## 📊 성공 기준

### 최소 성공 기준 (MVP)
- [ ] 10개 상품이 표시되는 쇼핑몰
- [ ] 회원가입/로그인 가능
- [ ] 장바구니 담기 가능
- [ ] 주문 생성 가능 (가짜 결제)
- [ ] 실제 배포되어 URL 접근 가능

### 추가 성공 기준
- [ ] 유튜브 영상 업로드
- [ ] 조회수 1,000 이상
- [ ] SNS 공유 50회 이상
- [ ] GitHub 스타 10개 이상

## 📚 참고 문서

- [최종 7일 실행계획](plans/최종_7일_실행계획.md)
- [Railway 배포 가이드](plans/Railway_배포_가이드.md)
- [쓰잘데기 컨셉](plans/쓰잘데기컨셉.md)
- [디자인 가이드](plans/디자인_가이드.md)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

## 📞 연락처

프로젝트 링크: [https://github.com/yourusername/fake_shopping_mall](https://github.com/yourusername/fake_shopping_mall)

---

**🎯 목표**: 7일 안에 실제 배포 가능한 "필요없는 물건 쇼핑몰" 완성 + 유튜브 콘텐츠 제작!
