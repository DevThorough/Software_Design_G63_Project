from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User, Profile
from . import db   ##means from __init__.py import db
from flask_login import login_required


fuelquote = Blueprint('fuel_quote', __name__)


@fuelquote.route('/fuel_quote', methods=['GET', 'POST'])
@login_required
def fqFunction():
    if request.method == 'POST':
        delivery_add = request.form.get('delivery_address')
        delivery_date = request.form.get('delivery_date')
        gallons = float(request.form.get('gallons_requested'))
        price = float(request.form.get('suggested_price'))
        total_amount_due = round(gallons * price,2)
        return render_template("fuel_quote.html",gallons_requested=gallons, delivery_address=delivery_add,
                                suggested_price = price, delivery_date=delivery_date, total_amount_due=total_amount_due,
                                active="fuelQuoteNavLink")
    return render_template("fuel_quote.html", active="fuelQuoteNavLink")