import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabla de unión para poder tener muchos productos en un solo carrito
cart_product = db.Table('cart_product',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('cart_id', db.Integer, db.ForeignKey('Cart_table.cart_id')),
    db.Column('product_id', db.Integer, db.ForeignKey('Products_table.product_id'))
)

class Product(db.Model):
    __tablename__ = 'Products_table'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'Users_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart_table.cart_id'))
    cart = db.relationship("Cart", backref="user")

class Cart(db.Model):
    __tablename__ = 'Cart_table'
    cart_id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('Product', secondary=cart_product, lazy='subquery')
    



