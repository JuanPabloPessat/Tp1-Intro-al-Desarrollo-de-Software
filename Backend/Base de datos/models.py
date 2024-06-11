import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
	__tablename__ = 'Tabla_productos'
	id_producto = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(255), nullable=False)
	imagen = db.Column(db.String(255), nullable=False)
	descripcion = db.Column(db.String(255), nullable=False)
	precio = db.Column(db.Integer, nullable=False)
	stock = db.Column(db.Integer)

class Usuario(db.Model):
	__tablename__ = 'Tabla_usuarios'
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(255), nullable=False, unique=True)
	contraseña = db.Column(db.String(255), nullable=False)
	id_carrito = db.Column(db.Integer, db.ForeignKey('Tabla_carritos.id_carrito'))

class Carrito(db.Model):
	__tablename__ = 'Tabla_carritos'
	id_carrito = db.Column(db.Integer, primary_key=True)
	Tabla_usuarios = db.relationship("Usuario")


