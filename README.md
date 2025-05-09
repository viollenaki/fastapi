# Простой проект FastAPI

Это простой пример проекта с использованием FastAPI.

## Установка

1. Активируйте виртуальное окружение:
```powershell
# В PowerShell (если были проблемы с политиками выполнения)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# ИЛИ для cmd
.\venv\Scripts\activate.bat
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

Чтобы запустить приложение:
```bash
uvicorn app.main:app --reload
```

После этого API будет доступно по адресу http://127.0.0.1:8000

## Документация API

Автоматическая документация доступна по адресам:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
#   f a s t a p i  
 