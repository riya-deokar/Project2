from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
api = Api(app)

# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/path/to/uploaded/files'  # Update this path

db = SQLAlchemy(app)

# Define your Document model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # Add other fields as necessary

# Define your AnalysisResult model
class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    keywords = db.Column(db.Text)
    sentiment = db.Column(db.String(50))
    # Add other fields as necessary
    document = db.relationship('Document', backref=db.backref('analysis_results', lazy=True))

# Define your DocumentUpload resource
class DocumentUpload(Resource):
    def post(self):
        # Check if the post request has the file part
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Create a new Document instance and save to database
            new_doc = Document(filename=filename)
            db.session.add(new_doc)
            db.session.commit()
            return {'message': 'File uploaded successfully', 'documentId': new_doc.id}, 201

# Define your DocumentList resource
class DocumentList(Resource):
    def get(self):
        documents = Document.query.all()
        return [{'id': doc.id, 'filename': doc.filename, 'upload_date': doc.upload_date.isoformat()} for doc in documents], 200

# Add resources to API
api.add_resource(DocumentUpload, '/upload')
api.add_resource(DocumentList, '/documents')

if __name__ == '__main__':
    db.create_all()  # Creates database tables
    app.run(debug=True)