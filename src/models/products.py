from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, func

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
    active = Column(Boolean, nullable=False, default=1) # 1 for active, 0 for inactive

    def __init__(self, name, barcode, description, price_sell, price_buy, id_category, id_supplier, stock=0):
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

    def get_paginated(page, per_page):
        products = session.query(Products).offset((page - 1) * per_page).limit(per_page).all()
        total_products_count = session.query(func.count(Products.id)).scalar()
        return products, total_products_count

    def get_by_id(product_id):
        return session.query(Products).filter_by(id=product_id).first()

    def get_by_name(product_name):
        return session.query(Products).filter_by(name=product_name).first()

    def create_product(self):
        session.add(self)
        session.commit()

    def update_product(self):
        session.commit()
