from flask import Blueprint, render_template, request, flash, redirect, session
from website.models import User, Profile, FuelQuote
from website.__init__ import db   ##means from __init__.py import db
from flask_login import login_required


fq_history = Blueprint('fuel_quote_history', __name__)


@fq_history.route('/history', methods=['GET', 'POST'])
@login_required
def historyFunction():
    # User is the name of table that has a column name
    userID = session['userID']
    quote_history = FuelQuote.query.filter_by(user_id=userID).all()
    return render_template("fuel_quote_history.html", active="historyNavLink",
                           quote_history=quote_history)