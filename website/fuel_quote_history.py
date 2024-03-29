from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User, Profile
from . import db   ##means from __init__.py import db
from flask_login import login_required


fq_history = Blueprint('fuel_quote_history', __name__)


@fq_history.route('/fuel_quote', methods=['GET', 'POST'])
@login_required
def fqFunction():
    return render_template("fuel_quote_history.html")