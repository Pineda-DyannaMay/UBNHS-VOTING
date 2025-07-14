import os
import base64
import cv2
import numpy as np
from flask import Blueprint, Flask, jsonify, request, render_template, redirect, url_for
from models import db, Student  # Import your database models
import json  # For handling JSON-encoded QR codes
import subprocess 

# Initialize the camera
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

# Create a Blueprint instead of an app
qr_scan_bp = Blueprint('qr_scan_bp', __name__, template_folder='Templates')


@qr_scan_bp.route('/student_page')

def student_page():
    return render_template('Student QR Scanner.html')


# Route for decoding QR codes from uploaded images
@qr_scan_bp.route('/decode_qr', methods=['POST'])
def decode_qr():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    try:
        img_data = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None and data:
            student = Student.query.filter_by(unique_code=data).first()
            if student:
                return jsonify({'qr_code_data': data, 'redirect': '/voting'})
            else:
                return jsonify({'error': 'QR code not found in the database'}), 404
        else:
            return jsonify({'error': 'No QR code found'}), 404

    except Exception as e:
        return jsonify({'error': f'Error decoding image: {str(e)}'}), 500


# Route to handle live camera-based QR code scanning
@qr_scan_bp.route('/live_qr_scan')
def live_qr_scan():
    try:
        # Initialize the camera
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        print("Starting live QR code scanning. Press 'q' to exit.")
        while True:
            ret, img = cap.read()
            if not ret:
                print("Failed to capture image. Exiting...")
                break

            data, bbox, _ = detector.detectAndDecode(img)

            # If a QR code is detected
            if bbox is not None:
                for i in range(len(bbox)):
                    point1 = tuple(map(int, bbox[i][0]))
                    point2 = tuple(map(int, bbox[(i + 1) % len(bbox)][0]))
                    cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)

                if data:
                    print("[+] QR Code detected, data:", data)
                    student = Student.query.filter_by(unique_code=data).first()
                    if student:
                        print(f"Student Found: {student.name}")
                        cap.release()
                        cv2.destroyAllWindows()
                        return redirect(url_for('qr_scan_bp.student_page'))
                    else:
                        print("QR Code not found in the database.")

            # Display the camera feed
            cv2.imshow("Live QR Code Scanner", img)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        return "Live scan ended. No QR code matched.", 200

    except Exception as e:
        print(f"Error during live scanning: {str(e)}")
        return f"Error during live scanning: {str(e)}", 500


# Route for QR code uploads
@qr_scan_bp.route('/upload_qr_image', methods=['POST'])
def upload_qr_image():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    try:
        img_data = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None and data:
            student = Student.query.filter_by(unique_code=data).first()
            if student:
                return jsonify({'qr_code_data': data, 'redirect': '/voting_page'})
            else:
                return jsonify({'error': 'Student not found in the database'}), 404
        else:
            return jsonify({'error': 'No QR code found'}), 404

    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
@qr_scan_bp.route('/start_live_scan')
def start_live_scan():
    try:
        # Start the live scanner script
        subprocess.Popen(['python', 'live_qr_scanner.py'])
        return "Live QR Scanner started. Check the scanner window.", 200
    except Exception as e:
        return f"Error starting live QR Scanner: {str(e)}", 500

@qr_scan_bp.route('/validate_qr', methods=['POST'])
def validate_qr():
    qr_data = request.json.get('qr_data')
    
    if not qr_data:
        return jsonify({'error': 'No QR data provided'}), 400

    try:
        student = Student.query.filter_by(unique_code=qr_data).first()
        if student:
            # Validation success, return redirect response
            return redirect(url_for('voting_bp.voting'))  # Correct redirect to voting page
        else:
            return jsonify({"status": "failed", "message": "QR code not found in database"}), 404
    except Exception as e:
        return jsonify({'error': f'Error validating QR code: {str(e)}'}), 500

    
@qr_scan_bp.route('/voting_bp/voting')
def voting():
    # This is where the user will be redirected after successful QR scan
    return render_template("Voting Page.html")  # Render the actual voting page template

