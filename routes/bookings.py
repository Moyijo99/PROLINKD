from flask import Blueprint, request, jsonify
from extensions import db
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

# New Endpoint 1: Update Booking
@bookings_blueprint.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """
    Update an existing booking.
    Body Params:
    - date: New date for the appointment (optional).
    - status: New status of the booking (optional).
    """
    data = request.get_json()
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    booking.date = data.get('date', booking.date)
    booking.status = data.get('status', booking.status)
    db.session.commit()
    return jsonify({"message": "Booking updated successfully"}), 200

# New Endpoint 2: Cancel Booking
@bookings_blueprint.route('/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """
    Cancel a booking by ID.
    """
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking cancelled successfully"}), 200

# New Endpoint 3: Get All Bookings for a Professional
@bookings_blueprint.route('/professional/<int:professional_id>', methods=['GET'])
def get_professional_bookings(professional_id):
    """
    Retrieve all bookings for a specific professional.
    """
    bookings = Booking.query.filter_by(professional_id=professional_id).all()
    return jsonify([
        {
            "id": b.id,
            "user_name": User.query.get(b.user_id).name,
            "date": b.date,
            "status": b.status
        }
        for b in bookings
    ]), 200
