from flask_wtf import Form
from wtforms import IntegerField, SelectField
from wtforms.validators import DataRequired
from .course_checker import return_subjects


class CourseForm(Form):
    department = SelectField('department', choices=return_subjects(), validators=[DataRequired()])
    number = IntegerField('number', validators=[DataRequired()])
    crn = IntegerField('crn', validators=[DataRequired()])
