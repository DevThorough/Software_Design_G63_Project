from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User, Profile, FuelQuote
from . import db   ##means from __init__.py import db
from flask_login import login_required
from .pricing import fuelPrice


fuelquote = Blueprint('fuel_quote', __name__)


@fuelquote.route('/fuel_quote', methods=['GET', 'POST'])
@login_required
def fqFunction():
    userID = session['userID']
    profile = Profile.query.filter_by(user_id=userID).first()
    if not profile:
        flash('Don't forget to create a profile!', category='error')##Disable submit button if no profile

    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address')
        delivery_date = request.form.get('delivery_date')
        gallons = float(request.form.get('gallons_requested'))
        price = float(request.form.get('suggested_price'))
        total_amount_due = round(gallons * price,2)
        ## add quote to quote history
        new_quote = FuelQuote(delivery_address=delivery_address, delivery_date=delivery_date,
                                gallons=gallons, price=price, total_amount_due=total_amount_due)
        db.session.add(new_quote)
        db.session.commit()
        flash("Fuel Quote added to History.", category="success")
        return render_template("fuel_quote.html",gallons_requested=gallons, delivery_address=delivery_address,
                                suggested_price = price, delivery_date=delivery_date, total_amount_due=total_amount_due,
                                active="fuelQuoteNavLink")
    elif request.method == 'GET':
        ### Auto populate form if profile exist; client address in profile
        if profile:
            return render_template("fuel_quote.html", onRecord = True,
                                   address1 = profile.address1, address2 = profile.address2,
                                   city = profile.city, state = profile.state,zipCode = profile.zipCode,
                                   active="fuelQuoteNavLink")

        return render_template("fuel_quote.html", active="fuelQuoteNavLink")