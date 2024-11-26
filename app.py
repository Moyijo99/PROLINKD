from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)  # Initialize db first
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import routes after db initialization
from routes.auth import auth_blueprint
from routes.professionals import professionals_blueprint
from routes.bookings import bookings_blueprint
from routes.reviews import reviews_blueprint

# Import models after db initialization to avoid circular import
from models import User, Professional, Booking, Review

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(professionals_blueprint, url_prefix='/api/professionals')
app.register_blueprint(bookings_blueprint, url_prefix='/api/bookings')
app.register_blueprint(reviews_blueprint, url_prefix='/api/reviews')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
