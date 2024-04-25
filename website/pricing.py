from flask import Blueprint
from .models import Profile, FuelQuote
from . import db  ##means from __init__.py import db

pricing = Blueprint('pricing', __name__)


def fuelPrice(gallons, delivery_date, userID):
    if gallons < 0:
        raise ValueError("Gallons can not be negative.")

    margin = 0.10 ## Company Profit Factor
    price = 1.50
    if gallons >= 1000:
        margin += 0.02
    else:
        margin += 0.03
    hasHistory = FuelQuote.query.filter_by(user_id=userID).first()
    if hasHistory == True and delivery_date == True:
        ## 0% if no history, otherwise discount 1%
        margin -= 0.01
    profile = Profile.query.filter_by(user_id=userID).first()
    if profile.state == "TX":
        margin += 0.02  ## In state shipping
    else:
        margin += 0.04  ## Out of state shipping
    price += margin * 1.50
    return round(price, 2)