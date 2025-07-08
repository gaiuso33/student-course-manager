from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from forms import StudentForm
from flask import request, redirect, url_for

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

if __name__ == '__main__':
    app.run(debug=True)
