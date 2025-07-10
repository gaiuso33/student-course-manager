from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, PasswordField
from wtforms import SelectField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField("Student Name", validators=[DataRequired()])
    matric_no = StringField("Matric Number", validators=[DataRequired()])
    course_name = StringField("Course Name", validators=[DataRequired()])
    score = FloatField("Score", validators=[DataRequired()])
    semester = SelectField("Semester", choices=[
        ("2024/2025 - First", "2024/2025 - First"),
        ("2024/2025 - Second", "2024/2025 - Second")
    ])
    submit = SubmitField("Add Record")
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
