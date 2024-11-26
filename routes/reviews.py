from flask import Blueprint, request, jsonify
from extensions import db
from models import Review, Professional, User

reviews_blueprint = Blueprint('reviews', __name__)

@reviews_blueprint.route('/', methods=['POST'])
def submit_review():
    """
    Submit a review for a professional.
    Body Params:
    - user_id: ID of the user submitting the review.
    - professional_id: ID of the professional.
    - rating: Rating out of 5.
    - comment: [Optional] Text comment.
    """
    data = request.get_json()
    review = Review(
        user_id=data['user_id'],
        professional_id=data['professional_id'],
        rating=data['rating'],
        comment=data.get('comment', "")
    )
    db.session.add(review)

    # Update the professional's rating
    professional = Professional.query.get(data['professional_id'])
    total_reviews = professional.reviews_count + 1
    new_rating = (professional.rating * professional.reviews_count + data['rating']) / total_reviews
    professional.rating = new_rating
    professional.reviews_count = total_reviews

    db.session.commit()
    return jsonify({"message": "Review submitted successfully"}), 201

@reviews_blueprint.route('/<int:professional_id>', methods=['GET'])
def get_professional_reviews(professional_id):
    """
    Get all reviews for a specific professional.
    """
    reviews = Review.query.filter_by(professional_id=professional_id).all()
    return jsonify([
        {
            "id": r.id,
            "user_name": User.query.get(r.user_id).name,
            "rating": r.rating,
            "comment": r.comment
        }
        for r in reviews
    ]), 200
