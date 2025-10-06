# 쓰잘데기 샘플 파일 사용 가이드

## 📁 파일 구조

```
sample/
├── index.html          # 메인 HTML 파일
├── styles.css          # 디자인 시스템 CSS
├── script.js           # JavaScript 기능
└── README.md           # 이 파일
```

## 🚀 실행 방법

### 1. 로컬 서버 실행
```bash
# Python 3 사용
python -m http.server 8000

# Python 2 사용
python -m SimpleHTTPServer 8000

# Node.js 사용 (http-server 설치 필요)
npx http-server

# VS Code Live Server 확장 사용
# index.html 우클릭 → "Open with Live Server"
```

### 2. 브라우저에서 확인
```
http://localhost:8000
```

## 🎨 디자인 특징

### ✅ 구현된 기능
- **미니멀 디자인**: 화이트 앤 블랙 기반
- **궁서체 폰트**: Noto Serif KR 사용
- **반응형 레이아웃**: 모바일, 태블릿, 데스크톱 대응
- **Bootstrap 5**: 기본 UI 컴포넌트 활용
- **커스텀 스타일**: 디자인 가이드에 맞는 스타일링

### 🛍️ 쇼핑몰 기능
- **상품 카드**: 6개 샘플 상품 표시
- **장바구니**: 상품 추가/제거/수량 변경
- **로컬 스토리지**: 장바구니 데이터 저장
- **주문 시뮬레이션**: 가짜 결제 프로세스
- **알림 시스템**: 성공/오류 메시지

### 🎭 애니메이션 효과
- **페이드 인**: 스크롤 시 요소 등장
- **호버 효과**: 카드 리프트, 버튼 변화
- **부드러운 스크롤**: 네비게이션 링크
- **로딩 애니메이션**: 주문 처리 시

## 📱 반응형 디자인

### 모바일 (768px 이하)
- 단일 컬럼 그리드
- 세로 네비게이션 메뉴
- 터치 친화적 버튼 크기

### 태블릿 (769px - 1024px)
- 2열 그리드 레이아웃
- 중간 크기 폰트

### 데스크톱 (1025px 이상)
- 3열 그리드 레이아웃
- 전체 기능 활용

## 🛠️ 커스터마이징

### 색상 변경
```css
:root {
    --primary-black: #000000;  /* 메인 색상 */
    --primary-white: #FFFFFF;  /* 배경 색상 */
    --accent-red: #F44336;     /* 강조 색상 */
}
```

### 폰트 변경
```css
:root {
    --font-primary: 'Your-Font', serif;
}
```

### 간격 조정
```css
:root {
    --space-md: 16px;  /* 기본 간격 */
    --space-lg: 24px;  /* 큰 간격 */
}
```

## 🔧 JavaScript 기능

### 장바구니 관리
```javascript
// 상품 추가
addToCart('상품명', 가격);

// 상품 제거
removeFromCart('상품명');

// 수량 변경
updateQuantity('상품명', 새수량);
```

### 알림 표시
```javascript
showAlert('메시지', 'success');  // 성공
showAlert('메시지', 'danger');   // 오류
showAlert('메시지', 'warning');  // 경고
```

## 📦 Bootstrap 컴포넌트

### 사용된 컴포넌트
- **Navbar**: 네비게이션 바
- **Grid**: 반응형 그리드
- **Buttons**: 버튼 스타일
- **Cards**: 상품 카드
- **Alerts**: 알림 메시지

### 커스터마이징
```css
/* Bootstrap 변수 오버라이드 */
:root {
    --bs-primary: var(--primary-black);
    --bs-border-radius: 0;
    --bs-font-sans-serif: var(--font-primary);
}
```

## 🎯 브랜드 아이덴티티

### "쓰잘데기" 컨셉
- **아이러니**: 완전히 쓸모없는 상품들
- **유머**: 재미있는 상품 설명
- **미니멀**: 깔끔한 디자인
- **일관성**: 전체적인 톤앤매너

### 샘플 상품들
1. **투명 우산**: 비를 막지 못하는 우산
2. **소리 나는 슬리퍼**: 걸을 때마다 삐삐 소리
3. **뒤집어진 시계**: 시침과 분침이 반대로
4. **구멍 난 양말**: 발가락이 다 나오는 양말
5. **무선 충전기**: 충전이 안 되는 충전기
6. **소리 안 나는 종**: 울리지 않는 종

## 🚀 Django 연동 준비

### 템플릿 변환
이 HTML 파일을 Django 템플릿으로 변환할 때:

1. **정적 파일 연결**
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<script src="{% static 'js/script.js' %}"></script>
```

2. **동적 데이터**
```html
{% for product in products %}
<div class="product-card">
    <h3>{{ product.name }}</h3>
    <p class="product-price">₩{{ product.price }}</p>
</div>
{% endfor %}
```

3. **CSRF 토큰**
```html
{% csrf_token %}
```

## 📋 체크리스트

### ✅ 완성된 기능
- [x] 반응형 레이아웃
- [x] 장바구니 기능
- [x] 로컬 스토리지
- [x] 애니메이션 효과
- [x] 알림 시스템
- [x] 부드러운 스크롤
- [x] 모바일 최적화

### 🔄 향후 개선사항
- [ ] 실제 이미지 추가
- [ ] 검색 기능
- [ ] 필터링 기능
- [ ] 사용자 리뷰
- [ ] 소셜 공유
- [ ] 다크 모드

## 🎨 디자인 가이드 준수

이 샘플은 `디자인_가이드.md`의 모든 규칙을 준수합니다:

- ✅ 미니멀리즘 원칙
- ✅ 화이트 앤 블랙 컬러 팔레트
- ✅ 궁서체 기반 타이포그래피
- ✅ Bootstrap 기본 UI 활용
- ✅ 일관된 스타일링
- ✅ 반응형 디자인

## 📞 문의

이 샘플 파일에 대한 질문이나 개선 제안이 있으시면 언제든지 연락주세요!

---

**쓰잘데기** - 세상에서 제일 쓸모없는 상점 🛍️
