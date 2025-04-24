# WSGI обертка для FastAPI приложения
import uvicorn
from app.main import app

# Для WSGI серверов
application = app

# Для непосредственного запуска этого файла
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
