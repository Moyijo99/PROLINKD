from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Import routes after initializing extensions
from routes.auth import auth_blueprint
from routes.professionals import professionals_blueprint
from routes.bookings import bookings_blueprint
from routes.reviews import reviews_blueprint

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
