from flask import Flask, request, render_template, send_file, redirect, url_for
from pdf2docx import Converter
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['pdf_file']
    if file and file.filename.endswith('.pdf'):
        unique_id = str(uuid.uuid4())
        pdf_filename = unique_id + '.pdf'
        docx_filename = unique_id + '.docx'

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        docx_path = os.path.join(app.config['OUTPUT_FOLDER'], docx_filename)

        file.save(pdf_path)

        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        return render_template("download.html", filename=docx_filename)
    else:
        return "Only PDF files are allowed."

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
