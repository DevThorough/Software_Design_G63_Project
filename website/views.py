from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Profile
from . import db   ##means from __init__.py import db
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    if(not session['loggedIn']):
        session['loggedIn'] = False;
    return render_template("login.html", loggedIn=session['loggedIn'])