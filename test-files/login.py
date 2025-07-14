from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from models import User

# Blueprint setup
auth_bp = Blueprint('auth_bp', __name__, template_folder='Templates')
login_manager = LoginManager()

# Define a simple User class for login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# In-memory user store
users = {
    'admin': User(id=1, username='admin', password=generate_password_hash('password123'))
}

@login_manager.user_loader
def load_user(user_id):
    # Fetch user by ID (in a real app, query the database)
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard_bp.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('Admin Login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'  # Redirect if not logged in

# class StudentLogin(UserMixin):
#     def __init__(self, student):
#         self.id = student.id
#         self.name = student.name
#         self.student_number = student.student_number

# @login_manager.user_loader
# def load_user(student_id):
#     from models import Student
#     return Student.query.get(int(student_id))

