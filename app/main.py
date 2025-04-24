from fastapi import FastAPI, HTTPException, Path, Query
from typing import List, Optional
from . import schemas

app = FastAPI(
    title="Простое API на FastAPI",
    description="Демонстрационный проект FastAPI",
    version="0.1.0"
)

# Имитация базы данных
items_db = [
    {"id": 1, "title": "Товар 1", "description": "Описание первого товара"},
    {"id": 2, "title": "Товар 2", "description": "Описание второго товара"}
]


@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работоспособности API."""
    return {"message": "Привет! Это простой проект FastAPI"}


@app.get("/items/", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100):
    """Получить список всех товаров с возможностью пагинации."""
    return [{"id": item["id"], "title": item["title"], "description": item["description"]} 
            for item in items_db[skip: skip + limit]]


@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int = Path(..., title="ID товара", ge=1)):
    """Получить товар по его ID."""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate):
    """Создать новый товар."""
    new_item_id = max([item["id"] for item in items_db]) + 1 if items_db else 1
    new_item = {"id": new_item_id, **item.model_dump()}  # Используем model_dump() для Pydantic v2
    items_db.append(new_item)
    return new_item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int = Path(..., title="ID товара для удаления", ge=1)):
    """Удалить товар по его ID."""
    for idx, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(idx)
            return {"message": f"Товар с ID {item_id} успешно удален"}
    raise HTTPException(status_code=404, detail="Товар не найден")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
