"""
Система конфигурации автономного агента
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class APIConfig(BaseModel):
    """Конфигурация API ключей"""
    openai_api_key: Optional[str] = None
    upwork_client_id: Optional[str] = None
    upwork_client_secret: Optional[str] = None
    fiverr_api_key: Optional[str] = None
    binance_api_key: Optional[str] = None
    binance_secret_key: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None


class AgentConfig(BaseModel):
    """Основная конфигурация агента"""
    daily_earning_goal: float = Field(default=1.0, description="Цель дневного заработка в долларах")
    max_daily_tasks: int = Field(default=10, description="Максимум задач в день")
    learning_rate: float = Field(default=0.1, description="Скорость обучения")
    risk_tolerance: float = Field(default=0.3, description="Толерантность к риску (0-1)")
    work_hours_start: int = Field(default=9, description="Начало рабочего дня")
    work_hours_end: int = Field(default=18, description="Конец рабочего дня")
    min_task_profit: float = Field(default=0.1, description="Минимальная прибыль с задачи")


class DatabaseConfig(BaseModel):
    """Конфигурация базы данных"""
    database_url: str = Field(default="sqlite:///agent_data.db")
    redis_url: str = Field(default="redis://localhost:6379")


class MonitoringConfig(BaseModel):
    """Конфигурация мониторинга"""
    dashboard_port: int = Field(default=8080)
    log_level: str = Field(default="INFO")
    metrics_retention_days: int = Field(default=30)


class Config:
    """Главный класс конфигурации"""
    
    def __init__(self):
        self.api = APIConfig(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            upwork_client_id=os.getenv("UPWORK_CLIENT_ID"),
            upwork_client_secret=os.getenv("UPWORK_CLIENT_SECRET"),
            fiverr_api_key=os.getenv("FIVERR_API_KEY"),
            binance_api_key=os.getenv("BINANCE_API_KEY"),
            binance_secret_key=os.getenv("BINANCE_SECRET_KEY"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            twitter_api_key=os.getenv("TWITTER_API_KEY"),
            twitter_api_secret=os.getenv("TWITTER_API_SECRET"),
        )
        
        self.agent = AgentConfig()
        self.database = DatabaseConfig()
        self.monitoring = MonitoringConfig()
        
        # Создаем папки если их нет
        self._create_directories()
    
    def _create_directories(self):
        """Создание необходимых директорий"""
        dirs = [
            "logs",
            "data",
            "models",
            "reports"
        ]
        
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)
    
    def get_missing_apis(self) -> list[str]:
        """Возвращает список недостающих API ключей"""
        missing = []
        
        if not self.api.openai_api_key:
            missing.append("OpenAI API Key")
        
        # Добавляем другие критичные API
        return missing
    
    def validate_configuration(self) -> bool:
        """Проверка корректности конфигурации"""
        missing_apis = self.get_missing_apis()
        
        if missing_apis:
            print(f"⚠️  Отсутствуют API ключи: {', '.join(missing_apis)}")
            return False
            
        return True