from sqlalchemy import Column, Integer, String
from src.models import Base

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', description='{self.description}', price={self.price})>"