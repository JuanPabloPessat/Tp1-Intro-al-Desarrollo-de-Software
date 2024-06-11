from flask import Flask, request, jsonify
from models import db 
from flask_cors import CORS
import json
from models import Producto, Usuario, Carrito


app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/productos', methods=['GET'])
def obtener_productos():
	try:
		productos = Producto.query.all()
		productos_data = []
		for producto in productos:
			data_producto = {
				'id_producto': producto.id_producto,
				'nombre': producto.nombre,
				'imagen': producto.imagen,
				'descripcion': producto.descripcion,
				'precio': producto.precio,
				'stock': producto.stock
			}
			productos_data.append(data_producto)
		return jsonify(productos_data), 200
	except Exception as error:
		print('Error', error)
		return jsonify({'message': 'Internal server error'}), 500


@app.route('/productos/<id_producto>', methods=['GET'])
def obtener_producto_Id(id_producto):
	try:
		producto = Producto.query.where(Producto.id_producto == id_producto).first()
		data_producto = {
			'id_producto': producto.id_producto,
			'nombre': producto.nombre,
			'imagen': producto.imagen,
			'descripcion': producto.descripcion,
			'precio': producto.precio,
			'stock': producto.stock
		}
		return jsonify(data_producto), 200
	except Exception as error:
		print('Error', error)
		return jsonify({'message': 'Internal server error'}), 500


@app.route('/usuario/<id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
	try:
		usuario = Usuario.query.where(Usuario.id == id_usuario).first()
		usuario_data = {
			'id': usuario.id,
			'nombre': usuario.nombre,
			'contraseña': usuario.contraseña,
			'id_carrito': usuario.id_carrito
		}
		return usuario_data
	except Exception as error:
		print('Error', error)
		return jsonify({'message': 'Internal server error'}), 500


with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)