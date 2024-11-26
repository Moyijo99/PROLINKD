from flask import Blueprint, request, jsonify
from app import db
from models import Booking, User, Professional

bookings_blueprint = Blueprint('bookings', __name__)

@bookings_blueprint.route('/', methods=['POST'])
def create_booking():
    """
    Create a new booking.
    Body Params:
    - user_id: ID of the user making the booking.
    - professional_id: ID of the professional.
    - date: Date of the appointment.
    """
    data = request.get_json()
    booking = Booking(
        user_id=data['user_id'],
        professional_id=data['professional_id'],
        date=data['date']
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking created successfully"}), 201

@bookings_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    """
    Retrieve all bookings for a specific user.
    """
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": b.id,
            "professional_name": User.query.get(Professional.query.get(b.professional_id).user_id).name,
            "date": b.date,
            "status": b.status
        }
        for b in bookings
    ]), 200
