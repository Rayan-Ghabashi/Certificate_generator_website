from flask import Flask, request, send_file, redirect, url_for, render_template, flash
import os
from werkzeug.utils import secure_filename
import logging
import pandas as pd
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import arabic_reshaper
from bidi.algorithm import get_display
from pdf_certificate_generator import create_certificate
from configuration import fontpath
import zipfile
import atexit
import signal
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit the maximum file size to 16MB
app.secret_key = 'supersecretkey'  # Needed for flashing messages

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    logging.debug('Received request to upload CSV')
    if 'csv' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['csv']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('CSV file successfully uploaded')
        return redirect(url_for('index'))
    flash('File type not allowed')
    return redirect(request.url)




@app.route('/upload_template', methods=['POST'])
def upload_template():
    logging.debug('Received request to upload template')
    if 'template' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['template']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('Template file successfully uploaded')
        return redirect(url_for('index'))
    flash('File type not allowed')
    return redirect(request.url)




@app.route('/download_file', methods=['POST'])
def download_file():
    
    csv = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.csv')]
    template = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.pdf')]

    if not csv and not template:
        flash('Both CSV and template files must be uploaded',category='error')
        return redirect(url_for('index'))
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv[-1])
    template_path = os.path.join(app.config['UPLOAD_FOLDER'], template[-1])

        
        # Process the files and generate the certificate
    certificate_path = certificate_generator(csv_path, template_path)
    zip_folder(certificate_path,'output.zip')

    return send_file('output.zip', as_attachment=True)
    
    

def certificate_generator(csv_file, template_file):
    
    pdfmetrics.registerFont(TTFont('NotoSansArabic', fontpath))
    df = pd.read_csv(csv_file)
    template_file_path = os.path.join(template_file)
    for index, row in df.iterrows():
        display_name = row['Name']
        name =''
        if(check_name_language(display_name)=='Arabic'):
            reshaped_text = arabic_reshaper.reshape(display_name)  # Reshape if Arabic
            name = get_display(reshaped_text)
            fontname = 'NotoSansArabic'
        else:
            name = display_name
            fontname = 'Times-BoldItalic'
        
        output_path =f"Generated_certificates/certificate_{display_name}.pdf"
        create_certificate(name,template_file_path,output_path,fontname)

    return 'Generated_certificates'
def check_name_language(name):
    arabic_count = sum(1 for char in name if '\u0600' <= char <= '\u06FF')
    english_count = sum(1 for char in name if 'A' <= char <= 'Z' or 'a' <= char <= 'z')
    
    if arabic_count > english_count:
        return "Arabic"
    elif english_count > arabic_count:
        return "English"
    
def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
def cleanup():
    print('Cleaning up...')
    # Remove the uploads directory and its contents
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    # Recreate the directory for future uploads
    if(os.path.exists('Generated_certificates')):
        shutil.rmtree('Generated_certificates')
    if(os.path.exists('output.zip')):
        os.remove('output.zip')
    print('Cleanup complete.')

# Register the cleanup function to be called on exit
atexit.register(cleanup)

# Register signal handlers for SIGINT and SIGTERM
def handle_signal(signum, frame):
    cleanup()
    exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('Generated_certificates', exist_ok=True)
    app.run(debug=True)
