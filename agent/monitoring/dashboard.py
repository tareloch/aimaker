"""
Веб-дашборд для мониторинга автономного агента
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn


class Dashboard:
    """Веб-дашборд для мониторинга агента"""
    
    def __init__(self, agent):
        self.agent = agent
        self.app = FastAPI(title="AI Agent Dashboard")
        self.active_connections = []
        
        # Настройка маршрутов
        self._setup_routes()
    
    def _setup_routes(self):
        """Настройка маршрутов FastAPI"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home():
            return self._get_dashboard_html()
        
        @self.app.get("/api/status")
        async def get_status():
            """Получение статуса агента"""
            return self.agent.get_status()
        
        @self.app.get("/api/strategies")
        async def get_strategies():
            """Получение информации о стратегиях"""
            if hasattr(self.agent, 'strategy_manager') and self.agent.strategy_manager:
                return self.agent.strategy_manager.get_strategy_stats()
            return {}
        
        @self.app.get("/api/earnings/history")
        async def get_earnings_history():
            """Получение истории заработка"""
            # Пока что заглушка - в будущем будет читать из базы данных
            return {
                "daily_earnings": [
                    {"date": "2024-01-01", "amount": 1.2},
                    {"date": "2024-01-02", "amount": 0.8},
                    {"date": "2024-01-03", "amount": 1.5},
                ],
                "total_earnings": 3.5
            }
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket для обновлений в реальном времени"""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                while True:
                    # Отправляем обновления каждые 5 секунд
                    status = self.agent.get_status()
                    await websocket.send_text(json.dumps({
                        "type": "status_update",
                        "data": status,
                        "timestamp": datetime.now().isoformat()
                    }))
                    await asyncio.sleep(5)
                    
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
    
    def _get_dashboard_html(self) -> str:
        """Генерация HTML для дашборда"""
        return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        
        .header h1 {
            color: #5a67d8;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #48bb78;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .card h3 {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            font-weight: 500;
            color: #4a5568;
        }
        
        .metric-value {
            font-weight: bold;
            color: #2d3748;
        }
        
        .earnings-value {
            color: #48bb78;
            font-size: 1.5em;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #48bb78, #38a169);
            border-radius: 10px;
            transition: width 0.5s ease;
        }
        
        .strategy-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            background: #f7fafc;
            border-radius: 8px;
            border-left: 4px solid #5a67d8;
        }
        
        .strategy-name {
            font-weight: 500;
        }
        
        .strategy-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .status-active {
            background: #c6f6d5;
            color: #276749;
        }
        
        .status-inactive {
            background: #fed7d7;
            color: #c53030;
        }
        
        .log-container {
            background: #1a202c;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 15px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .log-entry {
            margin-bottom: 8px;
            padding: 5px;
        }
        
        .log-entry.success {
            color: #68d391;
        }
        
        .log-entry.error {
            color: #fc8181;
        }
        
        .log-entry.warning {
            color: #f6e05e;
        }
        
        .refresh-time {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Автономный AI Агент</h1>
            <p><span class="status-indicator"></span>Статус: <span id="agent-status">Инициализация...</span></p>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>💰 Заработок</h3>
                <div class="metric">
                    <span class="metric-label">Сегодня:</span>
                    <span class="metric-value earnings-value" id="daily-earnings">$0.00</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Всего:</span>
                    <span class="metric-value" id="total-earnings">$0.00</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Цель:</span>
                    <span class="metric-value" id="daily-goal">$1.00</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                </div>
                <div style="text-align: center; margin-top: 10px; color: #666;">
                    <span id="progress-text">0% от дневной цели</span>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Статистика</h3>
                <div class="metric">
                    <span class="metric-label">Задач выполнено:</span>
                    <span class="metric-value" id="tasks-completed">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Активных стратегий:</span>
                    <span class="metric-value" id="active-strategies">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Время работы:</span>
                    <span class="metric-value" id="uptime">0ч 0м</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🎯 Стратегии</h3>
                <div id="strategies-list">
                    <div class="strategy-item">
                        <span class="strategy-name">Загрузка...</span>
                        <span class="strategy-status status-inactive">Неактивна</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>📝 Логи активности</h3>
            <div class="log-container" id="log-container">
                <div class="log-entry">Инициализация системы логирования...</div>
            </div>
        </div>
        
        <div class="refresh-time">
            Последнее обновление: <span id="last-update">—</span>
        </div>
    </div>

    <script>
        // WebSocket соединение для обновлений в реальном времени
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        let startTime = Date.now();
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            if (data.type === 'status_update') {
                updateDashboard(data.data);
            }
        };
        
        function updateDashboard(status) {
            // Обновление основных метрик
            document.getElementById('agent-status').textContent = status.is_running ? 'Активен' : 'Остановлен';
            document.getElementById('daily-earnings').textContent = `$${status.daily_earnings.toFixed(2)}`;
            document.getElementById('total-earnings').textContent = `$${status.total_earnings.toFixed(2)}`;
            document.getElementById('daily-goal').textContent = `$${status.daily_goal.toFixed(2)}`;
            document.getElementById('tasks-completed').textContent = status.tasks_completed;
            document.getElementById('active-strategies').textContent = status.active_strategies.length;
            
            // Обновление прогресса
            const progress = Math.min(status.progress_percentage, 100);
            document.getElementById('progress-fill').style.width = `${progress}%`;
            document.getElementById('progress-text').textContent = `${Math.round(progress)}% от дневной цели`;
            
            // Обновление времени работы
            const uptime = Math.floor((Date.now() - startTime) / 1000);
            const hours = Math.floor(uptime / 3600);
            const minutes = Math.floor((uptime % 3600) / 60);
            document.getElementById('uptime').textContent = `${hours}ч ${minutes}м`;
            
            // Обновление времени последнего обновления
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
            
            // Добавление записи в лог
            addLogEntry(`Статус обновлен: ${status.is_running ? 'Активен' : 'Остановлен'}`, 'success');
        }
        
        function addLogEntry(message, type = 'info') {
            const logContainer = document.getElementById('log-container');
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry ${type}`;
            logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            
            logContainer.appendChild(logEntry);
            logContainer.scrollTop = logContainer.scrollHeight;
            
            // Ограничиваем количество записей в логе
            const entries = logContainer.children;
            if (entries.length > 50) {
                logContainer.removeChild(entries[0]);
            }
        }
        
        // Загрузка стратегий
        async function loadStrategies() {
            try {
                const response = await fetch('/api/strategies');
                const strategies = await response.json();
                
                const strategiesList = document.getElementById('strategies-list');
                strategiesList.innerHTML = '';
                
                Object.entries(strategies).forEach(([name, data]) => {
                    const strategyItem = document.createElement('div');
                    strategyItem.className = 'strategy-item';
                    
                    const statusClass = data.is_active ? 'status-active' : 'status-inactive';
                    const statusText = data.is_active ? 'Активна' : 'Неактивна';
                    
                    strategyItem.innerHTML = `
                        <span class="strategy-name">${name}</span>
                        <span class="strategy-status ${statusClass}">${statusText}</span>
                    `;
                    
                    strategiesList.appendChild(strategyItem);
                });
                
            } catch (error) {
                console.error('Ошибка загрузки стратегий:', error);
            }
        }
        
        // Первоначальная загрузка данных
        loadStrategies();
        
        // Периодическое обновление стратегий
        setInterval(loadStrategies, 30000); // каждые 30 секунд
        
        // Обработка ошибок WebSocket
        ws.onerror = function(error) {
            addLogEntry('Ошибка соединения с сервером', 'error');
        };
        
        ws.onclose = function() {
            addLogEntry('Соединение с сервером закрыто', 'warning');
        };
        
        addLogEntry('Dashboard инициализирован', 'success');
    </script>
</body>
</html>
        """
    
    async def start(self, port: int = 8080):
        """Запуск веб-сервера дашборда"""
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    async def broadcast_update(self, data: Dict[str, Any]):
        """Отправка обновлений всем подключенным клиентам"""
        if self.active_connections:
            message = json.dumps({
                "type": "update",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
            
            # Удаляем неактивные соединения
            active_connections = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(message)
                    active_connections.append(connection)
                except:
                    pass  # Соединение закрыто
            
            self.active_connections = active_connections