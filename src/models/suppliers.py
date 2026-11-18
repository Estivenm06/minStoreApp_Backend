from sqlalchemy import Boolean, Column, Integer, String
from src.models import Base

class Suppliers(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    nit = Column(String(20), nullable=True)
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