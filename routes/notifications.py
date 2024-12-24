from flask import Blueprint, request, jsonify
from extensions import db
from models import Notification

notifications_blueprint = Blueprint('notifications', __name__)

@notifications_blueprint.route('/', methods=['POST'])
def send_notification():
    """
    Send a notification to a user.
    Body Params:
    - user_id: ID of the user to notify.
    - message: Notification message.
    """
    data = request.get_json()
    notification = Notification(
        user_id=data['user_id'],
        message=data['message']
    )
    db.session.add(notification)
    db.session.commit()
    return jsonify({"message": "Notification sent successfully"}), 201

@notifications_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user_notifications(user_id):
    """
    Get all notifications for a specific user.
    """
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": n.id,
            "message": n.message,
            "date": n.created_at
        }
        for n in notifications
    ]), 200
