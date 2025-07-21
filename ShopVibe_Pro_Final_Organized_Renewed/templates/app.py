
import requests

def verify_recaptcha(response_token):
    secret_key = "6LcUhlgrAAAAAJwVJ8FvAF9gADFCe5SiVyAoQNu5"
    payload = {
        'secret': secret_key,
        'response': response_token
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    return r.json().get('success', False)

from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify, flash
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import io
import pandas as pd
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'

# MongoDB connection
client = MongoClient('mongodb+srv://username:password@cluster.mongodb.net/mydb?retryWrites=true&w=majority')
db = client['mydb']

# Create indexes for performance
db.orders.create_index([('user_id', ASCENDING)])
db.users.create_index([('username', ASCENDING)], unique=True)
db.coupons.create_index([('code', ASCENDING)], unique=True)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('ليس لديك صلاحية الدخول لهذه الصفحة')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if db.users.find_one({'username': username}):
            flash('اسم المستخدم موجود مسبقاً')
            return redirect(url_for('register'))
        hashed = generate_password_hash(password)
        db.users.insert_one({'username': username, 'password': hashed, 'role': 'user'})
        flash('تم التسجيل بنجاح، الرجاء تسجيل الدخول')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')
            flash('تم تسجيل الدخول بنجاح')
            return redirect(url_for('home'))
        flash('اسم المستخدم أو كلمة المرور غير صحيحة')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج')
    return redirect(url_for('login'))

@app.route('/')
def home():
    products = list(db.products.find())
    return render_template('home.html', products=products)

@app.route('/add-to-cart/<product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    session['cart'] = cart
    flash('تمت إضافة المنتج إلى السلة')
    return redirect(url_for('home'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    products = []
    total = 0
    for pid, qty in cart.items():
        product = db.products.find_one({'_id': ObjectId(pid)})
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            products.append({'_id': pid, 'name': product['name'], 'price': product['price'], 'quantity': qty, 'subtotal': subtotal})
    return render_template('cart.html', products=products, total=total)

@app.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    cart = {}
    for pid, qty in request.form.items():
        try:
            qty_int = int(qty)
            if qty_int > 0:
                cart[pid] = qty_int
        except:
            continue
    session['cart'] = cart
    flash('تم تحديث السلة')
    return redirect(url_for('cart'))

@app.route('/remove-from-cart/<product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart
    flash('تمت إزالة المنتج من السلة')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('السلة فارغة')
        return redirect(url_for('home'))
    products = []
    total = 0
    for pid, qty in cart.items():
        product = db.products.find_one({'_id': ObjectId(pid)})
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            products.append({'_id': pid, 'name': product['name'], 'price': product['price'], 'quantity': qty, 'subtotal': subtotal})

    discount = 0
    coupon_code = ''
    if request.method == 'POST':
        coupon_code = request.form.get('coupon_code','').strip()
        coupon = db.coupons.find_one({'code': coupon_code, 'active': True})
        if coupon:
            discount = coupon['discount']
            flash(f'تم تطبيق الكوبون بنجاح. خصم {discount} MAD')
        else:
            flash('كود الكوبون غير صالح')

        total_after_discount = max(total - discount, 0)
        order_data = {
            'user_id': ObjectId(session['user_id']),
            'items': products,
            'total': total_after_discount,
            'coupon_code': coupon_code if discount > 0 else None,
            'discount': discount
        }
        order_id = db.orders.insert_one(order_data).inserted_id
        session.pop('cart', None)
        flash('تم إنشاء الطلب بنجاح')
        return redirect(url_for('invoice', order_id=str(order_id)))
    return render_template('checkout.html', products=products, total=total, discount=discount, coupon_code=coupon_code)

@app.route('/my-account')
@login_required
def my_account():
    orders = list(db.orders.find({'user_id': ObjectId(session['user_id'])}))
    return render_template('my_account.html', orders=orders)

@app.route('/invoice/<order_id>')
@login_required
def invoice(order_id):
    order = db.orders.find_one({'_id': ObjectId(order_id)})
    if not order:
        flash('الطلب غير موجود')
        return redirect(url_for('my_account'))
    if str(order['user_id']) != session['user_id'] and session.get('role') != 'admin':
        flash('غير مخول لعرض هذه الفاتورة')
        return redirect(url_for('my_account'))
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"فاتورة الطلب رقم {order_id}", ln=True, align='C')
    pdf.ln(10)
    for item in order.get('items', []):
        pdf.cell(0, 10, f"{item['name']} - الكمية: {item['quantity']} - السعر: {item['price']} MAD", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, f"المجموع: {order.get('total', 0)} MAD", ln=True)
    if order.get('discount'):
        pdf.cell(0, 10, f"الخصم: {order.get('discount')} MAD", ln=True)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return send_file(pdf_output, mimetype='application/pdf', download_name=f'invoice_{order_id}.pdf')

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = list(db.orders.find())
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/export-orders')
@admin_required
def export_orders():
    orders = list(db.orders.find())
    for o in orders:
        o['_id'] = str(o['_id'])
        o['user_id'] = str(o['user_id'])
    df = pd.DataFrame(orders)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Orders')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name='orders.xlsx', as_attachment=True)

# يمكنك إضافة واجهة إدارة منتجات لاحقاً

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/store")
def store():
    with open("item.json", "r") as f:
        products = json.load(f)
    return render_template("store.html", products=products)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    recaptcha_response = request.form.get("g-recaptcha-response")
    if not verify_recaptcha(recaptcha_response):
        return "reCAPTCHA failed", 400

    product_id = request.form.get("product_id")
    with open("item.json", "r") as f:
        products = json.load(f)

    product = next((p for p in products if str(p["_id"]) == str(product_id)), None)
    if not product:
        return "Product not found", 404

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    for item in cart:
        if item["_id"] == product["_id"]:
            item["quantity"] += 1
            break
    else:
        product["quantity"] = 1
        cart.append(product)

    session["cart"] = cart
    return redirect("/cart")

@app.route("/cart")
def cart():
    return render_template("cart.html", cart=session.get("cart", []))

@app.route("/checkout", methods=["POST"])
def checkout():
    recaptcha_response = request.form.get("g-recaptcha-response")
    if not verify_recaptcha(recaptcha_response):
        return "reCAPTCHA failed", 400

    cart = session.get("cart", [])
    if not cart:
        return "Cart is empty", 400

    return "Payment logic here (Stripe integration)"
