from sqlalchemy import create_engine, UniqueConstraint

DATABASE_URL = "postgresql+psycopg2://postgres:example@db:5432/data_challenge"
engine = create_engine(DATABASE_URL, echo=True)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    product = relationship("Product", back_populates="restaurant")

    def __repr__(self):
        return f"Restaurant(id={self.id}, name={self.name}, address={self.address}, phone={self.phone}, website={self.website})"

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    allergens = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    picture = Column(String, nullable=True)

    restaurant = relationship("Restaurant", back_populates="product")
    category = relationship("Category", back_populates="product")

    __table_args__ = (
        UniqueConstraint('name', 'restaurant_id', 'category_id'),
    )
    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, ingredients={self.ingredients}, restaurants={self.restaurants}, allergens={self.allergens}, category={self.category}, picture={self.picture})"

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    product = relationship("Product", back_populates="category")
    def __repr__(self):
        return f"category(id={self.id}, name={self.name})"



def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        for key, value in defaults.items():
            setattr(instance, key, value)
        return instance, False
    else:
        params = {**kwargs, **defaults}
        instance = model(**params)
        session.add(instance)
        return instance, True

