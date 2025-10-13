// 상품상세 페이지 JavaScript

// 상품 데이터
let currentProduct = null;
let currentQuantity = 1;

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeProductDetail();
    initializeEventListeners();
    loadProductFromURL();
});

// URL에서 상품 정보 로드
function loadProductFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const productName = urlParams.get('name');
    const productPrice = urlParams.get('price');
    
    if (productName && productPrice) {
        loadProduct(productName, parseInt(productPrice));
    } else {
        // 기본 상품 로드 (투명 우산)
        loadProduct('투명 우산', 12000);
    }
}

// 상품 정보 로드
function loadProduct(name, price) {
    currentProduct = { name, price };
    
    // 상품 정보 업데이트
    document.getElementById('product-name').textContent = name;
    document.getElementById('product-price').textContent = `₩${price.toLocaleString()}`;
    document.getElementById('product-breadcrumb').textContent = name;
    
    // 상품별 상세 정보 설정
    setProductDetails(name, price);
    
    // 이미지 설정
    setProductImages(name);
    
    // 평점 설정
    setProductRating(name);
    
    // 상품 특징 설정
    setProductFeatures(name);
}

// 상품별 상세 정보 설정
function setProductDetails(name, price) {
    const descriptions = {
        '투명 우산': '비가 안 맞는 우산. 완전히 투명해서 비를 막지 못합니다. 하지만 비 오는 날 들고 다니면 모든 사람이 웃어요!',
        '소리 나는 슬리퍼': '걸을 때마다 삐삐 소리가 나는 슬리퍼. 조용한 곳에서 사용 금지. 층간소음의 새로운 차원을 경험하세요.',
        '뒤집어진 시계': '시침과 분침이 반대로 돌아가는 시계. 시간을 알 수 없습니다. 하지만 시계를 보는 재미는 배가 됩니다.',
        '구멍 난 양말': '발가락이 다 나오는 구멍이 뚫린 양말. 보온 효과 제로. 하지만 통풍은 최고입니다.',
        '무선 충전기': '충전이 안 되는 무선 충전기. 완전히 무선이지만 전력도 무선. 무선의 진정한 의미를 경험하세요.',
        '소리 안 나는 종': '울리지 않는 장식용 종. 시각적 효과만 있습니다. 하지만 조용한 환경에서는 최고의 장식입니다.'
    };
    
    const description = descriptions[name] || '완전히 쓸모없지만 재미있는 물건입니다.';
    document.getElementById('product-description').textContent = description;
    
    // 상세 설명 탭 내용 업데이트
    const detailDescription = document.getElementById('product-detail-description');
    detailDescription.innerHTML = `
        <p>${description}</p>
        <p>이 상품은 완전히 쓸모없지만 재미있는 물건입니다.</p>
        <p>실용성을 포기하고 오직 재미만을 추구하는 철학으로 만들어진 특별한 상품입니다.</p>
        <p>일상의 지루함을 깨뜨리고 웃음을 선사하는 것이 이 상품의 유일한 목적입니다.</p>
        <p>친구나 가족에게 선물하면 분명 웃음이 터질 것입니다!</p>
    `;
}

// 상품별 이미지 설정
function setProductImages(name) {
    const imageMap = {
        '투명 우산': 'https://via.placeholder.com/400x400/000000/FFFFFF?text=투명+우산',
        '소리 나는 슬리퍼': 'https://via.placeholder.com/400x400/000000/FFFFFF?text=소리+나는+슬리퍼',
        '뒤집어진 시계': 'https://via.placeholder.com/400x400/000000/FFFFFF?text=뒤집어진+시계',
        '구멍 난 양말': 'https://via.placeholder.com/400x400/000000/FFFFFF?text=구멍+난+양말',
        '무선 충전기': 'https://via.placeholder.com/400x400/000000/FFFFFF?text=무선+충전기',
        '소리 안 나는 종': 'https://via.placeholder.com/400x400/000000/FFFFFF?text=소리+안+나는+종'
    };
    
    const mainImage = imageMap[name] || 'https://via.placeholder.com/400x400/000000/FFFFFF?text=상품+이미지';
    
    document.getElementById('product-main-image').src = mainImage;
    document.getElementById('product-main-image').alt = name;
    
    // 썸네일 이미지들 설정
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, index) => {
        thumb.src = mainImage;
        thumb.alt = name;
        thumb.classList.toggle('active', index === 0);
    });
}

// 상품별 평점 설정
function setProductRating(name) {
    const ratings = {
        '투명 우산': 4.2,
        '소리 나는 슬리퍼': 4.5,
        '뒤집어진 시계': 3.8,
        '구멍 난 양말': 4.0,
        '무선 충전기': 4.3,
        '소리 안 나는 종': 3.9
    };
    
    const rating = ratings[name] || 4.0;
    document.getElementById('rating-score').textContent = rating;
    
    // 별점 표시 업데이트
    updateStarDisplay(rating);
}

// 별점 표시 업데이트
function updateStarDisplay(rating) {
    const stars = document.querySelectorAll('.stars .star');
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    stars.forEach((star, index) => {
        if (index < fullStars) {
            star.classList.add('active');
        } else if (index === fullStars && hasHalfStar) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// 상품별 특징 설정
function setProductFeatures(name) {
    const features = {
        '투명 우산': [
            '완전히 투명한 재질',
            '비를 막지 못하는 특수 기능',
            '모든 사람의 시선을 끄는 디자인',
            '비 오는 날의 새로운 경험'
        ],
        '소리 나는 슬리퍼': [
            '걸을 때마다 삐삐 소리',
            '층간소음의 새로운 차원',
            '조용한 곳에서 사용 금지',
            '운동 효과는 제로'
        ],
        '뒤집어진 시계': [
            '시침과 분침이 반대로 회전',
            '시간을 알 수 없는 특수 기능',
            '시계를 보는 새로운 재미',
            '시간 개념의 혁신'
        ],
        '구멍 난 양말': [
            '발가락이 다 나오는 구멍',
            '보온 효과 제로',
            '최고의 통풍 효과',
            '발가락 자유의지'
        ],
        '무선 충전기': [
            '충전이 안 되는 무선 기능',
            '완전히 무선인 전력',
            '무선의 진정한 의미',
            '충전의 새로운 경험'
        ],
        '소리 안 나는 종': [
            '울리지 않는 장식용 종',
            '시각적 효과만 제공',
            '조용한 환경의 최고 장식',
            '소리 없는 종의 매력'
        ]
    };
    
    const productFeatures = features[name] || ['완전히 쓸모없는 기능', '실용성 제로', '재미만 추구'];
    
    const featuresList = document.getElementById('product-features');
    featuresList.innerHTML = productFeatures.map(feature => `<li>${feature}</li>`).join('');
}

// 이벤트 리스너 초기화
function initializeEventListeners() {
    // 수량 변경
    document.getElementById('quantity').addEventListener('change', function() {
        currentQuantity = parseInt(this.value);
        if (currentQuantity < 1) {
            this.value = 1;
            currentQuantity = 1;
        }
    });
    
    // 댓글 폼 제출
    document.getElementById('commentForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitComment();
    });
    
    // 문의 폼 제출
    document.getElementById('inquiryForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitInquiry();
    });
    
    // 별점 클릭
    document.querySelectorAll('.stars .star').forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.dataset.rating);
            submitRating(rating);
        });
    });
}

// 수량 증가
function increaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    if (currentValue < 99) {
        quantityInput.value = currentValue + 1;
        currentQuantity = currentValue + 1;
    }
}

// 수량 감소
function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        currentQuantity = currentValue - 1;
    }
}

// 메인 이미지 변경
function changeMainImage(imageSrc) {
    document.getElementById('product-main-image').src = imageSrc;
    
    // 썸네일 활성화 상태 변경
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.classList.remove('active');
    });
    event.target.classList.add('active');
}

// 장바구니에 추가 (상세 페이지에서)
function addToCartFromDetail() {
    if (!currentProduct) return;
    
    // 로컬 스토리지에서 기존 장바구니 불러오기
    let cart = JSON.parse(localStorage.getItem('ssaldagi_cart') || '[]');
    
    // 이미 있는 상품인지 확인
    const existingItem = cart.find(item => item.name === currentProduct.name);
    
    if (existingItem) {
        existingItem.quantity += currentQuantity;
    } else {
        cart.push({
            name: currentProduct.name,
            price: currentProduct.price,
            quantity: currentQuantity
        });
    }
    
    // 로컬 스토리지에 저장
    localStorage.setItem('ssaldagi_cart', JSON.stringify(cart));
    
    // 성공 메시지 표시
    showAlert(`${currentProduct.name} ${currentQuantity}개가 장바구니에 추가되었습니다!`, 'success');
    
    // 장바구니 배지 업데이트
    updateCartBadge();
}

// 바로 구매
function buyNow() {
    if (!currentProduct) return;
    
    // 장바구니에 추가
    addToCartFromDetail();
    
    // 주문 확인
    const totalPrice = currentProduct.price * currentQuantity;
    const orderItems = `${currentProduct.name} × ${currentQuantity}`;
    
    if (confirm(`바로 구매하시겠습니까?\n\n주문 상품:\n${orderItems}\n\n총 금액: ₩${totalPrice.toLocaleString()}`)) {
        processOrder();
    }
}

// 주문 처리
function processOrder() {
    // 로딩 표시
    const buyBtn = document.querySelector('.btn-secondary');
    const originalText = buyBtn.textContent;
    buyBtn.innerHTML = '<span class="loading"></span> 주문 처리 중...';
    buyBtn.disabled = true;
    
    // 주문 처리 시뮬레이션
    setTimeout(() => {
        showAlert('주문이 완료되었습니다! 쓰잘데기를 선택해주셔서 감사합니다.', 'success');
        
        // 버튼 원상복구
        buyBtn.textContent = originalText;
        buyBtn.disabled = false;
        
        // 홈으로 이동
        window.location.href = 'index.html';
    }, 2000);
}

// 댓글 제출
function submitComment() {
    const commentText = document.getElementById('commentText').value.trim();
    
    if (!commentText) {
        showAlert('댓글을 입력해주세요.', 'danger');
        return;
    }
    
    // 댓글 추가 (실제로는 서버로 전송)
    addComment(commentText);
    
    // 폼 초기화
    document.getElementById('commentText').value = '';
    
    showAlert('댓글이 등록되었습니다.', 'success');
}

// 댓글 추가
function addComment(text) {
    const commentsList = document.querySelector('.comments-list');
    const commentCount = commentsList.querySelector('h5');
    const currentCount = parseInt(commentCount.textContent.match(/\d+/)[0]);
    
    // 댓글 수 업데이트
    commentCount.textContent = `고객 댓글 (${currentCount + 1})`;
    
    // 새 댓글 요소 생성
    const newComment = document.createElement('div');
    newComment.className = 'comment-item';
    newComment.innerHTML = `
        <div class="comment-header">
            <span class="commenter-name">익명</span>
            <span class="comment-date">${new Date().toLocaleDateString('ko-KR')} ${new Date().toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'})}</span>
        </div>
        <div class="comment-content">${text}</div>
    `;
    
    // 댓글 목록 맨 위에 추가
    const commentsContainer = commentsList.querySelector('.comment-item').parentNode;
    commentsContainer.insertBefore(newComment, commentsContainer.firstChild);
}

// 문의 제출
function submitInquiry() {
    const type = document.getElementById('inquiryType').value;
    const title = document.getElementById('inquiryTitle').value.trim();
    const content = document.getElementById('inquiryContent').value.trim();
    const email = document.getElementById('inquiryEmail').value.trim();
    
    if (!title || !content || !email) {
        showAlert('모든 필드를 입력해주세요.', 'danger');
        return;
    }
    
    if (!isValidEmail(email)) {
        showAlert('올바른 이메일 주소를 입력해주세요.', 'danger');
        return;
    }
    
    // 문의 추가 (실제로는 서버로 전송)
    addInquiry(type, title, content, email);
    
    // 폼 초기화
    document.getElementById('inquiryForm').reset();
    
    showAlert('문의가 등록되었습니다. 빠른 시일 내에 답변드리겠습니다.', 'success');
}

// 문의 추가
function addInquiry(type, title, content, email) {
    const inquiryList = document.querySelector('.inquiry-list');
    
    // 새 문의 요소 생성
    const newInquiry = document.createElement('div');
    newInquiry.className = 'inquiry-item';
    newInquiry.innerHTML = `
        <div class="inquiry-header">
            <span class="inquiry-title">${title}</span>
            <span class="inquiry-status pending">답변대기</span>
        </div>
        <div class="inquiry-content">${content}</div>
        <div class="inquiry-date">${new Date().toLocaleDateString('ko-KR')}</div>
    `;
    
    // 문의 목록 맨 위에 추가
    const inquiryContainer = inquiryList.querySelector('.inquiry-item').parentNode;
    inquiryContainer.insertBefore(newInquiry, inquiryContainer.firstChild);
}

// 평점 제출
function submitRating(rating) {
    if (!currentProduct) return;
    
    // 평점 업데이트 (실제로는 서버로 전송)
    updateRating(rating);
    
    showAlert(`${rating}점으로 평가해주셔서 감사합니다!`, 'success');
}

// 평점 업데이트
function updateRating(newRating) {
    const currentRating = parseFloat(document.getElementById('rating-score').textContent);
    const currentCount = parseInt(document.querySelector('.rating-count').textContent.match(/\d+/)[0]);
    
    // 새로운 평점 계산 (간단한 평균)
    const newAverage = ((currentRating * currentCount) + newRating) / (currentCount + 1);
    
    // 평점 업데이트
    document.getElementById('rating-score').textContent = newAverage.toFixed(1);
    document.querySelector('.rating-count').textContent = `(${currentCount + 1}명 평가)`;
    
    // 별점 표시 업데이트
    updateStarDisplay(newAverage);
    
    // 탭 제목 업데이트
    document.getElementById('reviews-tab').textContent = `고객평점 (${currentCount + 1})`;
}

// 이메일 유효성 검사
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// 상품 페이지로 이동
function goToProduct(name, price) {
    window.location.href = `product-detail.html?name=${encodeURIComponent(name)}&price=${price}`;
}

// 알림 메시지 표시
function showAlert(message, type = 'info') {
    // 기존 알림 제거
    const existingAlert = document.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // 새 알림 생성
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // 페이지 상단에 추가
    document.body.insertBefore(alertDiv, document.body.firstChild);
    
    // 3초 후 자동 제거
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, 3000);
}

// 장바구니 배지 업데이트
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('ssaldagi_cart') || '[]');
    const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartLink = document.querySelector('a[href="index.html#cart"]');
    
    if (cartCount > 0) {
        if (!cartLink.querySelector('.badge')) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-danger ms-1';
            badge.textContent = cartCount;
            cartLink.appendChild(badge);
        } else {
            cartLink.querySelector('.badge').textContent = cartCount;
        }
    } else {
        const badge = cartLink.querySelector('.badge');
        if (badge) {
            badge.remove();
        }
    }
}

// 페이지 초기화
function initializeProductDetail() {
    // 장바구니 배지 업데이트
    updateCartBadge();
    
    // 스크롤 애니메이션 초기화
    initializeScrollAnimations();
}

// 스크롤 애니메이션 초기화
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // 애니메이션 대상 요소들 관찰
    document.querySelectorAll('.product-card, .section-title, .tab-content-body').forEach(el => {
        observer.observe(el);
    });
}

// 네비게이션 스크롤 효과
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.backgroundColor = '#FFFFFF';
        navbar.style.backdropFilter = 'none';
    }
});

// 부드러운 스크롤
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// 키보드 단축키
document.addEventListener('keydown', function(e) {
    // Ctrl + K: 검색 포커스
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape: 모달 닫기
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// 에러 처리
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showAlert('오류가 발생했습니다. 페이지를 새로고침해주세요.', 'danger');
});

// 개발자 도구 감지 (재미 요소)
let devtools = {open: false, orientation: null};
setInterval(function() {
    if (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.inner.width > 200) {
        if (!devtools.open) {
            devtools.open = true;
            console.log('%c쓰잘데기 상품상세 페이지 개발자 도구에 오신 것을 환영합니다!', 'color: #000; font-size: 20px; font-weight: bold;');
            console.log('%c이 상품은 완전히 쓸모없지만 재미있습니다.', 'color: #666; font-size: 14px;');
            console.log('%c실용성은 포기하고 재미만 추구하는 철학입니다.', 'color: #666; font-size: 14px;');
        }
    } else {
        devtools.open = false;
    }
}, 500);
