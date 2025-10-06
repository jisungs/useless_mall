// 쓰잘데기 쇼핑몰 JavaScript

// 장바구니 데이터
let cart = [];

// DOM 요소들
const cartItemsContainer = document.getElementById('cart-items');
const cartSummaryContainer = document.getElementById('cart-summary');
const cartListContainer = document.getElementById('cart-list');
const totalPriceElement = document.getElementById('total-price');

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    loadCartFromStorage();
    updateCartDisplay();
    initializeAnimations();
});

// 장바구니에 상품 추가
function addToCart(productName, price) {
    // 이미 장바구니에 있는 상품인지 확인
    const existingItem = cart.find(item => item.name === productName);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    // 로컬 스토리지에 저장
    saveCartToStorage();
    
    // 장바구니 표시 업데이트
    updateCartDisplay();
    
    // 성공 메시지 표시
    showAlert(`${productName}이(가) 장바구니에 추가되었습니다!`, 'success');
    
    // 장바구니 섹션으로 스크롤
    document.getElementById('cart').scrollIntoView({ behavior: 'smooth' });
}

// 장바구니에서 상품 제거
function removeFromCart(productName) {
    cart = cart.filter(item => item.name !== productName);
    saveCartToStorage();
    updateCartDisplay();
    showAlert(`${productName}이(가) 장바구니에서 제거되었습니다.`, 'danger');
}

// 수량 변경
function updateQuantity(productName, newQuantity) {
    const item = cart.find(item => item.name === productName);
    if (item) {
        if (newQuantity <= 0) {
            removeFromCart(productName);
        } else {
            item.quantity = newQuantity;
            saveCartToStorage();
            updateCartDisplay();
        }
    }
}

// 장바구니 표시 업데이트
function updateCartDisplay() {
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart text-center">
                <p class="text-muted">장바구니가 비어있습니다.</p>
                <p class="text-muted">위의 상품들을 선택해보세요!</p>
            </div>
        `;
        cartSummaryContainer.style.display = 'none';
    } else {
        cartItemsContainer.innerHTML = '';
        cartSummaryContainer.style.display = 'block';
        
        // 장바구니 아이템 목록 생성
        cartListContainer.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">₩${item.price.toLocaleString()} × ${item.quantity}</div>
                </div>
                <div class="cart-item-controls">
                    <div class="quantity-control">
                        <button class="quantity-btn" onclick="updateQuantity('${item.name}', ${item.quantity - 1})">-</button>
                        <input type="number" class="quantity-input" value="${item.quantity}" 
                               onchange="updateQuantity('${item.name}', parseInt(this.value))" min="1">
                        <button class="quantity-btn" onclick="updateQuantity('${item.name}', ${item.quantity + 1})">+</button>
                    </div>
                    <button class="remove-btn" onclick="removeFromCart('${item.name}')">삭제</button>
                </div>
            </div>
        `).join('');
        
        // 총 금액 계산 및 표시
        const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        totalPriceElement.textContent = `₩${totalPrice.toLocaleString()}`;
    }
}

// 주문하기
function checkout() {
    if (cart.length === 0) {
        showAlert('장바구니가 비어있습니다.', 'danger');
        return;
    }
    
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // 주문 확인 다이얼로그
    const orderItems = cart.map(item => `${item.name} × ${item.quantity}`).join('\n');
    
    if (confirm(`주문을 확인하시겠습니까?\n\n주문 상품:\n${orderItems}\n\n총 금액: ₩${totalPrice.toLocaleString()}`)) {
        // 주문 처리 (실제로는 서버로 전송)
        processOrder();
    }
}

// 주문 처리
function processOrder() {
    // 로딩 표시
    const checkoutBtn = document.querySelector('.cart-total .btn');
    const originalText = checkoutBtn.textContent;
    checkoutBtn.innerHTML = '<span class="loading"></span> 주문 처리 중...';
    checkoutBtn.disabled = true;
    
    // 실제 주문 처리 시뮬레이션
    setTimeout(() => {
        // 주문 완료
        showAlert('주문이 완료되었습니다! 쓰잘데기를 선택해주셔서 감사합니다.', 'success');
        
        // 장바구니 비우기
        cart = [];
        saveCartToStorage();
        updateCartDisplay();
        
        // 버튼 원상복구
        checkoutBtn.textContent = originalText;
        checkoutBtn.disabled = false;
        
        // 홈으로 스크롤
        document.getElementById('home').scrollIntoView({ behavior: 'smooth' });
    }, 2000);
}

// 로컬 스토리지에 장바구니 저장
function saveCartToStorage() {
    localStorage.setItem('ssaldagi_cart', JSON.stringify(cart));
}

// 로컬 스토리지에서 장바구니 불러오기
function loadCartFromStorage() {
    const savedCart = localStorage.getItem('ssaldagi_cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
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

// 애니메이션 초기화
function initializeAnimations() {
    // 스크롤 애니메이션
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
    document.querySelectorAll('.product-card, .section-title, .section-description').forEach(el => {
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

// 검색 기능 (향후 확장용)
function searchProducts(query) {
    const products = document.querySelectorAll('.product-card');
    const searchTerm = query.toLowerCase();
    
    products.forEach(product => {
        const title = product.querySelector('.product-title').textContent.toLowerCase();
        const description = product.querySelector('.product-description').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

// 상품 필터링 (향후 확장용)
function filterProducts(category) {
    const products = document.querySelectorAll('.product-card');
    
    products.forEach(product => {
        if (category === 'all') {
            product.style.display = 'block';
        } else {
            // 카테고리별 필터링 로직
            product.style.display = 'block';
        }
    });
}

// 장바구니 아이템 수 표시 업데이트
function updateCartBadge() {
    const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartLink = document.querySelector('a[href="#cart"]');
    
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

// 장바구니 업데이트 시 배지도 업데이트
const originalUpdateCartDisplay = updateCartDisplay;
updateCartDisplay = function() {
    originalUpdateCartDisplay();
    updateCartBadge();
};

// 페이지 로드 시 배지 업데이트
document.addEventListener('DOMContentLoaded', function() {
    updateCartBadge();
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

// 반응형 메뉴 토글
function toggleMobileMenu() {
    const navbarCollapse = document.getElementById('navbarNav');
    const isExpanded = navbarCollapse.classList.contains('show');
    
    if (isExpanded) {
        navbarCollapse.classList.remove('show');
    } else {
        navbarCollapse.classList.add('show');
    }
}

// 모바일 메뉴 외부 클릭 시 닫기
document.addEventListener('click', function(e) {
    const navbar = document.querySelector('.navbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.getElementById('navbarNav');
    
    if (!navbar.contains(e.target) && navbarCollapse.classList.contains('show')) {
        navbarCollapse.classList.remove('show');
    }
});

// 페이지 성능 최적화
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// 페이지 로드 시 지연 로딩 초기화
document.addEventListener('DOMContentLoaded', function() {
    lazyLoadImages();
});

// 에러 처리
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showAlert('오류가 발생했습니다. 페이지를 새로고침해주세요.', 'danger');
});

// 오프라인 감지
window.addEventListener('online', function() {
    showAlert('인터넷 연결이 복구되었습니다.', 'success');
});

window.addEventListener('offline', function() {
    showAlert('인터넷 연결이 끊어졌습니다. 오프라인 모드로 전환됩니다.', 'warning');
});

// 상품 페이지로 이동
function goToProduct(name, price) {
    window.location.href = `product-detail.html?name=${encodeURIComponent(name)}&price=${price}`;
}
let devtools = {open: false, orientation: null};
setInterval(function() {
    if (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.inner.width > 200) {
        if (!devtools.open) {
            devtools.open = true;
            console.log('%c쓰잘데기 개발자 도구에 오신 것을 환영합니다!', 'color: #000; font-size: 20px; font-weight: bold;');
            console.log('%c이 사이트는 완전히 쓸모없는 상품들을 판매합니다.', 'color: #666; font-size: 14px;');
            console.log('%c실용성은 포기하고 재미만 추구하는 쇼핑몰입니다.', 'color: #666; font-size: 14px;');
        }
    } else {
        devtools.open = false;
    }
}, 500);
