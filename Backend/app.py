from flask import Flask, jsonify, request, render_template, redirect
from db.models import db 
from flask_cors import CORS
from db.models import Product, User, Cart, CartProduct

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        products_data = []
        for product in products:
            data_product = {
                'product_id': product.product_id,
                'name': product.name,
                'image': product.image,
                'price': product.price,
                'stock': product.stock
            }
            products_data.append(data_product)
        return jsonify(products_data), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/cart/products/<id_cart>', methods=['GET'])
def get_cart_products(id_cart):
    try:
        results = db.session.query(Product.product_id, Product.name, Product.image, Product.price, Product.stock).\
            join(Cart.products).where(Cart.cart_id == id_cart).all()

        cart_products_data = []
        for product in results:
            data_product = {
                'product_id': product.product_id,
                'name': product.name,
                'image': product.image,
                'price': product.price,
                'stock': product.stock
            }
            cart_products_data.append(data_product)
        return jsonify(cart_products_data), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/cart/remove_products', methods=['GET', 'POST'])
def remove_cart_products():
    try:
        data = request.json
        cart_id = data.get('cart_id')
        product_id = data.get('product_id')

        product = CartProduct.query.where(CartProduct.product_id == product_id, CartProduct.cart_id == cart_id).first()

        db.session.delete(product)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/products/<products_id>', methods=['GET'])
def get_product_Id(products_id):
    try:
        product = Product.query.where(Product.product_id == products_id).first()
        data_product = {
            'product_id': product.product_id,
            'name': product.name,
            'image': product.image,
            'price': product.price,
            'stock': product.stock
        }
        return jsonify(data_product), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/user/login', methods=['GET', 'POST']) # Falta ir al home ya logueado, por ahora va al home pero sin loguear
def login():
    if request.method == 'POST':
        name = request.json.get("name")
        password = request.json.get("password")

        user = User.query.filter_by(name=name).first()

        if user and user.password == password:
            #session['nombre'] = usuario.nombre ver session de flask
            return jsonify({"success": True, "userId": user.id}), 200
        else:
            return jsonify({"success": False, "message": "Nombre o contraseña inválidos"}), 400

    return render_template('login.html')

@app.route('/user/register', methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':
        
        ultimo_usuario = User.query.order_by(User.id.desc()).first()
        if ultimo_usuario is not None:
            cart_id = ultimo_usuario.id + 1
        else:
            cart_id = 1

        name = request.json.get("name")
        password = request.json.get("password")

        users = User.query.all()
        users_name = []
        for user in users:
            users_name.append(user.name)

        if name == '' or password == '':
            return jsonify({"success": False, "message": "Nombre o contraseña inválidos"}), 400
        elif not name or not password:
            return jsonify({"success": False, "message": "Nombre o contraseña inválidos"}), 400
        elif name in users_name:
            return jsonify({"success": False, "message": "Ese nombre ya se encuentra registrado"}), 400

        new_cart = Cart(cart_id=cart_id)
        db.session.add(new_cart)
        db.session.commit()

        new_user = User(name=name,password=password, cart_id=cart_id)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True}), 200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.where(User.id == user_id).first()
        user_data = {
            'id': user.id,
            'name': user.name,
            'password': user.password,
            'cart_id': user.cart_id
        }
        return jsonify(user_data), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/user/cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.json.get("product_id")
        cart_id = request.json.get("cart_id")

        add_product = CartProduct(product_id=product_id, cart_id=cart_id)
        db.session.add(add_product)
        db.session.commit()

        return jsonify({"success": True}), 200

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500




with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)