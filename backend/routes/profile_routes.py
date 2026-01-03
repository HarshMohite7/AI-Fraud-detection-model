from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.db.user_queries import get_user_by_id

profile_routes = Blueprint("profile_routes", __name__)

@profile_routes.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    user_id = identity["id"]

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200
