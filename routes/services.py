from flask import Blueprint, request, jsonify
from extensions import db
from models import Service

services_blueprint = Blueprint('services', __name__)

# List all services or filter by category
@services_blueprint.route('/', methods=['GET'])
def list_services():
    """
    List all services or filter by name or category.
    Query Params:
    - category: Filter by service category.
    """
    category = request.args.get('category')
    query = Service.query
    if category:
        query = query.filter(Service.category.ilike(f'%{category}%'))
    services = query.all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "category": s.category
        }
        for s in services
    ]), 200

# Get details of a specific service
@services_blueprint.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """
    Get details of a specific service.
    """
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"message": "Service not found"}), 404
    return jsonify({
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "category": service.category
    }), 200

# Create a new service (admin only)
@services_blueprint.route('/', methods=['POST'])
def create_service():
    """
    Create a new service.
    Body Params:
    - name: Name of the service.
    - description: Description of the service.
    - category: Category of the service.
    """
    data = request.get_json()
    service = Service(
        name=data['name'],
        description=data['description'],
        category=data['category']
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({"message": "Service created successfully"}), 201

# Update an existing service
@services_blueprint.route('/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    """
    Update an existing service.
    """
    data = request.get_json()
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.category = data.get('category', service.category)
    db.session.commit()
    return jsonify({"message": "Service updated successfully"}), 200

# Delete a service
@services_blueprint.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    """
    Delete a service.
    """
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200
