from flask import Flask, jsonify, request, render_template
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
        products = Product.query.order_by(Product.product_id).all()
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
        user_cart = Cart.query.where(Cart.cart_id == cart_id).first()
        db.session.delete(product)
        user_cart.products_amount -= 1
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

@app.route('/cart/make_purchase/<cart_id>', methods=['DELETE'])
def make_purchase(cart_id):
    try:
        cart_products = CartProduct.query.where(CartProduct.cart_id == cart_id).all()
        user_cart = Cart.query.where(Cart.cart_id == cart_id).first()

        #Disminuye el stock de los productos en el carrito antes de limpiar el carrito
        for cart_product in cart_products:
            stock_product = Product.query.get(cart_product.product_id)
            if stock_product.stock > 0:
                stock_product.stock -= 1
                db.session.add(stock_product)
        db.session.commit()

        #limpia el carrito
        CartProduct.query.where(CartProduct.cart_id == cart_id).delete()
        user_cart.products_amount = 0
        db.session.commit()

        return jsonify({"success": True}), 200

    except:
        return jsonify({"success": False}), 400


@app.route('/user/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        name = request.json.get("name")
        password = request.json.get("password")

        user = User.query.filter_by(name=name).first()

        if user and user.password == password:
            return jsonify({"success": True, "userId": user.id}), 200
        else:
            return jsonify({"success": False, "message": "Nombre o contraseña inválidos"}), 400

    return render_template('login.html')

@app.route('/user/register', methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':

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

        new_user = User(name=name,password=password)
        db.session.add(new_user)
        db.session.commit()

        cart_id = new_user.id
        new_cart = Cart(cart_id = cart_id, products_amount=0)
        db.session.add(new_cart)
        db.session.commit()

        new_user.cart_id = cart_id
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

@app.route('/user/delete_account/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:

        user = User.query.where(User.id == user_id).first()
        user_cart = Cart.query.where(Cart.cart_id == user.cart_id).first()

        if user:
            user_cart = Cart.query.where(Cart.cart_id == user.cart_id).first()
            print(user_cart.cart_id)
            cart_products = CartProduct.query.where(CartProduct.cart_id == user_cart.cart_id).all()
            print(f"Cart products: {cart_products}")
            CartProduct.query.where(CartProduct.cart_id==user_cart.cart_id).delete()
            db.session.commit()

            db.session.delete(user_cart)
            db.session.delete(user)
        else:
            return jsonify({"success": False}), 400
        db.session.commit()

        return jsonify({"success": True}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"success": False}), 400

@app.route('/user/cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.json.get("product_id")
        cart_id = request.json.get("cart_id")

        add_product = CartProduct(product_id=product_id, cart_id=cart_id)
        db.session.add(add_product)
        db.session.commit()

        user_cart = Cart.query.where(Cart.cart_id == cart_id).first()
        user_cart.products_amount += 1
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