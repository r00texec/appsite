// ============================================
// AvtoWay - Главный скрипт
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initHamburger();
    initFormValidation();
    initSmoothScroll();
    initScrollAnimations();
    initFAQ();
    initStats();
});

// ============================================
// Hamburger Menu
// ============================================

function initHamburger() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        
        const spans = hamburger.querySelectorAll('span');
        spans.forEach(span => span.style.transition = 'all 0.3s ease');
        
        if (navLinks.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(10px, 10px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -7px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    navLinks.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            const spans = hamburger.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar')) {
            navLinks.classList.remove('active');
            const spans = hamburger.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
}

// ============================================
// Form Validation
// ============================================

function initFormValidation() {
    const form = document.querySelector('.contact-form');
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = form.querySelector('input[placeholder="Ваше имя"]');
        const email = form.querySelector('input[placeholder*="Email"]');
        const message = form.querySelector('textarea[placeholder*="Сообщение"]');

        if (!name.value.trim()) {
            showError(name, 'Пожалуйста, введите имя');
            return;
        }

        if (!email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            showError(email, 'Пожалуйста, введите корректный email');
            return;
        }

        if (!message.value.trim()) {
            showError(message, 'Пожалуйста, введите сообщение');
            return;
        }

        clearErrors(form);
        showSuccess(submitBtn);
        form.reset();
    });

    form.querySelectorAll('input, textarea').forEach(field => {
        field.addEventListener('input', () => {
            clearFieldError(field);
        });
    });
}

function showError(field, message) {
    clearFieldError(field);
    
    const wrapper = field.parentElement;
    const error = document.createElement('div');
    error.className = 'error-message';
    error.style.cssText = `
        color: #e74c3c;
        font-size: 0.85rem;
        margin-top: 0.3rem;
        animation: slideInLeft 0.3s ease;
    `;
    error.textContent = message;
    
    wrapper.appendChild(error);
    field.style.borderColor = '#e74c3c';
}

function clearFieldError(field) {
    const error = field.parentElement.querySelector('.error-message');
    if (error) error.remove();
    field.style.borderColor = '';
}

function clearErrors(form) {
    form.querySelectorAll('.error-message').forEach(err => err.remove());
    form.querySelectorAll('input, textarea').forEach(field => {
        field.style.borderColor = '';
    });
}

function showSuccess(btn) {
    const originalText = btn.textContent;
    btn.textContent = '✓ Спасибо! Сообщение отправлено';
    btn.style.background = 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)';
    
    setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
    }, 3000);
}

// ============================================
// Smooth Scroll
// ============================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const element = document.querySelector(href);
            
            if (element) {
                const offsetTop = element.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ============================================
// Scroll Animations
// ============================================

function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.service-card, .about-text, .contact-item, .stat-item, .advantage-item, .faq-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ============================================
// FAQ Аккордион
// ============================================

function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });
                
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });
}

// ============================================
// Счётчик статистики
// ============================================

function initStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    let hasAnimated = false;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                statNumbers.forEach(el => {
                    animateCounter(el);
                });
            }
        });
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        observer.observe(statsSection);
    }
}

function animateCounter(element) {
    const target = element.textContent;
    const number = parseInt(target.replace(/[^0-9]/g, ''));
    const duration = 2000;
    const startTime = Date.now();

    const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const current = Math.floor(number * progress);
        
        element.textContent = current.toLocaleString('ru-RU') + (target.includes('+') ? '+' : target.match(/[^0-9]+$/) || '');
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            element.textContent = target;
        }
    };

    animate();
}

// ============================================
// Active link highlighting
// ============================================

window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section, header');

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (scrollY >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// ============================================
// Dock Navigation
// ============================================

const dockItems = document.querySelectorAll('.dock-item');

dockItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Эффект клика
        item.style.transform = 'scale(0.85) translateY(-15px)';
        setTimeout(() => {
            item.style.transform = '';
        }, 120);
        
        // Переходим на нужную секцию
        const href = item.getAttribute('href');
        if (href === 'https://t.me/autoway') {
            window.open(href, '_blank');
        } else if (href.startsWith('#')) {
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                highlightDockItem(href);
            }
        }
    });
});

function highlightDockItem(sectionId) {
    dockItems.forEach(item => {
        item.style.opacity = '0.7';
    });
    
    const activeItem = document.querySelector(`.dock-item[href="${sectionId}"]`);
    if (activeItem) {
        activeItem.style.opacity = '1';
    }
}

// Обновляем dock при скролле
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('[id]');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.pageYOffset >= sectionTop - 300) {
            current = `#${section.getAttribute('id')}`;
        }
    });
    
    if (current) {
        highlightDockItem(current);
    }
}, { passive: true });


console.log('✓ AvtoWay - приложение загружено успешно!');
