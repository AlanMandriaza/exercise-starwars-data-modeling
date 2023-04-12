import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), unique=False, nullable=False)
    is_active = Column(Boolean(), unique=False, nullable=False)
    date_of_birth = Column(Date(), unique=False, nullable=True)
    address = Column(String(120), unique=False, nullable=True)
    city = Column(String(80), unique=False, nullable=True)
    country = Column(String(80), unique=False, nullable=True)
    phone_number = Column(String(20), unique=False, nullable=True)
    avatar = Column(String(120), unique=False, nullable=True)
    roles = relationship('Role', secondary='user_roles')

    
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', backref=backref('products', lazy=True))
    quantity = Column(Integer, nullable=False, default=0)



class PaymentItem(Base):
    __tablename__ = 'payment_items'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product')
    quantity = Column(Integer, nullable=False)


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)

  

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('orders', lazy=True))
    payment_id = Column(Integer, ForeignKey('payments.id'))
    payment = relationship('Payment', backref=backref('orders', lazy=True))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('reviews', lazy=True))
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', backref=backref('reviews', lazy=True))
    comment = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='carts')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    items = relationship('CartItem', backref='cart', lazy=True)

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship('Product')


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
