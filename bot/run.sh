#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f .env ]; then
    echo "❌ Файл .env не найден. Скопируйте .env.example и заполните токен."
    echo "   cp .env.example .env"
    exit 1
fi

if [ ! -d venv ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

echo "📦 Установка зависимостей..."
venv/bin/pip install -q -r requirements.txt

mkdir -p data

echo "🚀 Запуск бота..."
venv/bin/python bot.py
