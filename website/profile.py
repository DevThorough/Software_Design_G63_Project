from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User, Profile
from . import db   ##means from __init__.py import db
from flask_login import login_required


profile = Blueprint('profile', __name__)


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profileFunction():
    if session['userID']:
        userID = session['userID']
    if request.method == 'POST':
        fullName = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipCode = request.form.get('zipcode')

        profile = Profile.query.filter_by(user_id=userID).first()
        if profile:
            #update profile
            profile.fullName=fullName
            profile.address1=address1
            profile.address2=address2
            profile.city=city
            profile.state=state
            profile.zipCode=zipCode
            db.session.commit()
            flash("Profile edited successfully!", category="success")
            return redirect('/profile')
        else:
            #add profile to our database
            new_profile = Profile(fullName=fullName,address1=address1,address2=address2,
                                  city=city,state=state,zipCode=zipCode, user_id=userID)
            db.session.add(new_profile)
            db.session.commit()
            flash("Profile created successfully!", category="success")
            return redirect('/profile')
    elif request.method == 'GET':
        profile = Profile.query.filter_by(user_id=userID).first()
        ##display profile if exist
        if profile:
            return render_template("profile.html", onRecord = True,
                                   fullName = profile.fullName,address1 = profile.address1,
                                   address2 = profile.address2,city = profile.city,
                                   state = profile.state,zipCode = profile.zipCode,
                                   active="profileNavLink")
        else:
            return render_template("profile.html", onRecord=False, active="profileNavLink")