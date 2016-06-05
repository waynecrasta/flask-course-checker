from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CourseForm(Form):
    department = StringField('department', validators=[DataRequired()])
    number = IntegerField('number', validators=[DataRequired()])
    crn = IntegerField('crn', validators=[DataRequired()])
