from queue import Queue
import threading
from flask import current_app, jsonify  # Import Flask utilities for context and responses

# Initialize queues
pdf_analysis_queue = Queue()
nlp_analysis_queue = Queue()

def pdf_analysis_worker(app):
    with app.app_context():  # Required to allow Flask context (e.g., database access) within threads
        while True:
            task = pdf_analysis_queue.get()
            try:
                # Assuming extract_text_from_file and analyze_sentiment are in main.py
                # Import here to avoid circular imports
                from main import extract_text_from_file, analyze_sentiment
                
                filepath, file_extension = task['filepath'], task['file_extension']
                text = extract_text_from_file(filepath, file_extension)
                sentiment = analyze_sentiment(text)
                
                # Here, you would typically update a database record with the results
                # For demonstration, we'll just print the results
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
                # Importing here as well to avoid circular imports
                from main import analyze_sentiment
                
                text = task['text']
                sentiment = analyze_sentiment(text)
                
                # Similarly, handle the result of NLP analysis
                print(f'Analyzed text sentiment: {sentiment}')
                
            except Exception as e:
                current_app.logger.error(f'Error analyzing text: {e}')
            finally:
                nlp_analysis_queue.task_done()

def start_workers(app):
    # Start PDF analysis worker threads
    for _ in range(2):  # Adjust number based on expected workload
        thread = threading.Thread(target=pdf_analysis_worker, args=(app,))
        thread.daemon = True  # Allows thread to exit when main thread exits
        thread.start()
    
    # Start NLP analysis worker threads
    for _ in range(2):  # Similarly, adjust number as needed
        thread = threading.Thread(target=nlp_analysis_worker, args=(app,))
        thread.daemon = True
        thread.start()
