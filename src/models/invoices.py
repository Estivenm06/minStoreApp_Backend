from datetime import UTC, datetime

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, func

from src.models import Base, session


class PaymentMethods:
    CASH = 'cash'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    PAYPAL = 'paypal'
    BANK_TRANSFER = 'bank_transfer'
    #OTHER = 'other'

class Status:
    PENDING = 'pending'
    PAID = 'paid'
    CANCELLED = 'cancelled'

class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    id_client = Column(ForeignKey('clients.id'), nullable=False)
    id_user = Column(ForeignKey('users.id'), nullable=False)
    invoice_number = Column(String(20), nullable=False, unique=True)
    date_issued = Column(Date, nullable=False)
    subtotal = Column(Float(12, 2), nullable=False)
    tax = Column(Float(12, 2), nullable=False, default=0.00)
    total = Column(Float(12, 2), nullable=False)
    payment_method = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default=Status.PENDING)

    def __init__(self, id_client, id_user, invoice_number, subtotal, tax, total, payment_method, status=Status.PENDING, date_issued=None):
        self.id_client = id_client
        self.id_user = id_user
        self.invoice_number = invoice_number
        self.subtotal = subtotal
        self.tax = tax
        self.total = total
        self.payment_method = payment_method
        self.date_issued = date_issued or datetime.now(UTC)
        self.status = status

    def __repr__(self):
        return f"<Invoice(id={self.id}, id_client={self.id_client}, id_user={self.id_user}, invoice_number='{self.invoice_number}', date_issued={self.date_issued}, subtotal={self.subtotal}, tax={self.tax}, total={self.total}, payment_method='{self.payment_method}', status='{self.status}')>"

    def get_all():
        return session.query(Invoices).all()

    def get_paginated(page, per_page):
        invoices = session.query(Invoices).offset((page - 1) * per_page).limit(per_page).all()
        total_invoices_count = session.query(func.count(Invoices.id)).scalar()
        return invoices, total_invoices_count

    def get_paginated_by_user(user_id, page, per_page):
        invoices = session.query(Invoices).filter_by(id_user=user_id).offset((page - 1) * per_page).limit(per_page).all()
        total_invoices_count = session.query(func.count(Invoices.id)).filter_by(id_user=user_id).scalar()
        return invoices, total_invoices_count

    def get_by_id(invoice_id):
        return session.query(Invoices).filter_by(id=invoice_id).first()

    def get_by_invoice_number(invoice_number):
        return session.query(Invoices).filter_by(invoice_number=invoice_number).first()

    def get_by_client_id(client_id):
        return session.query(Invoices).filter_by(id_client=client_id).all()

    def get_by_user_id(user_id):
        return session.query(Invoices).filter_by(id_user=user_id).all()

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()
