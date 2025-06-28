from flask import Flask, request, render_template, send_from_directory
import os
from pdf2docx import Converter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def convert_pdf():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['pdf_file']
        if file.filename == '':
            return 'No file selected', 400
        
        if file and file.filename.endswith('.pdf'):
            # Save PDF
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)
            
            # Convert to Word
            word_filename = file.filename.replace('.pdf', '.docx')
            word_path = os.path.join(app.config['DOWNLOAD_FOLDER'], word_filename)
            
            cv = Converter(pdf_path)
            cv.convert(word_path)
            cv.close()
            
            return render_template('download.html', filename=word_filename)
    
    return 'Invalid request', 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)