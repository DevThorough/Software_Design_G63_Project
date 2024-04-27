from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.models import User, Profile
from website.__init__ import db   # means from __init__.py import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if 'loggedIn' not in session:
        session['loggedIn'] = False
    return render_template("homepage.html", loggedIn=session['loggedIn'])

@views.route('/home')
def homepage():
    if 'loggedIn' not in session:
        session['loggedIn'] = False
    return render_template("homepage.html", loggedIn=session['loggedIn'])