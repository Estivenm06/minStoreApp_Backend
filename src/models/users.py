import enum

from sqlalchemy import Boolean, Column, Integer, String

# Password hashing
from werkzeug.security import check_password_hash, generate_password_hash

from src.models import Base, session


class Role(str, enum.Enum):
    ADMIN = 'admin'
    SELLER = 'seller'
    PENDING = 'pending'

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    active = Column(Boolean, nullable=False, default=1)


    def __init__(self, username, name, password_hash, role):
        self.username = username
        self.name = name
        self.password_hash = generate_password_hash(password_hash)
        self.role = role
        self.active = 1

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', name='{self.name}', password_hash='{self.password_hash}', role='{self.role}', active={self.active})>"

    def get_user_by_id(user_id):
        return session.query(Users).filter_by(id=user_id).first()
    
    def get_user_by_username(username):
        return session.query(Users).filter_by(username=username).first()

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def login(self, password):
        return check_password_hash(self.password_hash, password)