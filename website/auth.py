from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db   ##means from __init__.py import db
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                session['userID'] = user.id
                session['loggedIn'] = True
                return redirect('/home')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template("login.html", loggedIn=session['loggedIn'])

@auth.route('/logout')
def logout():
    logout_user()
    session['loggedIn'] = False
    session.pop('userID', None)
    return redirect('/home')

@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exist.", category='error')
            return redirect('register')
        elif len(username) < 2:
            flash("Username must contain at least 2 characters.", category='error')
        elif len(password) < 3:
            flash("Password must contain at least 3 characters.", category='error')
        else:
            #add user to our database
            new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully! You may login.", category="success")
            response = make_response(render_template('login.html'), 200)
            return response
    else:
        return render_template("registration.html", loggedIn=session['loggedIn'])