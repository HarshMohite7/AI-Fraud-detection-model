from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required
from backend.db.dashboard_queries import get_dashboard_stats, get_recent_transactions

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def stats():
    stats_data = get_dashboard_stats()
    if stats_data:
        return jsonify(stats_data), 200
    else:
        return jsonify({"error": "Failed to fetch stats"}), 500

@dashboard_bp.route('/transactions/recent', methods=['GET'])
@jwt_required()
def recent_transactions():
    transactions = get_recent_transactions()
    return jsonify(transactions), 200
