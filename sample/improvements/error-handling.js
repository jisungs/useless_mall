// 에러 처리 및 검증 개선 JavaScript

// 폼 검증 함수들
const FormValidator = {
    // 이메일 검증
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    // 전화번호 검증
    validatePhone(phone) {
        const phoneRegex = /^[0-9-+\s()]+$/;
        return phoneRegex.test(phone) && phone.length >= 10;
    },
    
    // 필수 필드 검증
    validateRequired(value) {
        return value && value.trim().length > 0;
    },
    
    // 최소 길이 검증
    validateMinLength(value, minLength) {
        return value && value.trim().length >= minLength;
    },
    
    // 최대 길이 검증
    validateMaxLength(value, maxLength) {
        return !value || value.trim().length <= maxLength;
    }
};

// 에러 처리 클래스
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        // 사용자에게 친화적인 에러 메시지 표시
        const userMessage = this.getUserFriendlyMessage(error);
        showAlert(userMessage, 'danger');
        
        // 에러 로깅 (실제 서비스에서는 서버로 전송)
        this.logError(error, context);
    }
    
    static getUserFriendlyMessage(error) {
        if (error.name === 'NetworkError') {
            return '네트워크 연결을 확인해주세요.';
        } else if (error.name === 'ValidationError') {
            return '입력 정보를 다시 확인해주세요.';
        } else if (error.name === 'TimeoutError') {
            return '요청 시간이 초과되었습니다. 다시 시도해주세요.';
        } else {
            return '오류가 발생했습니다. 페이지를 새로고침해주세요.';
        }
    }
    
    static logError(error, context) {
        // 실제 서비스에서는 서버로 에러 로그 전송
        const errorLog = {
            message: error.message,
            stack: error.stack,
            context: context,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };
        
        // 로컬 스토리지에 임시 저장 (개발용)
        const logs = JSON.parse(localStorage.getItem('error_logs') || '[]');
        logs.push(errorLog);
        if (logs.length > 100) logs.shift(); // 최대 100개만 유지
        localStorage.setItem('error_logs', JSON.stringify(logs));
    }
}

// 네트워크 상태 모니터링
class NetworkMonitor {
    constructor() {
        this.isOnline = navigator.onLine;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            showAlert('인터넷 연결이 복구되었습니다.', 'success');
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            showAlert('인터넷 연결이 끊어졌습니다. 오프라인 모드로 전환됩니다.', 'warning');
        });
    }
    
    async checkConnection() {
        try {
            const response = await fetch('/api/health', { 
                method: 'HEAD',
                mode: 'no-cors',
                cache: 'no-cache'
            });
            return true;
        } catch (error) {
            return false;
        }
    }
}

// 로딩 상태 관리
class LoadingManager {
    constructor() {
        this.loadingElements = new Set();
    }
    
    show(element, text = '로딩 중...') {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (element) {
            element.classList.add('loading');
            element.setAttribute('aria-busy', 'true');
            element.setAttribute('aria-label', text);
            
            // 로딩 스피너 추가
            const spinner = document.createElement('div');
            spinner.className = 'loading-spinner';
            spinner.innerHTML = '<div class="spinner"></div>';
            element.appendChild(spinner);
            
            this.loadingElements.add(element);
        }
    }
    
    hide(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (element) {
            element.classList.remove('loading');
            element.removeAttribute('aria-busy');
            element.removeAttribute('aria-label');
            
            // 로딩 스피너 제거
            const spinner = element.querySelector('.loading-spinner');
            if (spinner) {
                spinner.remove();
            }
            
            this.loadingElements.delete(element);
        }
    }
    
    hideAll() {
        this.loadingElements.forEach(element => {
            this.hide(element);
        });
    }
}

// 폼 검증 및 제출 처리
class FormHandler {
    constructor(formSelector) {
        this.form = document.querySelector(formSelector);
        this.validator = FormValidator;
        this.setupValidation();
    }
    
    setupValidation() {
        if (!this.form) return;
        
        // 실시간 검증
        this.form.addEventListener('input', (e) => {
            this.validateField(e.target);
        });
        
        // 폼 제출 검증
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
    }
    
    validateField(field) {
        const rules = this.getValidationRules(field);
        const isValid = this.validateFieldRules(field, rules);
        
        this.updateFieldState(field, isValid);
        return isValid;
    }
    
    getValidationRules(field) {
        const rules = {};
        
        if (field.hasAttribute('required')) {
            rules.required = true;
        }
        
        if (field.type === 'email') {
            rules.email = true;
        }
        
        if (field.hasAttribute('minlength')) {
            rules.minLength = parseInt(field.getAttribute('minlength'));
        }
        
        if (field.hasAttribute('maxlength')) {
            rules.maxLength = parseInt(field.getAttribute('maxlength'));
        }
        
        return rules;
    }
    
    validateFieldRules(field, rules) {
        const value = field.value;
        
        if (rules.required && !this.validator.validateRequired(value)) {
            return false;
        }
        
        if (rules.email && value && !this.validator.validateEmail(value)) {
            return false;
        }
        
        if (rules.minLength && !this.validator.validateMinLength(value, rules.minLength)) {
            return false;
        }
        
        if (rules.maxLength && !this.validator.validateMaxLength(value, rules.maxLength)) {
            return false;
        }
        
        return true;
    }
    
    updateFieldState(field, isValid) {
        field.classList.toggle('is-valid', isValid);
        field.classList.toggle('is-invalid', !isValid);
        
        // 에러 메시지 표시/숨김
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.style.display = isValid ? 'none' : 'block';
        }
    }
    
    async handleSubmit() {
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData);
        
        try {
            // 폼 전체 검증
            const isValid = this.validateForm();
            if (!isValid) {
                showAlert('입력 정보를 다시 확인해주세요.', 'danger');
                return;
            }
            
            // 로딩 표시
            loadingManager.show(this.form, '처리 중...');
            
            // 실제 제출 로직 (여기서는 시뮬레이션)
            await this.submitForm(data);
            
            showAlert('성공적으로 처리되었습니다.', 'success');
            this.form.reset();
            
        } catch (error) {
            ErrorHandler.handle(error, 'Form Submission');
        } finally {
            loadingManager.hide(this.form);
        }
    }
    
    validateForm() {
        const fields = this.form.querySelectorAll('input, textarea, select');
        let isValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    async submitForm(data) {
        // 실제 서비스에서는 서버로 데이터 전송
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // 시뮬레이션: 90% 성공률
                if (Math.random() > 0.1) {
                    resolve(data);
                } else {
                    reject(new Error('서버 오류가 발생했습니다.'));
                }
            }, 1000);
        });
    }
}

// 전역 인스턴스 생성
const networkMonitor = new NetworkMonitor();
const loadingManager = new LoadingManager();

// 페이지 로드 시 폼 핸들러 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 댓글 폼
    new FormHandler('#commentForm');
    
    // 문의 폼
    new FormHandler('#inquiryForm');
    
    // 기타 폼들...
});

// 전역 에러 핸들러
window.addEventListener('error', function(e) {
    ErrorHandler.handle(e.error, 'Global Error Handler');
});

window.addEventListener('unhandledrejection', function(e) {
    ErrorHandler.handle(e.reason, 'Unhandled Promise Rejection');
});

// 네트워크 상태 확인 함수
async function checkNetworkStatus() {
    const isConnected = await networkMonitor.checkConnection();
    if (!isConnected) {
        showAlert('네트워크 연결을 확인해주세요.', 'warning');
    }
    return isConnected;
}

// 안전한 API 호출 함수
async function safeApiCall(url, options = {}) {
    try {
        const isOnline = await checkNetworkStatus();
        if (!isOnline) {
            throw new Error('네트워크 연결이 없습니다.');
        }
        
        const response = await fetch(url, {
            ...options,
            timeout: 10000 // 10초 타임아웃
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        ErrorHandler.handle(error, 'API Call');
        throw error;
    }
}
