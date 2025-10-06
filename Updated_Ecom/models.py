from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime





class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    user_email = Column(String(255), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)
    user_phone = Column(String, nullable=True)
    user_address = Column(String(256), nullable=True)
    user_role = Column(String(20), default="user", nullable=False)

    users_orders = relationship("Orders", back_populates="orders_users")
    userscart = relationship("Carts", back_populates="cartusers")



class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    product_price = Column(Integer)
    product_stock = Column(Integer)
    producta_description = Column(String(500))

    product_orderitems = relationship("OrderItems", back_populates="orderitems_product")
    products_cartitems = relationship("CartItems", back_populates="cartitems_products")




class Carts(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    cartusers = relationship("Users", back_populates="userscart")
    cart_cartitems = relationship("CartItems", back_populates="cartitems_cart")

class CartItems(Base):
    __tablename__ = "cartitems"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price_in_cart = Column(Integer, nullable=False)

    cartitems_cart = relationship("Carts", back_populates="cart_cartitems")
    cartitems_products = relationship("Products", back_populates="products_cartitems")




class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    orders_users = relationship("Users", back_populates="users_orders")
    orders_orderitems = relationship("OrderItems", back_populates="orderitems_orders")



class OrderItems(Base):
    __tablename__ = "orderitems"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False, default=1)
    price_at_order = Column(Integer, nullable=False)


    orderitems_orders = relationship("Orders", back_populates="orders_orderitems")
    orderitems_product = relationship("Products", back_populates="product_orderitems")


class Admins(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)
    details = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    admin = relationship("Users")