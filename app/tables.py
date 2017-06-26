from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://wayne:password@localhost/course_checker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(120))
    carrier = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, phone_number, carrier, username, password):
        self.phone_number = phone_number
        self.carrier = carrier
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String(120))
    course = db.Column(db.String(120))
    crn = db.Column(db.String(120))
    available = db.Column(db.String(120))

    def __init__(self, user_id, department, course, crn, available):
        self.user_id = user_id
        self.department = department
        self.course = course
        self.crn = crn
        self.available = available


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
