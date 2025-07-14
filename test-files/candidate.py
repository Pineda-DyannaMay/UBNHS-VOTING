import os
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from flask_login import login_required
from models import db, Candidate, VotingTime
from datetime import datetime
from werkzeug.utils import secure_filename
import traceback


# Allowed file types
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the candidate blueprint
candidate_bp = Blueprint('candidate_bp', __name__, template_folder='Templates')

@candidate_bp.route('/candidate')
@login_required
def candidate():
    candidates = Candidate.query.all()
    voting_time = VotingTime.query.first()  # Get the current voting configuration
    return render_template('Candidates Page.html', candidates=candidates, voting_end_time=voting_time.voting_end_time if voting_time else None)

@candidate_bp.route('/add_candidate', methods=['POST'])
def add_candidate():
    if 'candidate_pic' not in request.files:
        flash("No picture uploaded. Please choose a file.", "danger")
        return redirect(url_for('candidate_bp.add_candidate'))

    file = request.files['candidate_pic']
    if file and allowed_file(file.filename):  # Check if file is valid (e.g., image)
        filename = secure_filename(file.filename)  # Sanitize filename
        upload_folder = current_app.config['UPLOAD_FOLDER']  # Access app's config for UPLOAD_FOLDER
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)  # Save image

        # Create a new Candidate object and add to the database
        new_candidate = Candidate(
            committee=request.form['committee'],
            name=request.form['candidate_name'],
            picture=filename  # Save the file name in the database
        )

        print(f"Upload folder: {current_app.config['UPLOAD_FOLDER']}")
        print(f"Saving to: {file_path}")

        try:
            db.session.add(new_candidate)
            db.session.commit()
            flash("Candidate added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback if something goes wrong
            flash(f"Error adding candidate: {e}", "danger")
            print(f"Error: {e}")
    else:
        flash("Invalid file type. Please upload a valid image.", "danger")

    return redirect(url_for('candidate_bp.candidate'))


@candidate_bp.route('/delete_candidate/<int:candidate_id>', methods=['POST'])
@login_required
def delete_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    flash('Candidate deleted successfully!')
    return redirect(url_for('candidate_bp.candidate'))

"""@candidate_bp.route('/set_voting_duration', methods=['POST'])
def set_voting_duration():
    # Get the end time from the form
    end_time = request.form.get('voting_end_time')
    print(f"Received end_time: {end_time}")  # Debugging line

    if not end_time:
        flash('Please select a valid date and time.', 'danger')
        return redirect(url_for('candidate_bp.candidate'))

    try:
        # Ensure the input is in the correct format, add ':00' for seconds if necessary
        if len(end_time) == 16:  # Format like '2025-01-04 19:59'
            end_time += ":00"  # Add seconds to match 'YYYY-MM-DD HH:mm:ss'

        # Convert the adjusted end time to a datetime object
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        print(f"Parsed end time: {end_time}")

        # Check if there is already a voting configuration or create a new one
        voting_config = VotingTime.query.first()
        if not voting_config:
            print("No existing voting configuration found. Creating a new one.")
            # Create a new VotingTime object and store it in the database
            voting_config = VotingTime(voting_end_time=end_time)  # Create a new record with the end time
            db.session.add(voting_config)  # Add the new object to the session
        else:
            print(f"Found existing voting configuration: {voting_config.voting_end_time}. Updating to {end_time}.")
            # Update the existing voting configuration's end time
            voting_config.voting_end_time = end_time

        # Commit the changes to the database
        db.session.commit()  # Commit the transaction to the database
        print("Commit successful")
        flash('Voting duration set successfully!', 'success')

        # Convert datetime to string for frontend
        # Ensure the format matches the expected input for datetime-local
        formatted_end_time = voting_config.voting_end_time.strftime('%Y-%m-%dT%H:%M')

    except Exception as e:
        db.session.rollback()  # Rollback if something goes wrong
        flash(f'Error setting voting duration: {e}', 'danger')
        print(f"Error: {traceback.format_exc()}")  # Print detailed error message
        formatted_end_time = None  # If error, no end time to display

    return redirect(url_for('candidate_bp.candidate', voting_end_time=formatted_end_time))"""

@candidate_bp.route('/set_voting_duration', methods=['POST'])
def set_voting_duration():
    voting_end_time_str = request.form.get('voting_end_time')
    # Ensure the received time is in correct datetime format
    try:
        # Convert the string received from the form to a datetime object
        voting_end_time = datetime.strptime(voting_end_time_str, '%Y-%m-%dT%H:%M')
        print(f"Voting end time received: {voting_end_time}")

        # Create a new VotingTime record
        voting_time = VotingTime(voting_end_time=voting_end_time)

        # Add to the database session and commit
        db.session.add(voting_time)
        db.session.commit()
        
        flash('Voting end time set successfully!', 'success')
        
    except ValueError as e:
        # Handle invalid datetime format
        print(f"Error: {e}")
        flash('Invalid date-time format. Please try again.', 'danger')

    return redirect(url_for('candidate_bp.candidate'))  # Redirect as necessary