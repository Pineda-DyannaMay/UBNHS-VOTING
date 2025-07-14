import os
import qrcode
from flask import Blueprint, current_app, flash, redirect, url_for
from models import db, Student  # Import db and Student model from models

generate_qr_bp = Blueprint('generate_qr_bp', __name__)

def generate_qr_codes():
    try:
        # Ensure the 'qrcodes' directory exists (recreate if missing)
        if not os.path.exists('qrcodes'):
            os.makedirs('qrcodes')

        # Fetch all students from the database
        students = Student.query.all()
        
        if not students:
            print("No students found in the database.")
            return

        for student in students:
            # Create a string with non-sensitive information for the QR code
            qr_data = f"{student.unique_code}"

            # Check if the QR code for the student already exists
            if not os.path.exists(f'qrcodes/{student.student_number}.png'):
                try:
                    # Generate the QR code using student information
                    qr = qrcode.make(qr_data)
                    # Save the QR code with student_number as the filename
                    qr.save(f'qrcodes/{student.student_number}.png')
                    flash(f"Generated QR code for student {student.student_number}", "success")
                except Exception as e:
                    flash(f"Failed to generate QR code for student {student.student_number}: {e}", "danger")
                    continue  # Skip this student if QR generation fails
            else:
                flash(f"QR code for student {student.student_number} already exists.", "info")
                
        flash("QR codes generation completed.", "success")
    except Exception as e:
        flash(f"Error generating QR codes: {e}", "danger")

    return redirect(url_for('voters_bp.voters'))  # Redirect back to the voters page after operation
