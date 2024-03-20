from flask import Flask, request, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route('/api/upload/', methods=['POST'])
def upload():
    # Ensure there is a file in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400

    pdf_file = request.files['file']

    # Open the PDF file
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        # Iterate through each page and extract text
        for page in doc:
            text += page.get_text()

        print(text)  # Print the extracted text

        return jsonify({'message': 'PDF processed successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
