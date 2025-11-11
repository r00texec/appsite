# Руководство по кастомизации AvtoWayUz

## 🎨 Как персонализировать сайт

### 1. Изменение контактных данных

**Файл:** `index.html`

Найдите и измените следующие данные:

```html
<!-- Телефон -->
<a href="tel:+998901234567">+998 90 123 45 67</a>

<!-- Email -->
<a href="mailto:info@autoway.uz">info@autoway.uz</a>

<!-- Telegram -->
<a href="https://t.me/AvtoWayUz" target="_blank">@AvtoWayUz</a>

<!-- Адрес -->
<p>Ташкент, Узбекистан</p>
```

### 2. Изменение цветовой схемы

**Файл:** `styles/main.css`

Найдите раздел "Основные переменные":

```css
:root {
    --primary-color: #2563eb;        /* Основной цвет */
    --secondary-color: #1e40af;      /* Вторичный цвет */
    --accent-color: #dc2626;         /* Акцентный цвет */
    --text-color: #1f2937;           /* Цвет текста */
    --light-text: #6b7280;           /* Светлый текст */
    --background-color: #ffffff;     /* Цвет фона */
    --light-bg: #f9fafb;             /* Светлый фон */
}
```

**Популярные цветовые схемы:**

Для автосервиса (красный/оранжевый):
```css
--primary-color: #dc2626;
--secondary-color: #b91c1c;
--accent-color: #f97316;
```

Для премиум сервиса (темный/золото):
```css
--primary-color: #1f2937;
--secondary-color: #111827;
--accent-color: #fbbf24;
```

### 3. Изменение услуг

**Файл:** `index.html`

Найдите секцию "Услуги" и измените содержимое:

```html
<div class="service-card">
    <div class="service-icon">
        <i class="fas fa-tools"></i>  <!-- Измените иконку -->
    </div>
    <h3>Название услуги</h3>
    <p>Описание услуги</p>
</div>
```

**Доступные иконки Font Awesome:**
- `fa-tools` - инструменты
- `fa-wrench` - гаечный ключ
- `fa-cog` - шестеренка
- `fa-car` - машина
- `fa-plug` - штепсель
- `fa-paint-brush` - кисть
- `fa-star` - звезда
- `fa-check` - галочка

[Полный список иконок](https://fontawesome.com/icons)

### 4. Добавление логотипа

**Способ 1: Текстовый логотип**

В `index.html` найдите:
```html
<div class="navbar-brand">
    <h1>AvtoWayUz</h1>
    <span class="tagline">Автосервис</span>
</div>
```

**Способ 2: Картинка логотипа**

1. Создайте папку `images/`
2. Добавьте логотип `logo.png`
3. Замените на:

```html
<div class="navbar-brand">
    <img src="images/logo.png" alt="AvtoWayUz" class="logo">
</div>
```

4. Добавьте CSS в `styles/main.css`:

```css
.navbar-brand .logo {
    height: 40px;
    width: auto;
    margin-bottom: 0.5rem;
}
```

### 5. Изменение шрифтов

**Файл:** `styles/main.css`

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
```

**Популярные комбинации:**

Для профессионального вида:
```css
font-family: 'Roboto', 'Segoe UI', sans-serif;
```

Для элегантного вида:
```css
font-family: 'Poppins', 'Segoe UI', sans-serif;
```

### 6. Добавление социальных сетей

**Файл:** `index.html`

Найдите социальные ссылки и добавьте новые:

```html
<div class="social-links">
    <a href="https://t.me/AvtoWayUz" target="_blank"><i class="fab fa-telegram"></i></a>
    <a href="https://instagram.com/autoway" target="_blank"><i class="fab fa-instagram"></i></a>
    <a href="https://facebook.com/autoway" target="_blank"><i class="fab fa-facebook"></i></a>
    <a href="https://whatsapp.com" target="_blank"><i class="fab fa-whatsapp"></i></a>
    <a href="https://youtube.com/@autoway" target="_blank"><i class="fab fa-youtube"></i></a>
</div>
```

### 7. Изменение текста "О нас"

**Файл:** `index.html`

Найдите и измените:

```html
<div class="about-text">
    <h2>О компании AvtoWayUz</h2>
    <p>Мой текст про компанию...</p>
    <ul class="about-list">
        <li><i class="fas fa-check"></i> Преимущество 1</li>
        <li><i class="fas fa-check"></i> Преимущество 2</li>
        <!-- добавьте еще пункты -->
    </ul>
</div>
```

### 8. Добавление страницы "Портфолио/Галерея"

Добавьте новый раздел в HTML:

```html
<section class="portfolio" id="portfolio">
    <div class="container">
        <h2>Наши работы</h2>
        <div class="portfolio-grid">
            <div class="portfolio-item">
                <img src="images/work1.jpg" alt="Работа 1">
                <h3>Ремонт BMW</h3>
            </div>
            <div class="portfolio-item">
                <img src="images/work2.jpg" alt="Работа 2">
                <h3>Переделка Lacetti</h3>
            </div>
            <!-- добавьте еще -->
        </div>
    </div>
</section>
```

Добавьте CSS:

```css
.portfolio {
    padding: 5rem 0;
    background-color: var(--light-bg);
}

.portfolio h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.portfolio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}

.portfolio-item {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.portfolio-item:hover {
    transform: translateY(-10px);
}

.portfolio-item img {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

.portfolio-item h3 {
    padding: 1rem;
    background: white;
    text-align: center;
}
```

### 9. Настройка формы контактов

**Для реального использования:**

Измените JavaScript в `scripts/main.js`:

```javascript
// Замените на реальный код отправки
fetch('https://your-api.com/send-message', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        showNotification('Сообщение отправлено!', 'success');
        contactForm.reset();
    }
})
.catch(error => {
    showNotification('Ошибка при отправке', 'error');
});
```

### 10. Добавление блога

Создайте файл `blog.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <!-- скопируйте head из index.html -->
    <title>Блог - AvtoWayUz</title>
</head>
<body>
    <!-- скопируйте navbar из index.html -->
    
    <section class="blog">
        <div class="container">
            <h1>Блог автосервиса</h1>
            <div class="blog-grid">
                <article class="blog-post">
                    <h2>Как часто менять масло?</h2>
                    <p class="date">15 ноября 2025</p>
                    <p>Содержание статьи...</p>
                    <a href="#" class="read-more">Читать далее →</a>
                </article>
                <!-- добавьте еще статьи -->
            </div>
        </div>
    </section>
    
    <!-- скопируйте footer из index.html -->
</body>
</html>
```

## 🚀 Быстрые советы

1. **Резервная копия** - всегда делайте резервную копию перед изменениями
2. **Тестирование** - проверяйте все на мобильных устройствах
3. **SEO** - не забывайте обновлять meta-теги
4. **Производительность** - оптимизируйте изображения перед загрузкой
5. **Безопасность** - не добавляйте конфиденциальные данные на клиент

## 📚 Полезные ресурсы

- [Font Awesome Icons](https://fontawesome.com/icons)
- [CSS Tricks](https://css-tricks.com)
- [MDN Web Docs](https://developer.mozilla.org)
- [Figma](https://figma.com) - для дизайна
- [TinyPNG](https://tinypng.com) - сжатие изображений

## 💡 Примеры готовых вариантов

### Минимальный (Start-up)
Оставьте все по умолчанию, просто измените контакты и цвета.

### Стандартный (Small Business)
Добавьте галерею работ, измените все тексты, добавьте вторую страницу с отзывами.

### Премиум (Enterprise)
Добавьте блог, систему бронирования, чат поддержки, аналитику, оптимизацию.

Успехов с кастомизацией! 🎉
