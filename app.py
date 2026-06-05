from flask import Flask, render_template, jsonify
from flasgger import Swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth_routes import auth_bp
from goals_routes import goals_bp
from preferences_routes import preferences_bp
from device_routes import device_bp
from ai_routes import ai_bp
from nutrition_routes import nutrition_bp
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)
CORS(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = app.config['JWT_SECRET_KEY']
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app)

# JWT Error Handlers
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token is missing'}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize Swagger
swagger = Swagger(app, config={
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
},
template={
    "swagger": "2.0",
    "info": {
        "title": "Nourical API",
        "version": "1.0.0",
        "description": "API for Nourical nutrition platform"
    },
    "basePath": "/",
    "schemes": ["http", "https"] if app.config['ENV'] =='local' else ["https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Paste your token below. You can enter just the token OR 'Bearer <token>' — both work."
        }
    }
})
# print(app.config['DEBUG'])
# print('oke...',["http", "https"] if app.config['DEBUG'] else ["https"])

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(preferences_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(device_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(nutrition_bp)

# Create tables
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"[DB] Could not create tables: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Serve static images for email templates
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    from flask import send_from_directory
    return send_from_directory('static/images', filename)

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
