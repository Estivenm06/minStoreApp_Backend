from sqlalchemy import Boolean, Column, Integer, String
from src.models import Base, session

class Suppliers(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    nit = Column(String(20), nullable=True, unique=True)
    contact_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    active = Column(Boolean, nullable=False, default=1)

    def __init__(self, name, nit, contact_name, phone_number, email, address):
        self.name = name
        self.nit = nit
        self.contact_name = contact_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.active = 1

    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}', nit='{self.nit}', contact_name='{self.contact_name}', phone_number='{self.phone_number}', email='{self.email}', address='{self.address}', active={self.active})>"

    def get_paginated(page, per_page):
        offset = (page - 1) * per_page
        suppliers = session.query(Suppliers).offset(offset).limit(per_page).all()
        total_suppliers_count = session.query(Suppliers).count()
        return suppliers, total_suppliers_count

    def get_by_id(supplier_id):
        return session.query(Suppliers).filter_by(id=supplier_id).first()

    def get_by_name(name):
        return session.query(Suppliers).filter_by(name=name).first()

    def save(self):
        session.add(self)
        session.commit()

    def update(self, name=None, nit=None, contact_name=None, phone_number=None, email=None, address=None, active=1):
        self.name = name if name is not None else self.name
        self.nit = nit if nit is not None else self.nit
        self.contact_name = contact_name if contact_name is not None else self.contact_name
        self.phone_number = phone_number if phone_number is not None else self.phone_number
        self.email = email if email is not None else self.email
        self.address = address if address is not None else self.address
        self.active = active if active is not None else self.active
        session.commit()