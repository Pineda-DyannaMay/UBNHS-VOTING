from flask import Blueprint, render_template

# Define the blueprint for the home module
home_bp = Blueprint('home', __name__, template_folder='Templates')

@home_bp.route("/")
def home():
    return render_template("Home Page.html")

@home_bp.route("/student_page", methods=["GET", "POST"])
def student_page():
    return render_template("Student QR Scanner.html")

@home_bp.route("/admin_page", methods=["GET", "POST"])
def admin_page():
    return render_template("Admin Login.html")

if __name__ == '__main__':
    app.run(debug=True)