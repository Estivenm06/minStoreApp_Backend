import enum

from sqlalchemy import Column, Date, Integer, String, func

from src.models import Base, session


class Role(str, enum.Enum):
    CLIENT = 'client'


class Clients(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    document = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(200), nullable=True)
    date_created = Column(Date, nullable=False, default=func.current_date())
    active = Column(Integer, nullable=False, default=1)  # 1 for active, 0 for inactive
    role = Column(String(20), nullable=False)

    def __init__(self, document, name, last_name, phone_number=None, email=None, address=None, active=1, role=Role.CLIENT.value):
        self.document = document
        self.name = name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.active = active
        self.role = role

    def __repr__(self):
        return f"<Client(id={self.id}, document='{self.document}', name='{self.name}', last_name='{self.last_name}', phone_number='{self.phone_number}', email='{self.email}', address='{self.address}', date_created={self.date_created}, active={self.active}, role='{self.role}')>"

    def get_all():
        return session.query(Clients).all()

    def get_paginated(page, per_page):
        clients = session.query(Clients).offset((page - 1) * per_page).limit(per_page).all()
        total_clients_count = session.query(func.count(Clients.id)).scalar()
        return clients, total_clients_count

    def get_by_id(client_id):
        return session.query(Clients).filter_by(id=client_id).first()

    def get_by_document(client_document):
        return session.query(Clients).filter_by(document=client_document).first()

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()