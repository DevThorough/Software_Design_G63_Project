from flask import Blueprint
from .models import Profile, FuelQuote
from . import db  ##means from __init__.py import db

pricing = Blueprint('pricing', __name__)


def fuelPrice(gallons, delivery_date, userID):
    if gallons < 0:
        raise ValueError("Gallons can not be negative.")

    price = 3.99
    if gallons >= 100:
        price -= 0.50
    hasHistory = FuelQuote.query.filter_by(user_id=userID).first()
    if hasHistory == True and delivery_date == True:
        ## Apply discount
        price -= 0.5
    profile = Profile.query.filter_by(user_id=userID).first()
    if profile.state == "TX":
        price += 0.20
    else:
        price += 0.40  ## Out of state shipping
    return round(price, 2)