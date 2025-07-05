#!/bin/bash

echo "🚀 ПОДГОТОВКА К ДЕПЛОЮ AI АГЕНТА НА ОБЛАКО"
echo "==========================================="

# Проверяем наличие git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и попробуйте снова."
    exit 1
fi

echo "📝 Инициализация Git репозитория..."
git init

echo "📦 Добавление файлов..."
git add .

echo "💾 Создание коммита..."
git commit -m "🤖 Автономный AI Агент для заработка $1/день

Особенности:
- ✅ Умная ротация 10 Gemini API ключей
- ✅ Экономия запросов через накопление контекста
- ✅ 4 стратегии заработка с AI оптимизацией
- ✅ Веб dashboard для мониторинга
- ✅ Готов к деплою на бесплатный хостинг
- ✅ Работает 24/7 автономно

Деплой: Render.com, Railway, Fly.io
Цель: $1/день автоматического заработка"

echo "🌿 Создание main ветки..."
git branch -M main

echo ""
echo "✅ Git репозиторий готов!"
echo ""
echo "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo ""
echo "1. 🔗 Создайте репозиторий на GitHub:"
echo "   - Зайдите на https://github.com/new"
echo "   - Назовите репозиторий: ai-agent-earning"
echo "   - НЕ добавляйте README, .gitignore или LICENSE"
echo ""
echo "2. 🚀 Загрузите код на GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-agent-earning.git"
echo "   git push -u origin main"
echo ""
echo "3. 🌐 Деплой на хостинг:"
echo "   - Render.com (рекомендуется): https://render.com"
echo "   - Railway: https://railway.app" 
echo "   - Fly.io: установите CLI и запустите flyctl launch"
echo ""
echo "4. 💰 Ваш агент будет зарабатывать $1/день автономно!"
echo ""
echo "📖 Подробные инструкции: см. DEPLOYMENT.md"
echo ""