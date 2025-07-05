#!/bin/bash

echo "🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ AI АГЕНТА НА RENDER.COM"
echo "================================================="

# Проверяем наличие необходимых инструментов
if ! command -v curl &> /dev/null; then
    echo "❌ curl не найден. Установите curl и попробуйте снова."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git не найден. Установите Git и попробуйте снова."
    exit 1
fi

# Запрашиваем API ключ (безопасно)
echo "🔑 Введите ваш Render API ключ:"
read -s RENDER_API_KEY

if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ API ключ не может быть пустым!"
    exit 1
fi

echo "✅ API ключ получен"

# Проверяем подключение к Render API
echo "🔍 Проверка подключения к Render API..."
response=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $RENDER_API_KEY" https://api.render.com/v1/services)

if [ "$response" != "200" ]; then
    echo "❌ Ошибка подключения к Render API. Проверьте API ключ."
    exit 1
fi

echo "✅ Подключение к Render API успешно"

# Подготовка Git репозитория
echo "📝 Подготовка Git репозитория..."

# Проверяем, инициализирован ли Git
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git репозиторий инициализирован"
fi

# Добавляем файлы
git add .
git commit -m "🤖 AI Agent ready for Render deployment" 2>/dev/null || echo "📦 Файлы уже закоммичены"

# Проверяем наличие remote origin
if ! git remote get-url origin &> /dev/null; then
    echo "📋 GitHub репозиторий не настроен."
    echo "Создайте репозиторий на GitHub и добавьте remote:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/ai-agent-earning.git"
    echo "git push -u origin main"
    echo ""
    read -p "Нажмите Enter когда репозиторий будет готов на GitHub..."
fi

# Получаем URL репозитория
REPO_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REPO_URL" ]; then
    echo "❌ GitHub репозиторий не настроен. Настройте и попробуйте снова."
    exit 1
fi

echo "✅ GitHub репозиторий: $REPO_URL"

# Пушим код на GitHub
echo "📤 Загрузка кода на GitHub..."
git push origin main 2>/dev/null || echo "⚠️ Код уже загружен или нужно настроить доступ"

# Создаем сервис на Render через API
echo "🎯 Создание сервиса на Render..."

# Извлекаем информацию о репозитории
REPO_FULL_NAME=$(echo $REPO_URL | sed 's/.*github\.com[:/]\([^/]*\/[^/.]*\).*/\1/')

# JSON payload для создания сервиса
JSON_PAYLOAD=$(cat <<EOF
{
  "name": "ai-agent-earning",
  "type": "web_service",
  "repo": "https://github.com/$REPO_FULL_NAME",
  "branch": "main",
  "buildCommand": "pip install -r requirements.txt",
  "startCommand": "python main.py",
  "plan": "free",
  "env": "python",
  "envVars": [
    {
      "key": "DAILY_EARNING_GOAL",
      "value": "1.0"
    },
    {
      "key": "MAX_DAILY_TASKS", 
      "value": "10"
    },
    {
      "key": "RISK_TOLERANCE",
      "value": "0.3"
    },
    {
      "key": "PORT",
      "value": "8080"
    }
  ],
  "healthCheckPath": "/",
  "autoDeploy": true
}
EOF
)

# Отправляем запрос на создание сервиса
echo "🚀 Отправка запроса на создание сервиса..."

response=$(curl -s -X POST \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD" \
  https://api.render.com/v1/services)

# Проверяем ответ
service_id=$(echo $response | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
service_url=$(echo $response | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

if [ ! -z "$service_id" ]; then
    echo ""
    echo "🎉 УСПЕШНО! AI АГЕНТ РАЗВЕРНУТ НА RENDER!"
    echo "========================================="
    echo ""
    echo "🔗 Service ID: $service_id"
    echo "🌐 URL: $service_url"
    echo "📊 Dashboard: $service_url"
    echo "📋 API Status: $service_url/api/status"
    echo ""
    echo "⏱️  Деплой займет 5-10 минут..."
    echo "💰 После деплоя агент начнет зарабатывать $1/день автоматически!"
    echo ""
    echo "🔍 Отслеживайте процесс деплоя в панели Render:"
    echo "https://dashboard.render.com/web/$service_id"
    echo ""
else
    echo "❌ Ошибка создания сервиса:"
    echo "$response"
    echo ""
    echo "Возможные причины:"
    echo "- Неверный API ключ"
    echo "- Репозиторий недоступен"
    echo "- Лимиты аккаунта"
fi

# Очищаем переменную с API ключом
unset RENDER_API_KEY

echo "✅ Скрипт завершен"