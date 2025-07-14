from flask import Blueprint, render_template
from flask_login import login_required

# Create the about blueprint
about_bp = Blueprint('about_bp', __name__, template_folder='Templates')

# Define the route for the about page
@about_bp.route('/about')
@login_required
def about():
    return render_template('About Us.html')

