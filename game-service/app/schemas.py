from pydantic import BaseModel
from datetime import date

class GameBase(BaseModel):
    name: str
    category: str
    release_date: date
    price: float

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True
