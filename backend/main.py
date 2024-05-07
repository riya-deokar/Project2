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
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
import spacy
from search import search_wikipedia, search_nytimes

app = Flask(__name__)
CORS(app)  # Apply CORS to your app

# Configuration
app.config['JWT_SECRET_KEY'] = 'lia321ava'  # Set your JWT Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db.init_app(app)
migrate = Migrate(app, db)  # Flask-Migrate
jwt = JWTManager(app)  # Flask-JWT-Extended

# Register Flask blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

nlp = spacy.load('en_core_web_sm')

def extract_text_from_file(filepath, file_extension):
    text = ""
    if file_extension == 'pdf':
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
    elif file_extension in ['png', 'jpg', 'jpeg']:
        # Use pytesseract directly for better control and error handling
        try:
            text = pytesseract.image_to_string(Image.open(filepath), lang='eng')
        except Exception as e:
            logging.error(f"OCR processing failed: {e}")
            return '', str(e)  # Return error as string for better handling
    elif file_extension in ['txt', 'csv']:  # Plain text or CSV files
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
    elif file_extension == 'docx':
        try:
            text = textract.process(filepath, extension='docx').decode('utf-8')
        except Exception as e:
            logging.error(f"Error processing DOCX file: {e}")
            return '', str(e)  # Return error as string for better handling
    return text, ''  # Return text and empty string for error if successful

def extract_keywords(text):
    doc = nlp(text)

    # Only keep entities with specific labels
    desired_entity_types = {'PERSON', 'ORG', 'GPE'}
    keywords = [ent.text for ent in doc.ents if ent.label_ in desired_entity_types]

    # Optional: Additional filtering or transformations can be added here

    return keywords[:15]  # Limit to top 15 keywords

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
            text, error = extract_text_from_file(filepath, file_extension)

            if error:
                return jsonify({'error': 'OCR processing failed', 'details': error}), 500
            if text:
                sentiment = analyze_sentiment(text)
                keywords = extract_keywords(text)  # Extract keywords
                return jsonify({
                    'message': 'File processed successfully',
                    'text': text,
                    'sentiment': sentiment,
                    'keywords': keywords  # Include keywords in response
                })
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
    keywords = extract_keywords(text)  # Extract keywords
    return jsonify({'sentiment': sentiment, 'keywords': keywords})  # Include keywords in response

def analyze_document(text):
    sentiment = analyze_sentiment(text)  # Assuming you already have this function
    keywords = extract_keywords(text)
    return {
        'text': text,
        'sentiment': sentiment,
        'keywords': keywords
    }

# Searching Keywords
@app.route('/api/search/wikipedia', methods=['GET'])
def search_wiki():
    keyword = request.args.get('keyword')
    result = search_wikipedia(keyword)
    return jsonify({'result': result})

@app.route('/api/search/nytimes', methods=['GET'])
def search_nyt():
    keyword = request.args.get('keyword')
    result = search_nytimes(keyword)
    return jsonify({'result': result})

if __name__ == '__main__':
    # Ensure database tables are created and run the Flask application
    with app.app_context():
        db.create_all()
        start_workers(app) # Pass the Flask app to the worker starter function
    app.run(debug=True, port=5001)