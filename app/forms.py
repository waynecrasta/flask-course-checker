from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from .course_checker import return_subjects


class CourseForm(FlaskForm):
    department = SelectField('department', choices=return_subjects(), validators=[InputRequired()])
    number = IntegerField('number', validators=[InputRequired()])
    crn = IntegerField('crn', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('password', validators=[InputRequired()], render_kw={"placeholder": "password"})


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email")],
                        render_kw={"placeholder": "email"})
    username = StringField('username', validators=[InputRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('password', validators=[InputRequired()], render_kw={"placeholder": "password"})
