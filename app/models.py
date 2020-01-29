from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def compare_passwords(self, password):
        return check_password_hash(self.password_hash, password)
    
    def change_password(username, password):
        user=User.query.filter_by(username=username).first()
        user.password_hash = generate_password_hash(password)
        db.session.commit()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    author = db.Column(db.String(64))
    receiver = db.Column(db.String(64))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def init_data():
    User.query.delete()
    Note.query.delete()
    me = User(username='Michal')
    me.set_password('Bogusz')
    user1 = User(username='Jas')
    user1.set_password('Fasola')
    user2 = User(username='Tyler')
    user2.set_password('Durden')
    db.session.add(me)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    note1 = Note(body='Wysokosc Mount Everest to: 8848 m n.p.m.',author='Michal',receiver='')
    note2 = Note(body='Remember about First Rule',author='Tyler',receiver='Michal')
    note3 = Note(body='Gdzie jest moj mis!?',author='Jas',receiver='Tyler')
    db.session.add(note1)
    db.session.add(note2)
    db.session.add(note3)
    db.session.commit()