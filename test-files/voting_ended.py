from flask import Blueprint, render_template

# Update the Blueprint to include a unique prefix for voting_ended
voting_ended_bp = Blueprint('voting_ended', __name__, template_folder='Templates')

@voting_ended_bp.route('/voting_ended', methods=['GET', 'POST'])
def home():
    return render_template("voting_ended.html")
