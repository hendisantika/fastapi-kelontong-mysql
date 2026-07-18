from sqlalchemy import Column, String, Integer

from database import Base


class Merchandise(Base):
    __tablename__ = "merchandise"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    category_id = Column(Integer)
    price = Column(Integer)
    stock = Column(Integer)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(255))
