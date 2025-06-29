
from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename
from pdf2docx import Converter

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if not filename.endswith('.pdf'):
        return {'error': 'Only PDF files are allowed'}, 400

    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(pdf_path)

    word_filename = filename.replace('.pdf', '.docx')
    word_path = os.path.join(OUTPUT_FOLDER, word_filename)

    try:
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()
    except Exception as e:
        return {'error': f'Conversion failed: {str(e)}'}, 500

    return send_file(word_path, as_attachment=True, download_name=word_filename)

if __name__ == '__main__':
    app.run(debug=True)
