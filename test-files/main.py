import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from models import db, Student #import db from models
from home import home_bp
from login import auth_bp, login_manager
from app import dashboard_bp
from about_us import about_bp
from candidate import candidate_bp
from voters import voters_bp
from voting import voting_bp
from csv_upload import csv_upload_bp
from generate_qr import generate_qr_bp
from voting_ended import voting_ended_bp
from flask import send_from_directory
from flask_cors import CORS
from qr_scan import qr_scan_bp


app = Flask(__name__)
app.secret_key = 'your_secret_key'

CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000"], methods=["GET", "POST", "OPTIONS"]) # Allow all origins, or customize as needed


# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/Yllamor Lagan/Dropbox/PC/Downloads/test-files/pupt_elexpress.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/pupt_elexpress'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid overhead
app.config['SESSION_COOKIE_NAME'] = 'voting_session'
app.config['SQLALCHEMY_ECHO'] = True  # Log SQL queries

# Initialize the database with the app
db.init_app(app)

# Initialize Migrate
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager.init_app(app)

# Define the upload folder path (ensure this folder exists)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Set configuration on the app
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set the upload folder here

#edit this file path according to your file directory
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Yllamor Lagan\\Dropbox\\PC\\Downloads\\test-files\\uploads' 


app.config['WTF_CSRF_ENABLED'] = False



# Register Blueprints
app.register_blueprint(home_bp, url_prefix='/')  # Home Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')  # Auth Blueprint
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # Dashboard route
app.register_blueprint(about_bp, url_prefix='/about')  # About Us Blueprint
app.register_blueprint(candidate_bp, url_prefix='/candidate')  # Candidate Blueprint
app.register_blueprint(voters_bp, url_prefix='/voters')
app.register_blueprint(csv_upload_bp, url_prefix='/voters')
app.register_blueprint(generate_qr_bp, url_prefix='/voters')
app.register_blueprint(voting_bp, url_prefix='/voting')
app.register_blueprint(qr_scan_bp, url_prefix='/student_page')
app.register_blueprint(voting_ended_bp, url_prefix='/voting_ended')


@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.before_request
def handle_preflight():
    # Handle OPTIONS requests
    if request.method == 'OPTIONS':
        return '', 200

if __name__ == '__main__':
    app.run(debug=True)
