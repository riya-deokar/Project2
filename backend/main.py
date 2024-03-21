from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # CORS support
import fitz  # PyMuPDF
import textract
import os

# Import your application's modules
from app.sentiment_analysis import analyze_sentiment
from app.auth import auth_blueprint

app = Flask(__name__)
CORS(app)  # Apply CORS to your app

# Configuration
app.config['JWT_SECRET_KEY'] = 'lia321ava'  # Set your JWT Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db = SQLAlchemy(app)  # SQLAlchemy
migrate = Migrate(app, db)  # Flask-Migrate
jwt = JWTManager(app)  # Flask-JWT-Extended

# Register Flask blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Constants for allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'txt', 'csv'}

def allowed_file(filename):
    """
    Check if the filename has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload/', methods=['POST'])
def upload():
    # Implement the logic for file uploading
    pass  # Replace 'pass' with actual code

@app.route('/api/analyze/', methods=['POST'])
def analyze_document():
    # Implement the logic for document analysis
    pass  # Replace 'pass' with actual code

if __name__ == '__main__':
    # Ensure database tables are created and run the Flask application
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
