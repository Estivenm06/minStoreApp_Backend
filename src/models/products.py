from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey
from src.models import Base, session

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    barcode = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price_sell = Column(Integer, nullable=False)
    price_buy = Column(Integer, nullable=False)
    stock = Column(Float, nullable=False)
    id_category = Column(ForeignKey('categories.id'), nullable=False)
    id_supplier = Column(ForeignKey('suppliers.id'), nullable=False)
    active = Column(Boolean, nullable=False, default=1)

    def __init__(self, name, barcode, description, price_sell, price_buy, stock, id_category, id_supplier):
        self.name = name
        self.barcode = barcode
        self.description = description
        self.price_sell = price_sell
        self.price_buy = price_buy
        self.stock = stock
        self.id_category = id_category
        self.id_supplier = id_supplier
        self.active = 1

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', barcode='{self.barcode}', description='{self.description}', price_sell={self.price_sell}, price_buy={self.price_buy}, stock={self.stock}, id_category={self.id_category}, id_supplier={self.id_supplier}), active={self.active}>"

    def get_all():
        return session.query(Products).all()

    def create_product(self):
        session.add(self)
        session.commit()
