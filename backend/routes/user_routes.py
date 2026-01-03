from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.db.db_connection import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database error"}), 500
        
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, email, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database error"}), 500
        
    cursor = conn.cursor(dictionary=True)
    try:
        if password:
            import hashlib
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("UPDATE users SET name = %s, email = %s, password_hash = %s WHERE id = %s", (name, email, hashed_pw, user_id))
        else:
            cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
            
        conn.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
