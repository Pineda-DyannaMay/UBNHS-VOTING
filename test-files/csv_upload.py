import os
import random
import string
from flask import Blueprint, request, render_template, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
import csv
from models import db, Student  # Assuming your model is in the 'models.py' file
import hashlib
from flask import jsonify

csv_upload_bp = Blueprint('csv_upload', __name__)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_salt(length=16):
    """Generates a random salt."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@csv_upload_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        flash("No file part. Please select a file to upload.", "danger")
        return redirect(url_for('voters_bp.voters'))  # Adjust route as needed
    
    file = request.files['file'] 
    if file and allowed_file(file.filename):
        try:
            # Access the app's config for the upload folder
            upload_folder = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            # Process the CSV file
            with open(file_path, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if len(row) == 5:
                        student_number, name, year_level, precinct_number, email = row
                        salt = generate_salt()
                        unique_code = hashlib.sha256((student_number + salt).encode()).hexdigest()

                        student = Student(
                            student_number=student_number,
                            name=name,
                            year_level=year_level,
                            precinct_number=precinct_number,
                            email=email,
                            unique_code=unique_code
                        )
                        db.session.add(student)
                        db.session.commit()
                    else:
                        print(f"Skipping row with incorrect number of columns: {row}")

            flash("File uploaded and processed successfully!", "success")
            return redirect(url_for('voters_bp.voters'))  # Adjust route as needed
        except Exception as e:
            flash(f"An error occurred while processing the file: {e}", "danger")
            return redirect(url_for('voters_bp.voters'))  # Adjust route as needed
    else:
        flash("Invalid file type. Please upload a .csv file.", "danger")
        return redirect(url_for('voters_bp.voters'))  # Adjust route as needed
