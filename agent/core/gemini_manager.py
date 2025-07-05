"""
Умный менеджер Gemini API с ротацией ключей и экономией запросов
"""

import asyncio
import logging
import random
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


@dataclass
class APIKeyStats:
    """Статистика использования API ключа"""
    key: str
    requests_today: int = 0
    last_used: datetime = None
    errors_count: int = 0
    is_active: bool = True
    daily_limit: int = 1500  # Дневной лимит для Gemini free tier
    
    def __post_init__(self):
        if self.last_used is None:
            self.last_used = datetime.now()


class SmartContextAccumulator:
    """Умный накопитель контекста для минимизации запросов"""
    
    def __init__(self):
        self.context_buffer = []
        self.current_session = None
        self.last_request_time = None
        self.session_timeout = 300  # 5 минут
        
    def add_context(self, context_type: str, data: Any):
        """Добавить контекст в буфер"""
        self.context_buffer.append({
            "type": context_type,
            "data": data,
            "timestamp": datetime.now()
        })
        
        # Ограничиваем размер буфера
        if len(self.context_buffer) > 50:
            self.context_buffer = self.context_buffer[-30:]
    
    def should_make_request(self) -> bool:
        """Определить, нужно ли делать запрос сейчас"""
        if not self.last_request_time:
            return True
            
        # Если накопилось достаточно контекста или прошло много времени
        time_since_last = (datetime.now() - self.last_request_time).seconds
        
        return (len(self.context_buffer) >= 10 or 
                time_since_last > self.session_timeout or
                any(ctx["type"] == "critical" for ctx in self.context_buffer))
    
    def build_accumulated_prompt(self, new_query: str) -> str:
        """Собрать накопленный контекст в один промпт"""
        if not self.context_buffer:
            return new_query
            
        context_summary = []
        for ctx in self.context_buffer[-10:]:  # Последние 10 контекстов
            if ctx["type"] == "strategy_result":
                context_summary.append(f"Результат стратегии: {ctx['data']}")
            elif ctx["type"] == "market_data":
                context_summary.append(f"Рыночные данные: {ctx['data']}")
            elif ctx["type"] == "earnings":
                context_summary.append(f"Заработок: {ctx['data']}")
            elif ctx["type"] == "error":
                context_summary.append(f"Ошибка: {ctx['data']}")
        
        accumulated_context = "\n".join(context_summary)
        
        full_prompt = f"""
КОНТЕКСТ СЕССИИ:
{accumulated_context}

ТЕКУЩИЙ ЗАПРОС:
{new_query}

Проанализируй весь контекст и дай умное решение с учетом всей накопленной информации.
"""
        
        # Очищаем буфер после использования
        self.context_buffer = []
        self.last_request_time = datetime.now()
        
        return full_prompt


class GeminiManager:
    """Умный менеджер Gemini API с ротацией ключей"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Ваши API ключи
        self.api_keys = [
            "AIzaSyBPVRBwGusg6B4splT646TYd32hbGoozyA",
            "AIzaSyDor690Nm0efjObnHFWcS3sEv9Z3EFW_oU", 
            "AIzaSyBkJ5NN1XcC0iTf97e8m_urieGQhInyusc",
            "AIzaSyAAHwFeVoDBFgr5cAlJ9u2a5okOVsc4oXg",
            "AIzaSyA53tJdghSG6PnDv2lThkCV9x_cQhxecKM",
            "AIzaSyCaohwOPByd6-tBYThx0kysAXJyoDjk9u8",
            "AIzaSyDaYXMo9NwPcmBKGx6lN2mcJU5QW4JIVug",
            "AIzaSyArLkcZWgM5qQYzPOVfjH1BqjEIpA_4HEo",
            "AIzaSyD5PSsLmBtnmcpPUO4vq9Pg2a1rqJtHpks",
            "AIzaSyAG2IFVG4dUlZlExavQSM-A0vjzByVVcbA"
        ]
        
        # Статистика по ключам
        self.key_stats = {
            key: APIKeyStats(key=key) for key in self.api_keys
        }
        
        # Умный накопитель контекста
        self.context_accumulator = SmartContextAccumulator()
        
        # Текущий активный ключ
        self.current_key_index = 0
        
        # Настройки безопасности для Gemini
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        self.logger.info(f"🔑 Инициализирован Gemini Manager с {len(self.api_keys)} ключами")
    
    def get_next_available_key(self) -> Optional[str]:
        """Получить следующий доступный API ключ"""
        today = datetime.now().date()
        
        # Сбрасываем счетчики если новый день
        for stats in self.key_stats.values():
            if stats.last_used and stats.last_used.date() < today:
                stats.requests_today = 0
                stats.errors_count = 0
        
        # Ищем доступный ключ
        attempts = 0
        while attempts < len(self.api_keys):
            current_key = self.api_keys[self.current_key_index]
            stats = self.key_stats[current_key]
            
            # Проверяем доступность ключа
            if (stats.is_active and 
                stats.requests_today < stats.daily_limit and 
                stats.errors_count < 5):
                
                return current_key
            
            # Переходим к следующему ключу
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            attempts += 1
        
        self.logger.warning("⚠️ Все API ключи исчерпаны или заблокированы")
        return None
    
    def update_key_stats(self, api_key: str, success: bool, error: str = None):
        """Обновить статистику использования ключа"""
        if api_key in self.key_stats:
            stats = self.key_stats[api_key]
            stats.requests_today += 1
            stats.last_used = datetime.now()
            
            if not success:
                stats.errors_count += 1
                if stats.errors_count >= 5:
                    stats.is_active = False
                    self.logger.warning(f"🚫 Ключ {api_key[:20]}... деактивирован из-за ошибок")
    
    async def smart_request(self, prompt: str, context_type: str = "general", critical: bool = False) -> Optional[str]:
        """Умный запрос с накоплением контекста"""
        
        # Добавляем контекст
        if critical:
            context_type = "critical"
        
        self.context_accumulator.add_context(context_type, prompt)
        
        # Проверяем, нужно ли делать запрос сейчас
        if not critical and not self.context_accumulator.should_make_request():
            self.logger.info("📝 Контекст добавлен в буфер, запрос отложен")
            return None
        
        # Собираем накопленный промпт
        full_prompt = self.context_accumulator.build_accumulated_prompt(prompt)
        
        # Делаем запрос
        return await self._make_api_request(full_prompt)
    
    async def _make_api_request(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Выполнить API запрос с ретраями и ротацией ключей"""
        
        for attempt in range(max_retries):
            api_key = self.get_next_available_key()
            
            if not api_key:
                self.logger.error("❌ Нет доступных API ключей")
                return None
            
            try:
                # Настраиваем Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    'gemini-1.5-flash',  # Бесплатная модель
                    safety_settings=self.safety_settings
                )
                
                self.logger.info(f"🤖 Отправка запроса через ключ {api_key[:20]}...")
                
                # Отправляем запрос
                response = await asyncio.to_thread(
                    model.generate_content, 
                    prompt
                )
                
                if response.text:
                    self.update_key_stats(api_key, success=True)
                    self.logger.info(f"✅ Получен ответ ({len(response.text)} символов)")
                    
                    # Переходим к следующему ключу для равномерной нагрузки
                    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                    
                    return response.text
                else:
                    raise Exception("Пустой ответ от API")
                    
            except Exception as e:
                error_msg = str(e)
                self.logger.warning(f"⚠️ Ошибка API (попытка {attempt + 1}): {error_msg}")
                
                self.update_key_stats(api_key, success=False, error=error_msg)
                
                # Если превышен лимит, переходим к следующему ключу
                if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                
                # Пауза перед следующей попыткой
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Экспоненциальная задержка
        
        self.logger.error("❌ Все попытки API запроса исчерпаны")
        return None
    
    def get_api_stats(self) -> Dict[str, Any]:
        """Получить статистику использования API"""
        total_requests = sum(stats.requests_today for stats in self.key_stats.values())
        active_keys = sum(1 for stats in self.key_stats.values() if stats.is_active)
        
        return {
            "total_keys": len(self.api_keys),
            "active_keys": active_keys,
            "total_requests_today": total_requests,
            "context_buffer_size": len(self.context_accumulator.context_buffer),
            "current_key_index": self.current_key_index
        }
    
    async def analyze_earning_opportunity(self, market_data: Dict[str, Any], current_earnings: float) -> Optional[Dict[str, Any]]:
        """Проанализировать возможности заработка (критический запрос)"""
        
        prompt = f"""
Ты - эксперт по заработку денег онлайн. Проанализируй текущую ситуацию и предложи КОНКРЕТНЫЕ действия.

ТЕКУЩИЕ ДАННЫЕ:
- Заработано сегодня: ${current_earnings:.2f}
- Цель: $1.00 в день
- Осталось заработать: ${1.0 - current_earnings:.2f}

ДОСТУПНЫЕ СТРАТЕГИИ:
1. Фриланс (микро-задачи, переводы, data entry)
2. Контент-маркетинг (посты, комментарии)  
3. Опросы и тестирование
4. Реферальные программы
5. Микро-инвестиции

ДАЙ КОНКРЕТНЫЙ ПЛАН:
1. Какую стратегию использовать СЕЙЧАС?
2. Где именно искать задачи?
3. Сколько времени потратить?
4. Ожидаемый доход?

Ответ должен быть практическим и выполнимым СЕГОДНЯ.
"""
        
        response = await self.smart_request(prompt, "market_analysis", critical=True)
        
        if response:
            try:
                # Парсим ответ и возвращаем структурированные данные
                return {
                    "recommendation": response,
                    "confidence": 0.8,
                    "estimated_time": 60,  # минут
                    "estimated_earning": min(1.0 - current_earnings, 0.5)
                }
            except Exception as e:
                self.logger.error(f"Ошибка обработки ответа: {e}")
                return None
        
        return None
    
    async def optimize_strategy(self, strategy_results: List[Dict[str, Any]]) -> Optional[str]:
        """Оптимизировать стратегии на основе результатов"""
        
        # Добавляем результаты в контекст
        for result in strategy_results:
            self.context_accumulator.add_context("strategy_result", result)
        
        # Не делаем запрос сразу - накапливаем данные
        return await self.smart_request(
            "Проанализируй результаты стратегий и предложи улучшения",
            "strategy_optimization"
        )