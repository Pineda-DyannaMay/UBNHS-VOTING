import os
import cv2
import time
import webbrowser
from models import db, Student
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/pupt_elexpress'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid overhead
app.config['SESSION_COOKIE_NAME'] = 'voting_session'
app.config['SQLALCHEMY_ECHO'] = True  # Log SQL queries

# Initialize the database with the app
db.init_app(app)

# Initialize the camera
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

print("Live QR scanner started. Press 'q' to exit.")

# Wrap the whole QR scanner process in the app context
with app.app_context():
    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to capture image. Exiting...")
            break

        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None:
            for i in range(len(bbox)):
                point1 = tuple(map(int, bbox[i][0]))
                point2 = tuple(map(int, bbox[(i + 1) % len(bbox)][0]))
                cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)

            if data:
                print("[+] QR Code detected:", data)
                # Query the database directly within app context
                student = db.session.query(Student).filter_by(unique_code=data).first()

            if Student:
                print(f"Student Found: {Student.name}")
                qr_code_detected = True
                print("Redirecting to voting page...")
                webbrowser.open('http://127.0.0.1:5000/voting/voting')
                break
                # Avoid making any changes unless you commit explicitly
                # If you are not changing anything, don't call db.session.commit()
            else:
                print("QR Code not found in the database.")

        cv2.imshow("Live QR Scanner", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
