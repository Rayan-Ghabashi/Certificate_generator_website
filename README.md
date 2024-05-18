## Flask Application README
### Overview

This is a Flask web application designed to handle the upload of CSV and PDF files, process them, and generate certificates. The certificates are created based on a given template and data provided in the CSV file. The application supports both Arabic and English languages.
### Features
- Upload CSV files containing names and other details.
- Upload PDF template files to be used for generating certificates.
- Generate certificates for each entry in the CSV file.
- Support for Arabic text rendering.
- Download all generated certificates in a ZIP file.
- Automatic cleanup of uploaded files and generated certificates upon exit.
### Requirements
- Python 3.x
- Flask
- pandas
- reportlab
- arabic_reshaper
- python-bidi
- werkzeug
### Installation 
1. **Clone the repository:** 

```bash
git clone https://github.com/your-repo/flask-certificate-generator.git
cd flask-certificate-generator
``` 
2. **Create and activate a virtual environment:** 

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
``` 
3. **Install the required packages:** 

```bash
pip install -r requirements.txt
``` 
4. **Set up the configuration:** 
Ensure you have the correct path to the font file in `configuration.py`:

```python
fontpath = 'path/to/your/font/NotoSansArabic.ttf'
```
### Usage 
1. **Run the application:** 

```bash
python app.py
``` 
2. **Open your browser and go to:** 

```
http://127.0.0.1:5000/
``` 
3. **Upload a CSV file:** 
- Click on the 'Upload CSV' button and select your CSV file. 
4. **Upload a PDF template file:** 
- Click on the 'Upload Template' button and select your PDF template file. 
5. **Generate and download certificates:** 
- Click the 'Generate Certificates' button to process the files.
- Download the ZIP file containing the generated certificates.
### Application Structure 
- **app.py** : Main application file containing route definitions and core logic. 
- **configuration.py** : Configuration file where font paths and other settings are defined. 
- **templates/** : Folder containing HTML templates for the Flask app. 
- **index.html** : Main page template. 
- **uploads/** : Directory where uploaded files are stored. 
- **Generated_certificates/** : Directory where generated certificates are stored.
### Route Endpoints 
- `/` (GET): Displays the index page with upload forms. 
- `/upload_csv` (POST): Handles CSV file uploads. 
- `/upload_template` (POST): Handles template file uploads. 
- `/download_file` (POST): Processes the CSV and template files, generates certificates, and provides a ZIP file for download.
### Functions 
- **allowed_file(filename)** : Checks if the uploaded file has an allowed extension. 
- **certificate_generator(csv_file, template_file)** : Generates certificates from the CSV data and template file. 
- **check_name_language(name)** : Determines the language of a given name (Arabic or English). 
- **zip_folder(folder_path, output_zip)** : Zips the specified folder into an output ZIP file. 
- **cleanup()** : Cleans up the uploaded files and generated certificates.
### Logging

The application logs debug messages for key actions such as file uploads and processing steps. Ensure logging is set to the desired level as needed.
### Cleanup

The application automatically cleans up uploaded files and generated certificates when it exits. This is handled through the `atexit` module and signal handlers for SIGINT and SIGTERM.
### Future Enhancements
- preview support
- setting the x and y coordinates
- Support for multiple font options.
- Improved error handling and user feedback.
- requirements.txt
### Contributing

Feel free to open issues or submit pull requests with any enhancements or bug fixes.

## Where to find me
<a href="https://www.linkedin.com/in/rayan-ghabashi" target="_blank">LinkedIn</a>
