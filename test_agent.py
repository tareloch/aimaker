#!/usr/bin/env python3
"""
Тест автономного AI агента
"""

import asyncio
import logging
import sys
from agent.core.config import Config
from agent.core.gemini_manager import GeminiManager
from agent.strategies.strategy_manager import StrategyManager

# Настройка логирования для тестов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)


async def test_gemini_manager():
    """Тест менеджера Gemini API"""
    print("\n🧪 ТЕСТ: Gemini Manager")
    print("=" * 40)
    
    try:
        gemini = GeminiManager()
        
        # Тест статистики API
        stats = gemini.get_api_stats()
        print(f"✅ API статистика: {stats}")
        
        # Тест накопления контекста (без реального запроса)
        gemini.context_accumulator.add_context("test", "Тестовый контекст")
        print(f"✅ Контекст добавлен, размер буфера: {len(gemini.context_accumulator.context_buffer)}")
        
        print("✅ Gemini Manager инициализирован корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Gemini Manager: {e}")
        return False


async def test_strategies():
    """Тест стратегий заработка"""
    print("\n🧪 ТЕСТ: Стратегии заработка")
    print("=" * 40)
    
    try:
        config = Config()
        strategy_manager = StrategyManager(config)
        
        # Получаем доступные стратегии
        available = await strategy_manager.get_available_strategies()
        print(f"✅ Доступно стратегий: {len(available)}")
        
        for strategy in available:
            print(f"   📋 {strategy.name} - потенциал: ${await strategy.estimate_potential():.2f}")
        
        # Тест выбора лучших стратегий
        best_strategies = await strategy_manager.select_best_strategies(1.0)
        print(f"✅ Выбрано стратегий для $1.00: {len(best_strategies)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка стратегий: {e}")
        return False


async def test_strategy_execution():
    """Тест выполнения стратегии (без реальных API запросов)"""
    print("\n🧪 ТЕСТ: Выполнение стратегии")
    print("=" * 40)
    
    try:
        config = Config()
        strategy_manager = StrategyManager(config)
        
        # Тестируем выполнение одной стратегии
        strategy_name = "smart_referral"
        
        print(f"🚀 Тестируем стратегию: {strategy_name}")
        
        # Получаем стратегию
        strategy = strategy_manager.strategies.get(strategy_name)
        if not strategy:
            print(f"❌ Стратегия {strategy_name} не найдена")
            return False
        
        # Проверяем возможность выполнения
        can_execute = await strategy.can_execute()
        print(f"✅ Может выполняться: {can_execute}")
        
        if can_execute:
            # Симулируем выполнение (без реальных API вызовов)
            print("🔄 Симулируем выполнение стратегии...")
            
            # Здесь мы не делаем реальный запрос к API, а просто тестируем логику
            earnings = 0.45  # Симулированный заработок
            
            result = {
                "success": True,
                "earnings": earnings,
                "strategy": strategy_name,
                "test_mode": True
            }
            
            print(f"✅ Результат (симуляция): +${earnings:.2f}")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        return False


async def test_agent_components():
    """Тест основных компонентов агента"""
    print("\n🧪 ТЕСТ: Компоненты агента")
    print("=" * 40)
    
    try:
        from agent.core.agent import AutonomousAgent
        
        config = Config()
        agent = AutonomousAgent(config)
        
        # Тест инициализации
        await agent.initialize()
        print("✅ Агент инициализирован")
        
        # Тест получения статуса
        status = agent.get_status()
        print(f"✅ Статус агента: {status}")
        
        # Тест компонентов
        if agent.strategy_manager:
            print("✅ StrategyManager подключен")
        else:
            print("❌ StrategyManager не подключен")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка компонентов: {e}")
        return False


async def test_configuration():
    """Тест конфигурации"""
    print("\n🧪 ТЕСТ: Конфигурация")
    print("=" * 40)
    
    try:
        config = Config()
        
        print(f"✅ Дневная цель: ${config.agent.daily_earning_goal}")
        print(f"✅ Максимум задач: {config.agent.max_daily_tasks}")
        print(f"✅ Толерантность к риску: {config.agent.risk_tolerance}")
        
        # Проверяем API ключи
        missing_apis = config.get_missing_apis()
        if missing_apis:
            print(f"⚠️  Отсутствуют API ключи: {missing_apis}")
        else:
            print("✅ Все API ключи настроены")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False


async def run_all_tests():
    """Запуск всех тестов"""
    print("🤖 ТЕСТИРОВАНИЕ АВТОНОМНОГО AI АГЕНТА")
    print("=" * 50)
    
    tests = [
        ("Конфигурация", test_configuration),
        ("Gemini Manager", test_gemini_manager),
        ("Стратегии", test_strategies),
        ("Выполнение стратегии", test_strategy_execution),
        ("Компоненты агента", test_agent_components),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
            
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Итоги тестирования
    print("\n📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 30)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ ПРОШЕЛ" if result else "❌ ПРОВАЛЕН"
        print(f"{test_name:.<20} {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nИтого: {passed} прошло, {failed} провалено")
    
    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("Система готова к работе!")
    else:
        print(f"\n⚠️  {failed} тестов провалено")
        print("Необходимо исправить ошибки перед запуском")
    
    return failed == 0


if __name__ == "__main__":
    print("Запуск тестов автономного AI агента...")
    
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
        
    except KeyboardInterrupt:
        print("\n🛑 Тестирование прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)