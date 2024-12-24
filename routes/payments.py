from flask import Blueprint, request, jsonify
from extensions import db
from models import Payment

payments_blueprint = Blueprint('payments', __name__)

@payments_blueprint.route('/', methods=['POST'])
def make_payment():
    """
    Make a payment.
    Body Params:
    - user_id: ID of the user making the payment.
    - amount: Payment amount.
    - method: Payment method (e.g., 'credit_card', 'paypal').
    """
    data = request.get_json()
    payment = Payment(
        user_id=data['user_id'],
        amount=data['amount'],
        method=data['method']
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment successful"}), 201

@payments_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user_payments(user_id):
    """
    Get all payment records for a user.
    """
    payments = Payment.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": p.id,
            "amount": p.amount,
            "method": p.method,
            "date": p.created_at
        }
        for p in payments
    ]), 200
