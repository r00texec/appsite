# AvtoWayUz - Инструкция по развертыванию

## 🚀 Развертывание на различных платформах

### 1. Netlify (рекомендуется)

**Бесплатный хостинг с HTTPS и CDN**

1. Перейдите на [netlify.com](https://www.netlify.com)
2. Подключитесь через GitHub
3. Выберите репозиторий `my-site`
4. Нажмите "Deploy"
5. Готово! Ваш сайт будет доступен по уникальной ссылке

**Настройка базовой конфигурации:**
```
Build command: (оставить пустым)
Publish directory: . (корневая папка)
```

### 2. Vercel

1. Перейдите на [vercel.com](https://www.vercel.com)
2. Подключитесь через GitHub
3. Импортируйте проект
4. Нажмите "Deploy"

### 3. GitHub Pages

1. Откройте репозиторий на GitHub
2. Перейдите в Settings → Pages
3. Выберите "Deploy from a branch"
4. Выберите ветку `main`
5. Папка: `/ (root)`
6. Нажмите "Save"

Сайт будет доступен по адресу: `https://diasaliyev21-sudo.github.io/my-site/`

### 4. Собственный сервер (Linux/Ubuntu)

```bash
# 1. SSH подключение к серверу
ssh root@your_server_ip

# 2. Установка Nginx
sudo apt-get update
sudo apt-get install nginx

# 3. Клонирование репозитория
cd /var/www
sudo git clone https://github.com/diasaliyev21-sudo/my-site.git autoway

# 4. Настройка Nginx
sudo nano /etc/nginx/sites-available/autoway

# Вставьте это:
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    root /var/www/autoway;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

# 5. Активация конфигурации
sudo ln -s /etc/nginx/sites-available/autoway /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# 6. Установка SSL (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

### 5. Docker контейнер

**Dockerfile:**
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Запуск:**
```bash
docker build -t autoway-uz .
docker run -p 8000:80 autoway-uz
```

### 6. Cpanel/Shared Hosting

1. Подключитесь через FTP
2. Загрузите все файлы в папку `public_html`
3. Убедитесь, что `index.html` находится в корне
4. Готово!

## 🔐 Безопасность

### Рекомендации:

1. **HTTPS** - используйте только защищенное соединение
2. **CSP заголовки** - добавьте Content Security Policy
3. **Headers** - настройте правильные безопасные заголовки

### nginx.conf для безопасности:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## 📊 Мониторинг и аналитика

### Добавьте Google Analytics:

```html
<!-- В конец index.html перед </body> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

### Yandex Метрика:

```html
<!-- В конец index.html перед </body> -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrica/tag.js", "ym");

   ym(YOUR_YANDEX_ID, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true
   });
</script>
```

## 🔄 Автоматическое развертывание

### CI/CD с GitHub Actions

**`.github/workflows/deploy.yml`:**

```yaml
name: Deploy to Netlify

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v1.2
        with:
          publish-dir: '.'
          production-branch: main
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## 📱 Мобильная оптимизация

Сайт уже оптимизирован для мобильных устройств благодаря:
- Адаптивному CSS
- Viewport мета-тегу
- Оптимизированным изображениям
- Быстрой загрузке

## ⚡ Производительность

### Оптимизация:

1. Минификация CSS и JS
2. Lazy loading изображений
3. Кэширование браузера
4. GZIP сжатие

### Проверка скорости:

- [Google PageSpeed Insights](https://pagespeed.web.dev)
- [GTmetrix](https://gtmetrix.com)
- [WebPageTest](https://www.webpagetest.org)

## 📞 Поддержка доменов

Привяжите собственный домен:
1. Установите nameservers хостинга на регистраторе домена
2. Добавьте домен в настройки хостинга
3. Подождите обновления DNS (до 24 часов)

## 🎯 Готово к развертыванию!

Ваш сайт полностью готов к публикации. Выберите подходящий вариант развертывания и запустите его сегодня!
