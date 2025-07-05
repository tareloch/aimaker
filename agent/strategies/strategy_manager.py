"""
Менеджер стратегий заработка
"""

import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from agent.core.config import Config


class EarningStrategy(ABC):
    """Базовый класс для стратегий заработка"""
    
    def __init__(self, name: str, config: Config):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"strategy.{name}")
        self.is_active = False
        self.daily_earnings = 0.0
        self.success_rate = 0.0
        
    @abstractmethod
    async def can_execute(self) -> bool:
        """Проверка возможности выполнения стратегии"""
        pass
    
    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Выполнение стратегии"""
        pass
    
    @abstractmethod
    async def estimate_potential(self) -> float:
        """Оценка потенциального заработка"""
        pass


class FreelanceStrategy(EarningStrategy):
    """Стратегия заработка на фрилансе"""
    
    def __init__(self, config: Config):
        super().__init__("freelance", config)
        
    async def can_execute(self) -> bool:
        """Проверяем наличие API ключей для фриланс платформ"""
        return (self.config.api.upwork_client_id is not None or 
                self.config.api.fiverr_api_key is not None)
    
    async def execute(self) -> Dict[str, Any]:
        """Поиск и выполнение фриланс задач"""
        try:
            self.logger.info("🔍 Поиск фриланс заданий...")
            
            # Пока что заглушка - в будущем интеграция с реальными API
            earnings = 0.0
            
            # Симуляция поиска простых задач
            potential_tasks = [
                {"title": "Data entry", "budget": 0.5, "difficulty": "easy"},
                {"title": "Text translation", "budget": 1.2, "difficulty": "medium"},
                {"title": "Content writing", "budget": 2.0, "difficulty": "medium"},
            ]
            
            # В реальности здесь будет интеграция с API фриланс платформ
            self.logger.info(f"Найдено {len(potential_tasks)} потенциальных задач")
            
            return {
                "success": True,
                "earnings": earnings,
                "tasks_found": len(potential_tasks),
                "strategy": self.name
            }
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка выполнения фриланс стратегии: {e}")
            return {
                "success": False,
                "earnings": 0.0,
                "error": str(e),
                "strategy": self.name
            }
    
    async def estimate_potential(self) -> float:
        """Оценка потенциального заработка от фриланса"""
        if not await self.can_execute():
            return 0.0
        
        # Базовая оценка: $0.5-2.0 в зависимости от времени и навыков
        return 1.5


class CryptoTradingStrategy(EarningStrategy):
    """Стратегия заработка на криптотрейдинге"""
    
    def __init__(self, config: Config):
        super().__init__("crypto_trading", config)
        
    async def can_execute(self) -> bool:
        """Проверяем наличие API ключей для криптобирж"""
        return self.config.api.binance_api_key is not None
    
    async def execute(self) -> Dict[str, Any]:
        """Выполнение торговых операций"""
        try:
            self.logger.info("📈 Анализ крипторынка...")
            
            # Пока что заглушка - в будущем реальный трейдинг
            earnings = 0.0
            
            # Симуляция анализа рынка
            market_condition = "stable"  # bullish, bearish, stable
            
            self.logger.info(f"Состояние рынка: {market_condition}")
            
            return {
                "success": True,
                "earnings": earnings,
                "market_condition": market_condition,
                "strategy": self.name
            }
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка криптотрейдинг стратегии: {e}")
            return {
                "success": False,
                "earnings": 0.0,
                "error": str(e),
                "strategy": self.name
            }
    
    async def estimate_potential(self) -> float:
        """Оценка потенциального заработка от трейдинга"""
        if not await self.can_execute():
            return 0.0
        
        # Высокий потенциал, но высокий риск
        risk_factor = self.config.agent.risk_tolerance
        return 3.0 * risk_factor


class ContentCreationStrategy(EarningStrategy):
    """Стратегия заработка на создании контента"""
    
    def __init__(self, config: Config):
        super().__init__("content_creation", config)
        
    async def can_execute(self) -> bool:
        """Проверяем наличие OpenAI API для генерации контента"""
        return self.config.api.openai_api_key is not None
    
    async def execute(self) -> Dict[str, Any]:
        """Создание и продажа контента"""
        try:
            self.logger.info("✍️ Создание контента...")
            
            earnings = 0.0
            
            # Пока что заглушка - в будущем реальная генерация контента
            content_types = ["blog_posts", "social_media", "product_descriptions"]
            
            self.logger.info(f"Типы контента: {content_types}")
            
            return {
                "success": True,
                "earnings": earnings,
                "content_created": len(content_types),
                "strategy": self.name
            }
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка стратегии создания контента: {e}")
            return {
                "success": False,
                "earnings": 0.0,
                "error": str(e),
                "strategy": self.name
            }
    
    async def estimate_potential(self) -> float:
        """Оценка потенциального заработка от создания контента"""
        if not await self.can_execute():
            return 0.0
        
        return 1.0


class SurveyStrategy(EarningStrategy):
    """Стратегия заработка на опросах и микрозаданиях"""
    
    def __init__(self, config: Config):
        super().__init__("surveys", config)
        
    async def can_execute(self) -> bool:
        """Опросы доступны всегда"""
        return True
    
    async def execute(self) -> Dict[str, Any]:
        """Выполнение опросов"""
        try:
            self.logger.info("📝 Поиск доступных опросов...")
            
            earnings = 0.0
            
            # Симуляция поиска опросов
            available_surveys = 3
            
            self.logger.info(f"Найдено {available_surveys} опросов")
            
            return {
                "success": True,
                "earnings": earnings,
                "surveys_completed": available_surveys,
                "strategy": self.name
            }
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка стратегии опросов: {e}")
            return {
                "success": False,
                "earnings": 0.0,
                "error": str(e),
                "strategy": self.name
            }
    
    async def estimate_potential(self) -> float:
        """Оценка потенциального заработка от опросов"""
        return 0.3  # Низкий, но стабильный доход


class StrategyManager:
    """Менеджер всех стратегий заработка"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Инициализация всех стратегий
        self.strategies = {
            "freelance": FreelanceStrategy(config),
            "crypto_trading": CryptoTradingStrategy(config),
            "content_creation": ContentCreationStrategy(config),
            "surveys": SurveyStrategy(config),
        }
        
        self.logger.info(f"🎯 Инициализировано {len(self.strategies)} стратегий")
    
    async def get_available_strategies(self) -> List[EarningStrategy]:
        """Получить список доступных стратегий"""
        available = []
        
        for strategy in self.strategies.values():
            if await strategy.can_execute():
                available.append(strategy)
        
        self.logger.info(f"📋 Доступно стратегий: {len(available)}")
        return available
    
    async def select_best_strategies(self, target_amount: float) -> List[EarningStrategy]:
        """Выбрать лучшие стратегии для достижения целевой суммы"""
        available = await self.get_available_strategies()
        
        # Сортируем по потенциальному доходу
        strategy_potentials = []
        for strategy in available:
            potential = await strategy.estimate_potential()
            strategy_potentials.append((strategy, potential))
        
        # Сортируем по убыванию потенциала
        strategy_potentials.sort(key=lambda x: x[1], reverse=True)
        
        selected = []
        total_potential = 0.0
        
        for strategy, potential in strategy_potentials:
            if total_potential < target_amount:
                selected.append(strategy)
                total_potential += potential
        
        self.logger.info(f"🎯 Выбрано {len(selected)} стратегий для достижения ${target_amount}")
        return selected
    
    async def execute_strategy(self, strategy_name: str) -> Dict[str, Any]:
        """Выполнить конкретную стратегию"""
        if strategy_name not in self.strategies:
            raise ValueError(f"Неизвестная стратегия: {strategy_name}")
        
        strategy = self.strategies[strategy_name]
        
        if not await strategy.can_execute():
            return {
                "success": False,
                "error": "Стратегия недоступна",
                "strategy": strategy_name
            }
        
        return await strategy.execute()
    
    def get_strategy_stats(self) -> Dict[str, Any]:
        """Получить статистику по всем стратегиям"""
        stats = {}
        
        for name, strategy in self.strategies.items():
            stats[name] = {
                "is_active": strategy.is_active,
                "daily_earnings": strategy.daily_earnings,
                "success_rate": strategy.success_rate
            }
        
        return stats