# WSGI обертка для FastAPI приложения
import uvicorn
from asgi2wsgi import Asgi2Wsgi
from app.main import app

# Адаптируем FastAPI (ASGI) под WSGI
application = Asgi2Wsgi(app)

# Для непосредственного запуска этого файла
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
