from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField
from wtforms.validators import InputRequired
from .course_checker import return_subjects


class CourseForm(FlaskForm):
    department = SelectField('department', choices=return_subjects(), validators=[InputRequired()])
    number = IntegerField('number', validators=[InputRequired()])
    crn = IntegerField('crn', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('password', validators=[InputRequired()], render_kw={"placeholder": "password"})


class RegisterForm(FlaskForm):
    phone_number = StringField('phone number', validators=[InputRequired()],
                               render_kw={"placeholder": "phone number"})
    carrier = SelectField('Carrier', choices=[('verizon','Verizon'), ('att', 'AT&T'), ('sprint', 'Sprint'), ('tmobile', 'T-Mobile')])
    username = StringField('username', validators=[InputRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('password', validators=[InputRequired()], render_kw={"placeholder": "password"})
