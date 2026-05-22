from flask import Flask, render_template
from flasgger import Swagger
from flask_cors import CORS
from config import Config
from models import db
from auth_routes import auth_bp
from goals_routes import goals_bp
from preferences_routes import preferences_bp

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)
CORS(app)

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
    "schemes": ["http", "https"] if app.config['DEBUG'] else ["https"],
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

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(preferences_bp)
app.register_blueprint(goals_bp)

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
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
