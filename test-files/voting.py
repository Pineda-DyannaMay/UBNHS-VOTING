# voting.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Candidate, VoteLog, VotingTime
from datetime import datetime

voting_bp = Blueprint('voting_bp', __name__, template_folder='Templates')

@voting_bp.route('/voting', methods=['GET', 'POST'])
def voting():
    if request.method == 'POST':
        selected_candidates = request.form.to_dict()  # Collect selected candidates
        
        # Update the vote count in the database
        for committee, candidate_name in selected_candidates.items():
            candidate = Candidate.query.filter_by(name=candidate_name).first()
            if candidate:
                candidate.votes += 1  # Increment the vote count
                db.session.commit()  # Commit the changes to the database
        
        return redirect(url_for('voting_bp.vote_confirmation'))  # Redirect to confirmation page
    
    # Fetch candidates from the database and group them by committee
    candidates = Candidate.query.all()
    committees = {}
    for candidate in candidates:
        if candidate.committee not in committees:
            committees[candidate.committee] = []
        committees[candidate.committee].append(candidate)
    
    return render_template('Voting Page.html', candidates=committees)

@voting_bp.route('/vote_confirmation')
def vote_confirmation():
    return render_template('vote_confirmation.html')  # Create this template for confirmation

def cast_vote(student_id, candidate_id):
    # Check if the student has already voted
    existing_vote = VoteLog.query.filter_by(student_id=student_id).first()
    if existing_vote:
        raise ValueError("Student has already voted.")
    
    # Record the vote
    vote_log = VoteLog(student_id=student_id, candidate_id=candidate_id)
    db.session.add(vote_log)

    # Increment the candidate's vote count
    candidate = Candidate.query.get(candidate_id)
    candidate.votes += 1

    db.session.commit()
    
@voting_bp.route('/vote', methods=['GET', 'POST'])
def vote():
    voting_time = VotingTime.query.first()
    if voting_time and datetime.now() > voting_time.voting_end_time:
        flash('Voting has already ended.', 'danger')
        return redirect(url_for('voting_ended.html'))
    else:
        flash(f"Voting will end at {voting_time.voting_end_time}", 'info')

    
    # Proceed with the voting logic
    return render_template('Voting Page.html')# voting.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Candidate, VoteLog, VotingTime
from datetime import datetime

voting_bp = Blueprint('voting_bp', __name__, template_folder='Templates')

@voting_bp.route('/voting', methods=['GET', 'POST'])
def voting():
    # Get the VotingTime with the farthest future voting_end_time
    voting_time = VotingTime.query.order_by(VotingTime.voting_end_time.desc()).first()

    # Check if voting has ended
    if voting_time and datetime.now() > voting_time.voting_end_time:
        flash('Voting has already ended.', 'danger')
        return redirect(url_for('voting_bp.voting_ended'))  # Redirect to voting ended page
    
    # Handle voting logic if voting is still open
    if request.method == 'POST':
        selected_candidates = request.form.to_dict()  # Collect selected candidates

        # Update the vote count in the database
        for committee, candidate_name in selected_candidates.items():
            candidate = Candidate.query.filter_by(name=candidate_name).first()
            if candidate:
                candidate.votes += 1  # Increment the vote count
                db.session.commit()  # Commit the changes to the database
        
        return redirect(url_for('voting_bp.vote_confirmation'))  # Redirect to confirmation page

    # Fetch candidates from the database and group them by committee
    candidates = Candidate.query.all()
    committees = {}
    for candidate in candidates:
        if candidate.committee not in committees:
            committees[candidate.committee] = []
        committees[candidate.committee].append(candidate)
    
    return render_template('Voting Page.html', candidates=committees)

    # Fetch candidates from the database and group them by committee
    candidates = Candidate.query.all()
    committees = {}
    for candidate in candidates:
        if candidate.committee not in committees:
            committees[candidate.committee] = []
        committees[candidate.committee].append(candidate)
    
    return render_template('Voting Page.html', candidates=committees)

@voting_bp.route('/vote_confirmation')
def vote_confirmation():
    return render_template('vote_confirmation.html')  # Confirmation template

# New route for voting_ended page
@voting_bp.route('/voting_ended')
def voting_ended():
    return render_template('voting_ended.html')  # Template informing users that voting has ended

def cast_vote(student_id, candidate_id):
    # Check if the student has already voted
    existing_vote = VoteLog.query.filter_by(student_id=student_id).first()
    if existing_vote:
        raise ValueError("Student has already voted.")
    
    # Record the vote
    vote_log = VoteLog(student_id=student_id, candidate_id=candidate_id)
    db.session.add(vote_log)

    # Increment the candidate's vote count
    candidate = Candidate.query.get(candidate_id)
    candidate.votes += 1

    db.session.commit()
