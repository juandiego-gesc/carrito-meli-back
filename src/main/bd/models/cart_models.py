from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Table, func, Enum as SQLEnum
from enum import Enum
from src.main.bd.config.database import Base
from sqlalchemy.orm import relationship

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	username = Column(String(150), unique=True, index=True)
	name = Column(String(150), unique=False, index=False)
	email = Column(String(150), unique=True, index=True)
	hashed_password = Column(String(150))

	del_flag = Column(Boolean, default=False)
	created_at = Column(DateTime, server_default=func.now())
	updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

	cart_items = relationship("CartItem", back_populates="user")


class Product(Base):
	__tablename__ = "product"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	name = Column(String(150), unique=False, index=True)
	price = Column(Float, unique=False, index=False)
	image_url = Column(String(150), unique=False, index=False)
	description = Column(String(150), unique=False, index=False)

	del_flag = Column(Boolean, default=False)
	created_at = Column(DateTime, server_default=func.now())
	updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

	carts = relationship("CartItem", back_populates="product")

class CartItem(Base):
	__tablename__ = "cart_item"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("user.id"))
	product_id = Column(Integer, ForeignKey("product.id"))
	quantity = Column(Integer, unique=False, index=False)

	del_flag = Column(Boolean, default=False)
	created_at = Column(DateTime, server_default=func.now())
	updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
	
	user = relationship("User", back_populates="cart_items")
	product = relationship("Product", back_populates="carts")

