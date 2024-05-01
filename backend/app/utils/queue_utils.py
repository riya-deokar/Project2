from queue import Queue
import threading
from flask import current_app, jsonify
import bleach
import re

# Initialize queues
pdf_analysis_queue = Queue()
nlp_analysis_queue = Queue()

def sanitize_input(data):
    """Sanitize input data to prevent injection attacks."""
    if isinstance(data, dict):
        return {key: bleach.clean(str(value)) for key, value in data.items()}
    return data

def validate_filepath(filepath, extension):
    """Validate the file path and extension for allowed formats."""
    valid_extensions = ['pdf', 'txt']
    if not re.match(r'^[\w,.\s-]+$', filepath) or extension not in valid_extensions:
        raise ValueError("Invalid file path or file type")

def add_to_pdf_analysis_queue(task):
    """Add tasks to PDF analysis queue after sanitizing."""
    sanitized_task = sanitize_input(task)
    pdf_analysis_queue.put(sanitized_task)

def add_to_nlp_analysis_queue(task):
    """Add tasks to NLP analysis queue after sanitizing."""
    sanitized_task = sanitize_input(task)
    nlp_analysis_queue.put(sanitized_task)

def pdf_analysis_worker(app):
    with app.app_context():  # Required for Flask context within threads
        while True:
            task = pdf_analysis_queue.get()
            try:
                # Sanitization and validation at the point of processing
                validate_filepath(task['filepath'], task['file_extension'])
                
                from main import extract_text_from_file, analyze_sentiment
                filepath, file_extension = task['filepath'], task['file_extension']
                text = extract_text_from_file(filepath, file_extension)
                sentiment = analyze_sentiment(text)
                
                # Secure handling of data output
                print(f'Processed {filepath}: {sentiment}')
            except Exception as e:
                current_app.logger.error(f'Error processing file {filepath}: {e}')
            finally:
                pdf_analysis_queue.task_done()

def nlp_analysis_worker(app):
    with app.app_context():
        while True:
            task = nlp_analysis_queue.get()
            try:
                from main import analyze_sentiment
                
                text = sanitize_input(task['text'])  # Sanitize text before processing
                sentiment = analyze_sentiment(text)
                
                print(f'Analyzed text sentiment: {sentiment}')
            except Exception as e:
                current_app.logger.error(f'Error analyzing text: {e}')
            finally:
                nlp_analysis_queue.task_done()

def start_workers(app):
    # Start PDF and NLP analysis worker threads
    for _ in range(2):  # Adjust number based on expected workload
        threading.Thread(target=pdf_analysis_worker, args=(app,), daemon=True).start()
        threading.Thread(target=nlp_analysis_worker, args=(app,), daemon=True).start()