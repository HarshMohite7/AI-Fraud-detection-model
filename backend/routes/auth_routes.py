from flask import Blueprint, request, jsonify
from backend.db.db_connection import get_db_connection
import mysql.connector
from flask_jwt_extended import create_access_token
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database error"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 400

        # Hash password (simple hash for demo, use bcrypt in production)
        # Using simple string for now if previously implementation was simple, 
        # but let's stick to what likely was there or a basic safe one.
        # Assuming plain text or basic hash for compatibility with previous snippets if any.
        # Let's use simple sha256 for now.
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, 'Analyst')", (name, email, hashed_pw))
        conn.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username') # Front end sends 'username'
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Allow login by name or email
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT * FROM users WHERE (email = %s OR name = %s) AND password_hash = %s"
        cursor.execute(query, (username_or_email, username_or_email, hashed_pw))
        user = cursor.fetchone()

        if user:
            access_token = create_access_token(identity=user['id'])
            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "name": user['name'],
                    "email": user['email'],
                    "role": user['role']
                }
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        conn.close()
