"""
Основной класс автономного AI агента
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass

from agent.core.config import Config
from agent.strategies.strategy_manager import StrategyManager


@dataclass
class AgentState:
    """Состояние агента"""
    is_running: bool = False
    daily_earnings: float = 0.0
    total_earnings: float = 0.0
    tasks_completed: int = 0
    active_strategies: List[str] = None
    last_learning_update: datetime = None
    
    def __post_init__(self):
        if self.active_strategies is None:
            self.active_strategies = []
        if self.last_learning_update is None:
            self.last_learning_update = datetime.now()


class AutonomousAgent:
    """
    Автономный AI агент для заработка денег
    
    Ключевые возможности:
    - Автономное планирование и выполнение задач
    - Обучение на результатах
    - Адаптация стратегий
    - Мониторинг прогресса
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.state = AgentState()
        
        # Основные компоненты
        self.strategy_manager = None
        
        self.logger.info("🤖 Автономный агент создан")
    
    async def initialize(self):
        """Инициализация всех компонентов агента"""
        try:
            self.logger.info("🔧 Инициализация компонентов агента...")
            
            # Проверка конфигурации
            if not self.config.validate_configuration():
                self.logger.warning("⚠️ Не все API ключи настроены, но агент может работать в ограниченном режиме")
            
            # Инициализация менеджера стратегий
            self.strategy_manager = StrategyManager(self.config)
            
            self.logger.info("✅ Все компоненты инициализированы")
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка инициализации: {e}")
            raise
    
    async def run(self):
        """Основной цикл работы агента"""
        self.state.is_running = True
        self.logger.info("🚀 Запуск основного цикла агента")
        
        try:
            while self.state.is_running:
                await self._daily_cycle()
                
                # Проверяем, достигли ли дневной цели
                if self.state.daily_earnings >= self.config.agent.daily_earning_goal:
                    self.logger.info(f"🎉 Дневная цель достигнута: ${self.state.daily_earnings:.2f}")
                    await self._end_of_day_routine()
                    
                # Небольшая пауза между циклами
                await asyncio.sleep(60)  # 1 минута
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Получен сигнал остановки")
        except Exception as e:
            self.logger.error(f"❌ Ошибка в основном цикле: {e}")
        finally:
            await self.shutdown()
    
    async def _daily_cycle(self):
        """Дневной цикл работы агента"""
        try:
            self.logger.info("📅 Начало дневного цикла")
            
            # Получаем доступные стратегии
            available_strategies = await self.strategy_manager.get_available_strategies()
            
            if not available_strategies:
                self.logger.warning("⚠️ Нет доступных стратегий для заработка")
                await asyncio.sleep(300)  # 5 минут
                return
            
            # Выбираем лучшие стратегии для достижения цели
            remaining_target = self.config.agent.daily_earning_goal - self.state.daily_earnings
            selected_strategies = await self.strategy_manager.select_best_strategies(remaining_target)
            
            self.logger.info(f"🎯 Выбрано {len(selected_strategies)} стратегий для заработка ${remaining_target:.2f}")
            
            # Выполняем стратегии
            for strategy in selected_strategies:
                if not self.state.is_running:
                    break
                
                self.logger.info(f"🚀 Выполняем стратегию: {strategy.name}")
                result = await strategy.execute()
                
                # Обрабатываем результат
                if result.get("success", False):
                    earnings = result.get("earnings", 0.0)
                    self.state.daily_earnings += earnings
                    self.state.total_earnings += earnings
                    self.state.tasks_completed += 1
                    
                    # Обновляем список активных стратегий
                    if strategy.name not in self.state.active_strategies:
                        self.state.active_strategies.append(strategy.name)
                    
                    self.logger.info(
                        f"✅ Стратегия {strategy.name}: +${earnings:.2f} "
                        f"(всего сегодня: ${self.state.daily_earnings:.2f})"
                    )
                else:
                    error = result.get("error", "Неизвестная ошибка")
                    self.logger.warning(f"⚠️ Стратегия {strategy.name} не выполнена: {error}")
                
                # Пауза между стратегиями
                await asyncio.sleep(30)
            
            # Общая пауза в конце цикла
            await asyncio.sleep(300)  # 5 минут
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка в дневном цикле: {e}")
    

    
    async def _end_of_day_routine(self):
        """Процедуры конца дня"""
        try:
            # Логирование итогов дня
            self.logger.info(f"📊 Итоги дня: заработано ${self.state.daily_earnings:.2f}, выполнено {self.state.tasks_completed} задач")
            
            # Сброс дневной статистики
            self.state.daily_earnings = 0.0
            self.state.tasks_completed = 0
            self.state.active_strategies = []
            
            self.logger.info("✅ Дневной цикл завершен, статистика сброшена")
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка в процедурах конца дня: {e}")
    
    async def shutdown(self):
        """Корректное завершение работы агента"""
        self.logger.info("🔄 Завершение работы агента...")
        
        self.state.is_running = False
        
        # Логирование финальной статистики
        self.logger.info(f"💰 Общий заработок за время работы: ${self.state.total_earnings:.2f}")
        
        self.logger.info("✅ Агент успешно завершил работу")
    
    def get_status(self) -> Dict[str, Any]:
        """Получение текущего статуса агента"""
        return {
            "is_running": self.state.is_running,
            "daily_earnings": self.state.daily_earnings,
            "total_earnings": self.state.total_earnings,
            "tasks_completed": self.state.tasks_completed,
            "active_strategies": self.state.active_strategies,
            "daily_goal": self.config.agent.daily_earning_goal,
            "progress_percentage": (self.state.daily_earnings / self.config.agent.daily_earning_goal) * 100
        }