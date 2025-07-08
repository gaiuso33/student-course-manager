from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from forms import StudentForm
from flask import request, redirect, url_for
import pandas as pd
from flask import send_file
from io import BytesIO


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
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

# ------------------ helper functions ------------------

def calculate_gpa(grades):
    total_points = 0
    total_courses = len(grades)
    
    for grade in grades:
        score = grade.score
        # Use your university's grading scale
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

    return round(total_points / total_courses, 2) if total_courses > 0 else 0.0

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
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
            student_id=student.id
        )
        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_student.html', form=form)

@app.route('/students')
def list_students():
    students = Student.query.all()
    student_data = []

    for student in students:
        gpa = calculate_gpa(student.courses)
        student_data.append({
            'name': student.name,
            'matric': student.matric_no,
            'gpa': gpa,
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
