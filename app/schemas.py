from typing import Optional
from pydantic import BaseModel
from pydantic.config import ConfigDict  # Правильный импорт ConfigDict


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    
    # Современный способ конфигурации для Pydantic v2
    model_config = ConfigDict(from_attributes=True)
