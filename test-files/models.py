from flask_sqlalchemy import SQLAlchemy
import hashlib
import uuid

db = SQLAlchemy()

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.String(50), nullable=False)
    precinct_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    unique_code = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Student {self.name}, {self.student_number}>'

    # Function to generate and hash a unique code
    @staticmethod
    def generate_unique_code():
        # Generate a random UUID and hash it
        unique_code = str(uuid.uuid4())
        hashed_code = hashlib.sha256(unique_code.encode('utf-8')).hexdigest()
        return hashed_code

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    committee = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.Integer, default=0)  # Store vote counts

    def __repr__(self):
        return f'<Candidate {self.name}, Committee: {self.committee}>'
    
class VoteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    student = db.relationship('Student', backref=db.backref('vote_logs', lazy=True))
    candidate = db.relationship('Candidate', backref=db.backref('vote_logs', lazy=True))

    def __repr__(self):
        return f'<VoteLog Student: {self.student_id}, Candidate: {self.candidate_id}>'
    
class VotingTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voting_end_time = db.Column(db.DateTime, nullable=False)


