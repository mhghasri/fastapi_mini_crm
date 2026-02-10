from sqlalchemy import create_engine, Column, Integer, String, JSON, UUID, Float, Text, Boolean, Numeric, Date, DateTime, Time, ForeignKey, Interval, Enum, ARRAY, LargeBinary, Table, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100))
    email = Column(String(150), unique=True)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())

    orders =relationship("Order", backref="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"customer_id: {self.id}, name: {self.name}, email: {self.email}"
    
class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(Text(), nullable=True)
    price = Column(Float(), default=0)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())

    customer_id = Column(Integer, ForeignKey("customer.id"))

    def __repr__(self):
        return f"order_id: {self.id}, title: {self.title}, price: {self.price}, customer_id: {self.customer_id}"
    
