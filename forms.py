from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField("Student Name", validators=[DataRequired()])
    matric_no = StringField("Matric Number", validators=[DataRequired()])
    course_name = StringField("Course Name", validators=[DataRequired()])
    score = FloatField("Course Score", validators=[DataRequired()])
    submit = SubmitField("Submit")
