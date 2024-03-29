from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User, Profile
from . import db   ##means from __init__.py import db
from flask_login import login_required


history = Blueprint('history', __name__)


@history.route('/history', methods=['GET'])
@login_required
def historyFunction():
    return render_template("fuel_quote_history.html", active="historyNavLink")