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

@app.route('/user/login', methods=['GET', 'POST']) # Todavia no terminado
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(nombre=name).first()

        if user and user.password == password:
            # session['name'] = usuario.nombre ver session de flask
            return redirect('/products')
        else:
            return render_template('login.html', error='Usuario incorrecto')

    return render_template('login.html')

@app.route('/user/register', methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':
        name = request.json.get("name")
        password = request.json.get("password")

        if name == '' or password == '':
            return jsonify({"success": False, "message": "Nombre o contraseña inválidos"}), 400
        elif not name or not password:
            return jsonify({"success": False, "message": "Nombre o contraseña inválidos"}), 400

        new_user = User(name=name,password=password)
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

@app.route('/cart')
def cart():
    return

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)