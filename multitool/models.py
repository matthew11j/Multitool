from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from multitool import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Module('{self.title}', '{self.description}')"

class Golf_Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False, default="N/A")
    date_played = db.Column(db.DateTime, default="N/A")
    h1Score = db.Column(db.Integer)
    h2Score = db.Column(db.Integer)
    h3Score = db.Column(db.Integer)
    h4Score = db.Column(db.Integer)
    h5Score = db.Column(db.Integer)
    h6Score = db.Column(db.Integer)
    h7Score = db.Column(db.Integer)
    h8Score = db.Column(db.Integer)
    h9Score = db.Column(db.Integer)
    h10Score = db.Column(db.Integer)
    h11Score = db.Column(db.Integer)
    h12Score = db.Column(db.Integer)
    h13Score = db.Column(db.Integer)
    h14Score = db.Column(db.Integer)
    h15Score = db.Column(db.Integer)
    h16Score = db.Column(db.Integer)
    h17Score = db.Column(db.Integer)
    h18Score = db.Column(db.Integer)
    h1Putt = db.Column(db.Integer)
    h2Putt = db.Column(db.Integer)
    h3Putt = db.Column(db.Integer)
    h4Putt = db.Column(db.Integer)
    h5Putt = db.Column(db.Integer)
    h6Putt = db.Column(db.Integer)
    h7Putt = db.Column(db.Integer)
    h8Putt = db.Column(db.Integer)
    h9Putt = db.Column(db.Integer)
    h10Putt = db.Column(db.Integer)
    h11Putt = db.Column(db.Integer)
    h12Putt = db.Column(db.Integer)
    h13Putt = db.Column(db.Integer)
    h14Putt = db.Column(db.Integer)
    h15Putt = db.Column(db.Integer)
    h16Putt = db.Column(db.Integer)
    h17Putt = db.Column(db.Integer)
    h18Putt = db.Column(db.Integer)
    frontScore = db.Column(db.Integer)
    backScore = db.Column(db.Integer)
    totalScore = db.Column(db.Integer)
    course_played = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Golf_Round('{self.id}', '{self.date_played}')"

class Golf_Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    h1Par = db.Column(db.Integer)
    h2Par = db.Column(db.Integer)
    h3Par = db.Column(db.Integer)
    h4Par = db.Column(db.Integer)
    h5Par = db.Column(db.Integer)
    h6Par = db.Column(db.Integer)
    h7Par = db.Column(db.Integer)
    h8Par = db.Column(db.Integer)
    h9Par = db.Column(db.Integer)
    h10Par = db.Column(db.Integer)
    h11Par = db.Column(db.Integer)
    h12Par = db.Column(db.Integer)
    h13Par = db.Column(db.Integer)
    h14Par = db.Column(db.Integer)
    h15Par = db.Column(db.Integer)
    h16Par = db.Column(db.Integer)
    h17Par = db.Column(db.Integer)
    h18Par = db.Column(db.Integer)

    def __repr__(self):
        return f"Golf_Course('{self.name}')"