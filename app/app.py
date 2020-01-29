from flask import Flask, session, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import redis
import os

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
db = SQLAlchemy(app)


import models
from models import User, Note, init_data
init_data()

@app.route('/')
@app.route('/index')
@login_required
def index():
    notes = Note.query.all()
    notesForUser = []
    for note in notes:
        if note.receiver == '' or note.receiver == str(current_user.username):
            notesForUser.append(note)
    return render_template('index.html', title='Home', notes=notesForUser)


@app.route('/changepassform')
@login_required
def changepassform():
    return render_template('passChange.html')


@app.route('/changepass', methods=['POST'])
@login_required
def changepass():
    user=str(current_user.username)
    user_record = User.query.filter_by(username=user).first()
    old =request.form.get('old' )
    new =request.form.get('new' )
    conf=request.form.get('conf')
    if not user_record.compare_passwords(old):
        flash("Niepoprawne stare haslo")
        return redirect(url_for('changepassform'))
    if new != conf:
        flash("Potwierdzenie hasla musi byc takie samo")
        return redirect(url_for('changepassform'))
    User.change_password(user, new)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.compare_passwords(request.form['password']):
            flash('Niepoprawny login lub haslo')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/addnote', methods=['POST'])
@login_required
def addnote():
    note=request.form.get('note')
    author=request.form.get('author')
    check=request.form.get('check')
    receiver=request.form.get('receiver')
    if check == "on":
        receiver=''
    newNote = Note(body=note,author=author,receiver=receiver)
    db.session.add(newNote)
    db.session.commit()
    return redirect(url_for('index'))   


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

    

