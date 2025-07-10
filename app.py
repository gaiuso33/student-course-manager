from flask import Flask, render_template, send_file,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from forms import StudentForm, LoginForm
import pandas as pd
from io import BytesIO
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


# SQLite DB config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ Models ------------------

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    matric_no = db.Column(db.String(50), unique=True, nullable=False)
    courses = db.relationship('CourseGrade', backref='student', lazy=True)

class CourseGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(50), nullable=False)  # e.g., "2024/2025 - First"
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'student'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Create the database tables
with app.app_context():
    db.create_all()
# Create an admin user if it doesn't exist
with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

# ------------------ helper functions ------------------

def calculate_gpa(courses):
    total_points = 0
    total_courses = len(courses)
    if total_courses == 0:
        return 0.0

    for course in courses:
        score = course.score
        if score >= 70:
            points = 4.0
        elif score >= 60:
            points = 3.0
        elif score >= 50:
            points = 2.0
        elif score >= 45:
            points = 1.0
        else:
            points = 0.0
        total_points += points

    return round(total_points / total_courses, 2)

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    # Optionally restrict to admin only
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    form = StudentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(matric_no=form.matric_no.data).first()
        if not student:
            student = Student(name=form.name.data, matric_no=form.matric_no.data)
            db.session.add(student)
            db.session.commit()

        grade = CourseGrade(
            course_name=form.course_name.data,
            score=form.score.data,
            semester=form.semester.data,
            student_id=student.id
        )
        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_student.html', form=form)

@app.route('/students')
@login_required
def list_students():
    students = Student.query.all()
    student_data = []

    for student in students:
        # Group courses by semester
        semesters = {}
        for course in student.courses:
            semesters.setdefault(course.semester, []).append(course)

        # Calculate GPA per semester
        semester_gpas = {
            semester: calculate_gpa(courses)
            for semester, courses in semesters.items()
        }

        student_data.append({
            'name': student.name,
            'matric': student.matric_no,
            'semester_gpas': semester_gpas,
            'courses': student.courses
        })

    return render_template('students.html', students=student_data)

@app.route('/export/excel')
def export_excel():
    students = Student.query.all()
    data = []

    for student in students:
        gpa = calculate_gpa(student.courses)
        for course in student.courses:
            data.append({
                'Name': student.name,
                'Matric No': student.matric_no,
                'Course': course.course_name,
                'Score': course.score,
                'GPA': gpa
            })

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Student Records')
    output.seek(0)

    return send_file(output, download_name="student_records.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
