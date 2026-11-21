from sqlalchemy import Column, Float, ForeignKey, Integer, func

from src.models import Base, session


class DetailedInvoices(Base):
    __tablename__ = 'detailed_invoices'

    id = Column(Integer, primary_key=True)
    id_invoice = Column(ForeignKey('invoices.id'), nullable=False)
    id_product = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float(10, 2), nullable=False)
    subtotal = Column(Float(12, 2), nullable=False)

    def __init__(self, id_invoice, id_product, quantity, unit_price, subtotal):
        self.id_invoice = id_invoice
        self.id_product = id_product
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal

    def __repr__(self):
        return f"<DetailedInvoices(id={self.id}, id_invoice={self.id_invoice}, id_product={self.id_product}, quantity={self.quantity}, unit_price={self.unit_price}, subtotal={self.subtotal})>"

    def get_all():
        return session.query(DetailedInvoices).all()

    def get_paginted(page, per_page):
        invoices = session.query(DetailedInvoices).offset((page - 1) * per_page).limit(per_page).all()
        total_invoices_count = session.query(func.count(DetailedInvoices.id)).scalar()
        return invoices, total_invoices_count

    def get_by_id(detailed_invoice_id):
        return session.query(DetailedInvoices).filter_by(id=detailed_invoice_id).first()

    def get_by_invoice_id(invoice_id):
        return session.query(DetailedInvoices).filter_by(id_invoice=invoice_id).all()

    def get_by_invoice_and_product(invoice_id, product_id):
        return session.query(DetailedInvoices).filter_by(id_invoice=invoice_id, id_product=product_id).first()

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()