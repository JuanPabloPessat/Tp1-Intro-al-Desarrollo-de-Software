import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class Cart(db.Model):
	__tablename__ = 'Cart_table'
	cart_id = db.Column(db.Integer, primary_key=True)
	Users_table = db.relationship("User")


