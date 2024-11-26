from flask import Blueprint, request, jsonify
from app import db
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
    query = Professional.query
    if service:
        query = query.filter(Professional.service.ilike(f'%{service}%'))
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
