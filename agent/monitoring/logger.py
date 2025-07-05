"""
Система логирования для автономного агента
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(log_level: str = "INFO", log_dir: str = "logs"):
    """Настройка системы логирования"""
    
    # Создаем директорию для логов
    Path(log_dir).mkdir(exist_ok=True)
    
    # Настройка форматирования
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очищаем существующие обработчики
    root_logger.handlers.clear()
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Файловый обработчик для общих логов
    general_log_file = Path(log_dir) / f"agent_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        general_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Отдельный файл для ошибок
    error_log_file = Path(log_dir) / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Отдельный файл для заработка
    earnings_log_file = Path(log_dir) / f"earnings_{datetime.now().strftime('%Y%m%d')}.log"
    earnings_handler = RotatingFileHandler(
        earnings_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10
    )
    earnings_handler.setLevel(logging.INFO)
    
    # Специальный форматтер для логов заработка
    earnings_formatter = logging.Formatter(
        '%(asctime)s | EARNINGS | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    earnings_handler.setFormatter(earnings_formatter)
    
    # Создаем отдельный логгер для заработка
    earnings_logger = logging.getLogger("earnings")
    earnings_logger.addHandler(earnings_handler)
    earnings_logger.setLevel(logging.INFO)
    earnings_logger.propagate = False  # Не передавать в корневой логгер
    
    logging.info("📝 Система логирования настроена")


class EarningsLogger:
    """Специальный логгер для отслеживания заработка"""
    
    def __init__(self):
        self.logger = logging.getLogger("earnings")
    
    def log_earning(self, strategy: str, amount: float, source: str = "", details: str = ""):
        """Логирование заработка"""
        message = f"Strategy: {strategy} | Amount: ${amount:.2f}"
        
        if source:
            message += f" | Source: {source}"
        
        if details:
            message += f" | Details: {details}"
        
        self.logger.info(message)
    
    def log_loss(self, strategy: str, amount: float, reason: str = ""):
        """Логирование потерь"""
        message = f"LOSS - Strategy: {strategy} | Amount: ${amount:.2f}"
        
        if reason:
            message += f" | Reason: {reason}"
        
        self.logger.warning(message)
    
    def log_goal_achieved(self, daily_amount: float, total_amount: float):
        """Логирование достижения цели"""
        message = f"GOAL ACHIEVED! Daily: ${daily_amount:.2f} | Total: ${total_amount:.2f}"
        self.logger.info(message)