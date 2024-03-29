from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User, Profile
from . import db   ##means from __init__.py import db
from flask_login import login_required


fuelquote = Blueprint('fuel_quote', __name__)


@fuelquote.route('/fuel_quote', methods=['GET', 'POST'])
@login_required
def fqFunction():
    userID = session['userID']
    profile = Profile.query.filter_by(user_id=userID).first()
    if not profile:
        flash('Create a profile to get a quote.', category='error')

    if request.method == 'POST':
        ## client address in profile: profile.state, profile.city etc.
        delivery_state = profile.state
        delivery_date = request.form.get('delivery_date')
        gallons = float(request.form.get('gallons_requested'))
        price = float(request.form.get('suggested_price'))
        total_amount_due = round(gallons * price,2)
        return render_template("fuel_quote.html",gallons_requested=gallons, delivery_address=delivery_state,
                                suggested_price = price, delivery_date=delivery_date, total_amount_due=total_amount_due,
                                active="fuelQuoteNavLink")
    elif request.method == 'GET':

        return render_template("fuel_quote.html", active="fuelQuoteNavLink")