from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # CORS support
import fitz  # PyMuPDF
import textract
import os
import logging
from app.models import db
from app.sentiment_analysis import analyze_sentiment
from app.auth import auth_blueprint
from app.utils.queue_utils import start_workers

app = Flask(__name__)
CORS(app)  # Apply CORS to your app

# Configuration
app.config['JWT_SECRET_KEY'] = 'lia321ava'  # Set your JWT Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
#db = SQLAlchemy(app)  # SQLAlchemy
db.init_app(app)

migrate = Migrate(app, db)  # Flask-Migrate
jwt = JWTManager(app)  # Flask-JWT-Extended

# Register Flask blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

def extract_text_from_file(filepath, file_extension):
    # Extract text based on file extension
    text = ""
    if file_extension == 'pdf':
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
    elif file_extension in ['png', 'jpg', 'jpeg']:  # Example for image files
        text = textract.process(filepath, method='tesseract', language='eng').decode()
    elif file_extension in ['txt', 'csv']:  # Plain text or CSV files
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
    elif file_extension == 'docx':
        text = textract.process(filepath, extension='docx').decode()
    # Add more conditions for other file types if necessary
    return text

# Constants for allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'txt', 'csv'}

logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API'S
# Secure File Uploader/Ingester
@app.route('/api/upload/', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('/tmp', filename)
            file.save(filepath)
            
            file_extension = filename.rsplit('.', 1)[1].lower()
            text = extract_text_from_file(filepath, file_extension)
            if text:
                sentiment = analyze_sentiment(text)
                return jsonify({'message': 'File processed successfully', 'text': text, 'sentiment': sentiment})
            else:
                return jsonify({'error': 'Could not extract text from file'}), 400
        else:
            return jsonify({'error': 'Unsupported file type or invalid file'}), 400
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return jsonify({'error': 'An error occurred while processing the file'}), 500

# Text NLP Analysis
@app.route('/api/analyze/', methods=['POST'])
def analyze_document():
    text = request.json.get('text', '')
    sentiment = analyze_sentiment(text)
    return jsonify({'sentiment': sentiment})


# FUNCTION STUBS FOR UNHIGHLIGHTED API'S
# Feed Ingester
@app.route('/api/ingest/', methods=['POST'])
def ingest_feed():
    # Placeholder for feed ingestion logic
    # You could process RSS feeds, social media streams, etc.
    return jsonify({'message': 'Feed ingestion logic not yet implemented'}), 501

# Output Generator
@app.route('/api/generate/', methods=['GET'])
def generate_output():
    # Placeholder for output generation logic
    # You could generate reports, summaries, visualizations, etc.
    return jsonify({'message': 'Output generation logic not yet implemented'}), 501


if __name__ == '__main__':
    # Ensure database tables are created and run the Flask application
    with app.app_context():
        db.create_all()
        start_workers(app) # Pass the Flask app to the worker starter function
    app.run(debug=True, port=5001)