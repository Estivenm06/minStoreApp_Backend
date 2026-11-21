from sqlalchemy import Column, Integer, String

from src.models import Base, session


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', description='{self.description}')>"

    def get_all():
        return session.query(Categories).all()

    def get_by_id(category_id):
        return session.query(Categories).get(category_id)

    def get_by_name(name):
        return session.query(Categories).filter_by(name=name).first()

    def save(self):
        session.add(self)
        session.commit()    

    def update(self):
        session.commit()