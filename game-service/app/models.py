from sqlalchemy import Column, Integer, String, Date, Numeric
from .database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    release_date = Column(Date)
    price = Column(Numeric(10, 2))
