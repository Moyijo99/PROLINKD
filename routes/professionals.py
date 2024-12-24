from flask import Blueprint, request, jsonify
from extensions import db
from models import Professional, User

professionals_blueprint = Blueprint('professionals', __name__)

@professionals_blueprint.route('/', methods=['GET'])
def list_professionals():
    """
    List all professionals or search by service.
    Query Params:
    - service: Filter by service type.
    - location: [Optional] Filter by location (if location is added to the model).
    """
    service = request.args.get('service')
    location = request.args.get('location')  # Optional filter by location
    query = Professional.query
    
    if service:
        query = query.filter(Professional.service.ilike(f'%{service}%'))
    
    if location:
        query = query.filter(Professional.location.ilike(f'%{location}%'))  # Assuming location exists in the model
    
    professionals = query.all()
    return jsonify([
        {
            "id": p.id,
            "name": User.query.get(p.user_id).name,
            "service": p.service,
            "rating": p.rating,
            "reviews_count": p.reviews_count
        }
        for p in professionals
    ]), 200

@professionals_blueprint.route('/<int:professional_id>', methods=['GET'])
def get_professional(professional_id):
    """
    Get details of a specific professional.
    """
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": "Professional not found"}), 404
    user = User.query.get(professional.user_id)
    return jsonify({
        "id": professional.id,
        "name": user.name,
        "email": user.email,
        "service": professional.service,
        "rating": professional.rating,
        "reviews_count": professional.reviews_count
    }), 200

# New Endpoint 1: Add a New Professional
@professionals_blueprint.route('/', methods=['POST'])
def add_professional():
    """
    Add a new professional.
    Body Params:
    - user_id: ID of the user to be linked with this professional.
    - service: Service the professional offers.
    - location: (Optional) Location where the professional operates.
    - rating: Initial rating (defaults to 0).
    """
    data = request.get_json()
    professional = Professional(
        user_id=data['user_id'], 
        service=data['service'], 
        location=data.get('location'),  # Optional field
        rating=data.get('rating', 0),  # Default to 0
        reviews_count=0  # Default count to 0
    )
    db.session.add(professional)
    db.session.commit()
    return jsonify({"message": "Professional added successfully"}), 201

# New Endpoint 2: Update a Professional's Information
@professionals_blueprint.route('/<int:professional_id>', methods=['PUT'])
def update_professional(professional_id):
    """
    Update information about a professional.
    Body Params:
    - service: Updated service type.
    - location: Updated location.
    - rating: Updated rating (Optional, usually based on reviews).
    """
    data = request.get_json()
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": "Professional not found"}), 404
    
    professional.service = data.get('service', professional.service)
    professional.location = data.get('location', professional.location)
    professional.rating = data.get('rating', professional.rating)
    db.session.commit()
    return jsonify({"message": "Professional updated successfully"}), 200

# New Endpoint 3: Delete a Professional
@professionals_blueprint.route('/<int:professional_id>', methods=['DELETE'])
def delete_professional(professional_id):
    """
    Delete a professional.
    """
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": "Professional not found"}), 404
    
    db.session.delete(professional)
    db.session.commit()
    return jsonify({"message": "Professional deleted successfully"}), 200
