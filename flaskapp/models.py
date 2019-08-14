from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    is_registered = db.Column(db.String(6), nullable=False, default='False')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.is_registered}')"

class Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Detail('{self.name}', '{self.address}', '{self.gender}','{self.phone_no}')"
    