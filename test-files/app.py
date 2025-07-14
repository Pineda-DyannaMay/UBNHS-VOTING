from flask import Blueprint, render_template
from models import db, Candidate  # Ensure db is imported from models
from flask_login import login_required  # Ensure login_required is imported

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='Templates')

@dashboard_bp.route('/home')
@login_required
def dashboard():
    # Fetch the vote counts for each committee
    committees = Candidate.query.with_entities(Candidate.committee, db.func.sum(Candidate.votes).label('total_votes'))\
        .group_by(Candidate.committee).all()

    # Convert data into a format suitable for chart.js
    committee_names = [committee.committee for committee in committees]
    vote_counts = [committee.total_votes for committee in committees]

    return render_template('Admin Dashboard.html', committees=committee_names, votes=vote_counts)

@dashboard_bp.route('/summary')
def summary():
    results = Candidate.query.order_by(Candidate.votes.desc()).all()
    return render_template('summary.html', results=results)