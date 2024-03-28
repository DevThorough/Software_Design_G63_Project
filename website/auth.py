from flask import Blueprint, render_template, request, flash, redirect, url_for, session
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
                session['userID'] = user.id
                session['loggedIn'] = True
                return redirect(url_for('.profile', userID = user.id))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    logout_user()
    session.pop('loggedIn', None)
    session.pop('userID', None)
    return redirect(url_for('.login'))

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
    else:
        redirect('/register')

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if session['userID']:
        userID = session['userID']
    if request.method == 'POST':
        fullName = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipCode = request.form.get('zipcode')

        profile = Profile.query.filter_by(user_id=userID).first()
        if profile:
            #update profile
            profile.fullName=fullName
            profile.address1=address1
            profile.address2=address2
            profile.city=city
            profile.state=state
            profile.zipCode=zipCode
            db.session.commit()
            flash("Profile edited successfully!", category="success")
            return redirect('/profile')
        else:
            #add profile to our database
            new_profile = Profile(fullName=fullName,address1=address1,address2=address2,
                                  city=city,state=state,zipCode=zipCode, user_id=userID)
            db.session.add(new_profile)
            db.session.commit()
            flash("Profile created successfully!", category="success")
            return redirect('/profile')
    elif request.method == 'GET':
        profile = Profile.query.filter_by(user_id=userID).first()
        ##display profile if exist
        if profile:
            return render_template("profile.html", onRecord = True,
                                   fullName = profile.fullName,address1 = profile.address1,
                                   address2 = profile.address2,city = profile.city,
                                   state = profile.state,zipCode = profile.zipCode)
        else:
            return render_template("profile.html", onRecord=False)