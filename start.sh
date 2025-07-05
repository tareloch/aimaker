#!/bin/bash

echo "🤖 АВТОНОМНЫЙ AI АГЕНТ - БЫСТРЫЙ ЗАПУСК"
echo "======================================"
echo

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден"
    exit 1
fi

echo "✅ Python3 найден"

# Создание директорий
mkdir -p logs data models reports config
echo "✅ Директории созданы"

# Создание .env файла если его нет
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Файл .env создан"
        echo "⚠️  ВНИМАНИЕ: Отредактируйте .env и добавьте API ключи!"
    fi
fi

echo
echo "🚀 Запуск агента..."
echo "📊 Dashboard будет доступен на http://localhost:8080"
echo "🛑 Для остановки нажмите Ctrl+C"
echo

# Запуск агента
python3 main.py