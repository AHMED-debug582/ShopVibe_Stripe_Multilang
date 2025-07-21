
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from bson.objectid import ObjectId
import datetime

main = Blueprint("main", __name__)

@main.route('/')
def home():
    products = current_app.mongo.products.find().limit(6)
    return render_template('home.html', products=products)

@main.route('/products')
def product_list():
    products = current_app.mongo.products.find()
    return render_template('product_list.html', products=products)

@main.route('/product/<id>')
def product_detail(id):
    product = current_app.mongo.products.find_one({'_id': ObjectId(id)})
    return render_template('product_detail.html', product=product)

@main.route('/add_to_cart/<id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[id] = cart.get(id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@main.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for pid, qty in session['cart'].items():
            product = current_app.mongo.products.find_one({'_id': ObjectId(pid)})
            if product:
                subtotal = product['price'] * qty
                total += subtotal
                cart_items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render_template('cart.html', cart_items=cart_items, total=total)

@main.route('/update_cart', methods=['POST'])
def update_cart():
    session['cart'] = {k: int(v[0]) for k, v in request.form.to_dict(flat=False).items()}
    return redirect(url_for('main.cart'))

@main.route('/checkout')
def checkout():
    cart_items = []
    total = 0
    if 'cart' in session:
        for pid, qty in session['cart'].items():
            product = current_app.mongo.products.find_one({'_id': ObjectId(pid)})
            if product:
                subtotal = product['price'] * qty
                total += subtotal
                cart_items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render_template('checkout.html', cart_items=cart_items, total=total)


@main.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    cart = session.get('cart', {})
    line_items = []

    for pid, qty in cart.items():
        product = current_app.mongo.products.find_one({'_id': ObjectId(pid)})
        if product:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                    },
                    'unit_amount': int(product['price'] * 100),
                },
                'quantity': qty,
            })

    if not line_items:
        return redirect(url_for('main.cart'))

    session_data = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('main.payment_success', _external=True),
        cancel_url=url_for('main.payment_cancel', _external=True),
    )

    return redirect(session_data.url)

@main.route('/success')
def payment_success():
    session.pop('cart', None)
    return render_template('success.html')

@main.route('/cancel')
def payment_cancel():
    return render_template('cancel.html')
