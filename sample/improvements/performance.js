// 성능 최적화 JavaScript

// 이미지 지연 로딩
class LazyImageLoader {
    constructor() {
        this.imageObserver = null;
        this.setupObserver();
    }
    
    setupObserver() {
        const options = {
            root: null,
            rootMargin: '50px',
            threshold: 0.1
        };
        
        this.imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                    this.imageObserver.unobserve(entry.target);
                }
            });
        }, options);
    }
    
    observeImages() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            this.imageObserver.observe(img);
        });
    }
    
    loadImage(img) {
        const src = img.dataset.src;
        if (src) {
            img.src = src;
            img.classList.remove('lazy');
            img.classList.add('loaded');
            
            // 로딩 완료 이벤트
            img.addEventListener('load', () => {
                img.classList.add('fade-in');
            });
        }
    }
}

// 리소스 프리로딩
class ResourcePreloader {
    constructor() {
        this.preloadedResources = new Set();
    }
    
    preloadImage(src) {
        if (this.preloadedResources.has(src)) return;
        
        const img = new Image();
        img.src = src;
        this.preloadedResources.add(src);
    }
    
    preloadCSS(href) {
        if (this.preloadedResources.has(href)) return;
        
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'style';
        link.href = href;
        document.head.appendChild(link);
        this.preloadedResources.add(href);
    }
    
    preloadJS(src) {
        if (this.preloadedResources.has(src)) return;
        
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'script';
        link.href = src;
        document.head.appendChild(link);
        this.preloadedResources.add(src);
    }
}

// 캐시 관리
class CacheManager {
    constructor() {
        this.cache = new Map();
        this.maxSize = 100;
    }
    
    set(key, value, ttl = 300000) { // 기본 5분 TTL
        const item = {
            value: value,
            expiry: Date.now() + ttl
        };
        
        this.cache.set(key, item);
        
        // 캐시 크기 제한
        if (this.cache.size > this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
    }
    
    get(key) {
        const item = this.cache.get(key);
        
        if (!item) return null;
        
        if (Date.now() > item.expiry) {
            this.cache.delete(key);
            return null;
        }
        
        return item.value;
    }
    
    clear() {
        this.cache.clear();
    }
}

// 디바운스/스로틀 함수
class PerformanceUtils {
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// 성능 모니터링
class PerformanceMonitor {
    constructor() {
        this.metrics = {};
        this.setupMonitoring();
    }
    
    setupMonitoring() {
        // 페이지 로드 시간 측정
        window.addEventListener('load', () => {
            this.measurePageLoad();
        });
        
        // 리소스 로딩 시간 측정
        this.measureResourceTiming();
        
        // 사용자 상호작용 측정
        this.measureUserInteractions();
    }
    
    measurePageLoad() {
        const navigation = performance.getEntriesByType('navigation')[0];
        
        this.metrics.pageLoad = {
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
            totalTime: navigation.loadEventEnd - navigation.fetchStart
        };
        
        console.log('Page Load Metrics:', this.metrics.pageLoad);
    }
    
    measureResourceTiming() {
        const resources = performance.getEntriesByType('resource');
        
        this.metrics.resources = resources.map(resource => ({
            name: resource.name,
            duration: resource.duration,
            size: resource.transferSize
        }));
        
        console.log('Resource Timing:', this.metrics.resources);
    }
    
    measureUserInteractions() {
        let interactionCount = 0;
        const startTime = Date.now();
        
        ['click', 'scroll', 'keydown'].forEach(eventType => {
            document.addEventListener(eventType, () => {
                interactionCount++;
            });
        });
        
        // 5초마다 상호작용 통계 업데이트
        setInterval(() => {
            const timeElapsed = Date.now() - startTime;
            const interactionsPerSecond = interactionCount / (timeElapsed / 1000);
            
            this.metrics.userInteractions = {
                totalInteractions: interactionCount,
                interactionsPerSecond: interactionsPerSecond,
                timeElapsed: timeElapsed
            };
        }, 5000);
    }
    
    getMetrics() {
        return this.metrics;
    }
}

// 메모리 사용량 모니터링
class MemoryMonitor {
    constructor() {
        this.setupMonitoring();
    }
    
    setupMonitoring() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                console.log('Memory Usage:', {
                    used: Math.round(memory.usedJSHeapSize / 1048576) + ' MB',
                    total: Math.round(memory.totalJSHeapSize / 1048576) + ' MB',
                    limit: Math.round(memory.jsHeapSizeLimit / 1048576) + ' MB'
                });
                
                // 메모리 사용량이 높으면 경고
                if (memory.usedJSHeapSize / memory.jsHeapSizeLimit > 0.8) {
                    console.warn('High memory usage detected!');
                }
            }, 10000); // 10초마다 체크
        }
    }
}

// 코드 분할 및 지연 로딩
class CodeSplitter {
    constructor() {
        this.loadedModules = new Set();
    }
    
    async loadModule(moduleName) {
        if (this.loadedModules.has(moduleName)) {
            return;
        }
        
        try {
            // 동적 import를 사용한 모듈 로딩
            const module = await import(`./modules/${moduleName}.js`);
            this.loadedModules.add(moduleName);
            return module;
        } catch (error) {
            console.error(`Failed to load module ${moduleName}:`, error);
            throw error;
        }
    }
    
    async loadModuleWhenNeeded(moduleName, condition) {
        if (condition && !this.loadedModules.has(moduleName)) {
            return await this.loadModule(moduleName);
        }
    }
}

// 전역 인스턴스 생성
const lazyImageLoader = new LazyImageLoader();
const resourcePreloader = new ResourcePreloader();
const cacheManager = new CacheManager();
const performanceMonitor = new PerformanceMonitor();
const memoryMonitor = new MemoryMonitor();
const codeSplitter = new CodeSplitter();

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 이미지 지연 로딩 시작
    lazyImageLoader.observeImages();
    
    // 중요한 리소스 프리로드
    resourcePreloader.preloadImage('images/hero-bg.jpg');
    resourcePreloader.preloadCSS('styles.css');
    
    // 성능 최적화된 이벤트 리스너
    const debouncedScroll = PerformanceUtils.debounce(handleScroll, 100);
    const throttledResize = PerformanceUtils.throttle(handleResize, 250);
    
    window.addEventListener('scroll', debouncedScroll);
    window.addEventListener('resize', throttledResize);
});

// 스크롤 핸들러 (디바운스 적용)
function handleScroll() {
    // 스크롤 관련 로직
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    } else {
        navbar.style.backgroundColor = '#FFFFFF';
    }
}

// 리사이즈 핸들러 (스로틀 적용)
function handleResize() {
    // 리사이즈 관련 로직
    const viewportWidth = window.innerWidth;
    
    if (viewportWidth < 768) {
        // 모바일 최적화
        document.body.classList.add('mobile-view');
    } else {
        document.body.classList.remove('mobile-view');
    }
}

// 캐시된 데이터 가져오기
function getCachedData(key) {
    return cacheManager.get(key);
}

// 데이터 캐시에 저장
function setCachedData(key, data, ttl) {
    cacheManager.set(key, data, ttl);
}

// 성능 메트릭 가져오기
function getPerformanceMetrics() {
    return performanceMonitor.getMetrics();
}

// 메모리 정리
function cleanupMemory() {
    // 불필요한 이벤트 리스너 제거
    // 사용하지 않는 DOM 요소 제거
    // 캐시 정리
    cacheManager.clear();
    
    // 가비지 컬렉션 강제 실행 (가능한 경우)
    if (window.gc) {
        window.gc();
    }
}

// 페이지 언로드 시 정리
window.addEventListener('beforeunload', function() {
    cleanupMemory();
});
