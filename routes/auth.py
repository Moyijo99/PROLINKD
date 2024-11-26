from flask import Blueprint, request, jsonify
from app import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['name'], email=data['email'], password=hashed_password, is_professional=data.get('is_professional', False))
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
