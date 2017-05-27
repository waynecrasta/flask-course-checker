from flask import render_template, flash, request, redirect, url_for
from app import app
from .forms import CourseForm, RegisterForm, LoginForm
from .course_checker import check_open
from .tables import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CourseForm()
    if form.validate_on_submit():
        avail = check_open(form.department.data, form.number.data, form.crn.data)
        flash(avail)
        # flash(return_crn(form.department.data, form.number.data))
    return render_template('course.html', form=form)


@app.route('/result', methods=['POST'])
def result():
    f = request.form
    avail = check_open(f['department'], f['course'], f['crn'])
    return render_template('result.html', avail=avail, section=f['crn'], dept=f['department'], number=f['course'])


@app.route('/login', methods=('GET', 'POST'))
def login():
    wrong_login = False
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
        wrong_login = True
    return render_template('login.html', form=form, wrong_login=wrong_login)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
        if User.query.filter_by(email=email).first():
            form.email.errors.append('This email has already been registered.')
            return render_template('register.html', form=form)
        if User.query.filter_by(username=username).first():
            form.username.errors.append('This username has already been registered.')
            return render_template('register.html', form=form)
        try:
            db.session.add(User(email, username, password))
            db.session.commit()
            user = User.query.filter_by(username=username).first()
            login_user(user)
        except:
            return render_template('register.html', form=form)
        return redirect(url_for('index'))
    else:
        return render_template('register.html', form=form)
