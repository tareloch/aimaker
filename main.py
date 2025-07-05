#!/usr/bin/env python3
"""
Автономный AI Агент для Заработка
Главный файл запуска системы
"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

from agent.core.agent import AutonomousAgent
from agent.core.config import Config
from agent.monitoring.logger import setup_logging
from agent.monitoring.dashboard import Dashboard


async def main():
    """Главная функция запуска агента"""
    
    # Настройка логирования
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Запуск автономного AI агента...")
        
        # Загрузка конфигурации
        config = Config()
        
        # Создание экземпляра агента
        agent = AutonomousAgent(config)
        
        # Инициализация компонентов
        await agent.initialize()
        
        # Запуск мониторинга и dashboard
        dashboard = Dashboard(agent)
        asyncio.create_task(dashboard.start())
        
        logger.info("✅ Агент успешно инициализирован")
        logger.info(f"🎯 Цель: заработать $1 в день")
        logger.info(f"📊 Dashboard доступен на http://localhost:8080")
        
        # Основной цикл работы агента
        await agent.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал завершения")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
    finally:
        logger.info("🔄 Завершение работы агента...")


if __name__ == "__main__":
    # Проверка Python версии
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8+")
        sys.exit(1)
    
    # Запуск агента
    asyncio.run(main())