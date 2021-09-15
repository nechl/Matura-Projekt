from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    food = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,  default=datetime.utcnow)
    amount = db.Column(db.Integer())
    finished_at = db.Column(db.DateTime, index = True)
    start_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Order {};{}>'.format(self.food, self.user_id)
    
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))