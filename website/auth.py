from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

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
                return redirect('/profile')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exist.", category='error')
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
            flash("Account created successfully!", category="success")
            return redirect(url_for('views.home'))
    return render_template("registration.html", user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def editProfile():
    if request.method == 'POST':
        fullName = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipCode = request.form.get('zipcode')

        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if profile:
            #updATE
        else:
            #create
    elif request.method == 'GET':
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        ##display profile
        return render_template("profile.html")