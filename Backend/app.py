from flask import Flask, jsonify, request, render_template, redirect
from db.models import db 
from flask_cors import CORS
from db.models import Product, User, Cart

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/products', methods=['GET'])
def obtener_productos():
    try:
        productos = Producto.query.all()
        productos_data = []
        for producto in productos:
            data_producto = {
                'product_id': producto.product_id,
                'name': producto.name,
                'image': producto.image,
                'price': producto.price,
                'stock': producto.stock
            }
            productos_data.append(data_producto)
        return jsonify(productos_data), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/products/<products_id>', methods=['GET'])
def obtener_producto_Id(products_id):
    try:
        producto = Producto.query.where(Product.product_id == products_id).first()
        data_producto = {
            'product_id': producto.product_id,
            'name': producto.name,
            'image': producto.image,
            'price': producto.price,
            'stock': producto.stock
        }
        return jsonify(data_producto), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/usuario/inicio-sesion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']

        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and usuario.contraseña == contraseña:
            # session['nombre'] = usuario.nombre ver session de flask
            return redirect('/productos')
        else:
            return render_template('login.html', error='Usuario incorrecto')

    return render_template('login.html')

@app.route('/usuario/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']

        if nombre == '' or contraseña == '':
            return render_template('registro.html', error='Nombre o Contraseña invalidos')

        nuevo_usuario = Usuario(nombre=nombre, contraseña=contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect('/usuario/inicio-sesion')
    
    return render_template('registro.html')

@app.route('/usuario/<id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    try:
        usuario = Usuario.query.where(Usuario.id == id_usuario).first()
        usuario_data = {
            'id': usuario.id,
            'name': usuario.name,
            'password': usuario.password,
            'cart_id': usuario.cart_id
        }
        return jsonify(usuario_data), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/carrito')
def carrito():
    return

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)