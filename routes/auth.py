from flask import Blueprint, request, jsonify
from extensions import db, bcrypt  # Import from extensions instead of app.py
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if the email is already in the database
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400  # Return an error response

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        name=data['name'], 
        email=data['email'], 
        password=hashed_password, 
        is_professional=data.get('is_professional', False)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={"id": user.id, "is_professional": user.is_professional})
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# New Endpoint 1: Get Current User Profile
@auth_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_professional": user.is_professional
    }
    return jsonify(user_data), 200

# New Endpoint 2: Update User Profile
@auth_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

# New Endpoint 3: Change Password
@auth_blueprint.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not bcrypt.check_password_hash(user.password, old_password):
        return jsonify({"message": "Old password is incorrect"}), 401
    
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200

# New Endpoint 4: Delete User Account
@auth_blueprint.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200
