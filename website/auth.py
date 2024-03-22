from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if len(username) < 2:
            #flash("Username must contain at least 2 characters.", category='error')
            pass
        elif len(password) < 3:
            #flash("Password must contain at least 3 characters.", category='error')
            pass
        else:
            #add user to our database
            flash("Account created successfully!", category="success")
    return render_template("registration.html")