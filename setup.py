#!/usr/bin/env python3
"""
Скрипт установки и настройки автономного AI агента
"""

import os
import sys
import shutil
from pathlib import Path


def create_env_file():
    """Создание файла .env из примера"""
    print("🔧 Создание файла конфигурации...")
    
    if Path(".env").exists():
        print("⚠️  Файл .env уже существует, пропускаем создание")
        return
    
    if Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
        print("✅ Файл .env создан из .env.example")
        print("📝 Отредактируйте .env файл и добавьте ваши API ключи")
    else:
        print("❌ Файл .env.example не найден")


def create_directories():
    """Создание необходимых директорий"""
    print("📁 Создание директорий...")
    
    dirs = [
        "logs",
        "data", 
        "models",
        "reports",
        "config"
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Создана директория: {dir_name}")


def install_dependencies():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Зависимости успешно установлены")
        else:
            print(f"❌ Ошибка установки зависимостей: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка установки: {e}")
        return False
    
    return True


def check_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка версии Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или новее")
        print(f"   Текущая версия: {sys.version}")
        return False
    
    print(f"✅ Python версия OK: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def display_next_steps():
    """Отображение следующих шагов"""
    print("\n" + "="*60)
    print("🎉 УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*60)
    print()
    print("📋 СЛЕДУЮЩИЕ ШАГИ:")
    print()
    print("1. 🔑 Настройте API ключи в файле .env:")
    print("   - OpenAI API Key (обязательно)")
    print("   - Upwork/Fiverr API (для фриланса)")  
    print("   - Binance API (для трейдинга)")
    print("   - Другие по желанию")
    print()
    print("2. 🚀 Запустите агента:")
    print("   python main.py")
    print()
    print("3. 📊 Откройте dashboard в браузере:")
    print("   http://localhost:8080")
    print()
    print("4. 💡 Агент начнет искать способы заработка автоматически!")
    print()
    print("⚠️  ВАЖНО: Убедитесь, что настроили хотя бы OpenAI API ключ")
    print("   для базовой функциональности.")
    print()
    print("📞 Если нужна помощь с настройкой API, скажите мне!")
    print("="*60)


def main():
    """Главная функция установки"""
    print("🤖 АВТОНОМНЫЙ AI АГЕНТ - УСТАНОВКА")
    print("="*40)
    print()
    
    # Проверка версии Python
    if not check_python_version():
        sys.exit(1)
    
    # Создание директорий
    create_directories()
    
    # Создание .env файла
    create_env_file()
    
    # Установка зависимостей
    if not install_dependencies():
        print("❌ Установка прервана из-за ошибок")
        sys.exit(1)
    
    # Следующие шаги
    display_next_steps()


if __name__ == "__main__":
    main()