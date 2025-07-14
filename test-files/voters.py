from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from models import db, Student
from generate_qr import generate_qr_codes


# Create the candidate blueprint
voters_bp = Blueprint('voters_bp', __name__, template_folder='Templates')


# Route to render the voters page and display the students table
@voters_bp.route('/voters')
@login_required
def voters():
    students = Student.query.all()  # Fetch all students from the database
    return render_template('Voters Page.html', students=students)

# Route to fetch the student data for the table (AJAX call)
@voters_bp.route('/voters/students_data', methods=['GET'])
def students_data():
    students = Student.query.all()  # Fetch students from the database
    students_list = [
        {
            'student_number': student.student_number,
            'name': student.name,
            'email': student.email,
        }
        for student in students
    ]
    return jsonify(students_list)

@voters_bp.route('/edit_student/<int:student_number>', methods=['POST'])
def edit_student(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if student:
        # Update student details
        student.name = request.form['name']
        student.email = request.form['email']
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Student not found"}), 404

@voters_bp.route('/delete_student/<int:student_number>', methods=['POST'])
def delete_student(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Student not found"}), 404

@voters_bp.route('/voters/generate_qr', methods=['POST'])
@login_required
def generate_qr():
    try:
        generate_qr_codes()  # This will generate and save the QR codes
        flash("QR codes generated successfully!", "success")  # Success message
    except Exception as e:
        flash(f"Failed to generate QR codes: {e}", "danger")  # Error message
    
    return redirect(url_for('voters_bp.voters'))  # Redirect back to the voters page