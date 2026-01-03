from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Import blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.user_routes import user_bp
from backend.routes.profile_routes import profile_routes

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

# Serve Static Files (Frontend)
# Assuming 'web' is at the same level as 'backend'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, '..', 'web')

app.register_blueprint(profile_routes)


@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(WEB_DIR, 'public'), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Check if path exists in web folder directly
    if os.path.exists(os.path.join(WEB_DIR, path)):
        return send_from_directory(WEB_DIR, path)
    # Check public folder
    elif os.path.exists(os.path.join(WEB_DIR, 'public', path)):
        return send_from_directory(os.path.join(WEB_DIR, 'public'), path)
    # Check pages folder
    elif os.path.exists(os.path.join(WEB_DIR, 'pages', path)):
        return send_from_directory(os.path.join(WEB_DIR, 'pages'), path)
    # Check assets folder
    elif os.path.exists(os.path.join(WEB_DIR, 'assets', path)):
        return send_from_directory(os.path.join(WEB_DIR, 'assets'), path)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
