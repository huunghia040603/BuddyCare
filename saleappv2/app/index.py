import math

from flask import render_template, request, redirect, session, jsonify
import dao
import utils
from saleappv2.app import app, login
from flask_login import login_user


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    products = dao.load_products(kw, cate_id, page)
    num = dao.count_product()

    return render_template('index.html', products=products,
                           pages=math.ceil(num/app.config['PAGE_SIZE']))


@app.route('/login')
def process_user_login():
    return render_template('login.html')


@app.route('/admin/login', methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    '''
    {
        "cart": {
            "1": {
                "id": "1",
                "name": "ABC",
                "price": 123,
                "quantity": 2
            },
            "2": {
                "id": "2",
                "name": "ABC",
                "price": 123,
                "quantity": 1
            }
        }
    }
    '''

    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart: # sp da co trong gio
        cart[id]['quantity'] += 1
    else: # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.context_processor
def common_resp():
    return {
        'categories': dao.load_categories(),
        'cart': utils.count_cart(session.get('cart'))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True,port=22000)
