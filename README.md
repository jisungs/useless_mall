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

### ✅ 완료된 작업 (Day 0)

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

### 📦 현재 상품 목록 (3개 완료)

1. **100명 유튜버 포토카드** - 100명 구독자를 가진 유튜버 지성스의 친필 사인이 담긴 포토카드
2. **지성스의 사소한 이야기** - 100명 구독자를 보유한 유튜버 지성스의 생각이 담긴 수필집 PDF 전자책
3. **지성스의 사인이 담긴 노트** - 지성스가 직접 제작한 한지 노트, 표지에 친필 사인 포함

### 🔄 다음 작업 예정

#### **Day 1: 프로젝트 기초** (6시간)
- [ ] Django 프로젝트 생성 (products, users, cart, orders 앱)
- [ ] 데이터베이스 모델 생성 (Category, Product)
- [ ] Admin 커스터마이징
- [ ] 기본 템플릿 작성

#### **Day 2: 기본 페이지** (6시간)
- [ ] 홈페이지 개발
- [ ] 상품 목록/상세 페이지
- [ ] 스타일링 및 반응형 디자인

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

## 📁 프로젝트 구조

```
fake_shopping_mall/
├── config/                 # Django 프로젝트 설정
│   ├── settings.py        # 메인 설정 파일
│   └── urls.py            # URL 라우팅
├── test_app/              # 테스트 앱 (배포 확인용)
├── static/                # 정적 파일
│   └── img/               # 상품 이미지 (10개)
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
