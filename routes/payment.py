
from flask import Blueprint, request, jsonify, url_for
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

payment_bp = Blueprint('payment', __name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@payment_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': data.get('product_name', 'Order')},
                'unit_amount': int(float(data.get('amount', 1)) * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('shop.home', _external=True) + '?success=true',
        cancel_url=url_for('shop.cart', _external=True) + '?canceled=true',
    )
    return jsonify(id=session.id)
