from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CartProduct(db.Model):
    __tablename__ = 'Cart_product'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart_table.cart_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products_table.product_id'))

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
    products_amount = db.Column(db.Integer)
    products = db.relationship('Product', secondary='Cart_product', lazy='subquery')