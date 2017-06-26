from flask import render_template, request, redirect, url_for
from app import app
from .forms import CourseForm, RegisterForm, LoginForm
from .course_checker import check_open
from .tables import User, Subscription, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if (current_user.is_authenticated):
        phone_number = current_user.phone_number
        courses = []
        if Subscription.query.filter_by(user_id=current_user.id).first():
            results = Subscription.query.filter_by(user_id=current_user.id).all()
            courses = [
                {'department': result.department, 'course': result.course, 'crn': result.crn, 'open': result.available}
                for result in
                results]
        return render_template('home.html', courses=courses)
    return render_template('home.html')


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
        phone_number = form.phone_number.data
        carrier = form.carrier.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
        if User.query.filter_by(phone_number=phone_number).first():
            form.phone_number.errors.append('This phone number has already been registered.')
            return render_template('register.html', form=form)
        if User.query.filter_by(username=username).first():
            form.username.errors.append('This username has already been registered.')
            return render_template('register.html', form=form)
        try:
            db.session.add(User(phone_number, carrier, username, password))
            db.session.commit()
            user = User.query.filter_by(username=username).first()
            login_user(user)
        except:
            return render_template('register.html', form=form)
        return redirect(url_for('index'))
    else:
        return render_template('register.html', form=form)


@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    form = CourseForm()
    if request.method == 'POST':
        f = request.form
        try:
            available = check_open(f['department'], f['course'], f['crn'])
            db.session.add(Subscription(current_user.id, f['department'], f['course'], f['crn'], available))
            db.session.commit()
        except:
            return render_template('add_class.html', form=form, f=f, error=True)
        return redirect(url_for('index'))
    return render_template('add_class.html', form=form, f=None, error=False)


@app.route('/delete_class/<crn>')
@login_required
def delete_class(crn):
    course = Subscription.query.filter_by(user_id=current_user.id, crn=crn).first()
    if course:
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for('index'))
