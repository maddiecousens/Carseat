""" Rideshare App """

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

#**TD** Adjust once model.py is created
from model import *
from datetime import datetime


app = Flask(__name__)

# Secret key - required for Flask Sessions and debug toolbar
app.secret_key = "thomothgromoth"

# Fail if Jinja uses undefined variable
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    return render_template('index.html', session=session)

@app.route('/search')
def search_rides():
    """Search database for rides"""

    if request.args.get('query'):
        rides = Ride.query.options(db.joinedload('user')).all()
        return render_template('search.html', rides=rides)
    else:
        starting = request.args.get('starting')
        ending = request.args.get('ending')
        print starting, ending
        
        rides = Ride.query.options(db.joinedload('user')).filter(Ride.start_location == starting, Ride.end_location == ending).all()
        
        #**TD** figure out mile radius & lat/long situation. create lat/long helper fnc
        return render_template('search.html', rides=rides, session=session)

@app.route('/post-ride', methods=["GET"])
def view_rideform():

    return render_template('rideform.html', session=session)

@app.route('/post-ride', methods=["POST"])
def process_rideform():
    driver = request.form.get('driver')
    start_location = request.form.get('start_location')
    end_location = request.form.get('end_location')
    date = datetime.strptime(request.form.get('date'),'%m/%d/%y')
    seats = request.form.get('seats')

    print driver, start_location, end_location, date, seats

    ride = Ride(driver=driver, start_location=start_location, end_location=end_location, date=date, seats=seats)

    db.session.add(ride)
    db.session.commit()
    flash("Ride added to DB")

    return redirect('/')

## Login forms: model window?

@app.route('/login', methods=["GET"])
def view_login():
    return render_template('login.html', session=session)

@app.route("/login", methods=["POST"])
def login_process():
    """Login process"""

    # Get email and password from input fields in form
    email = request.form.get('email')
    password = request.form.get('password')


    # If email is in database, grab password from database
    if User.query.filter(User.email == email).first():

        # Grab user OBJECT
        user = User.query.filter(User.email==email).first()

        db_password = user.password

        # Check if provided pw matches db pw
        if password == db_password:

            # Set session cookie to user_id from user OBJECT
            session['current_user'] = user.user_id 
            flash("Logged in as %s" % user.name)

            return redirect('/') 

        # If wrong password, flash message, redirect to login
        else:
            flash("Wrong password!")
            return redirect("/login")

    # If email is not in database, flash message, redirect to /login
    else:
        flash("Email is not in use.  Please register.")
        return redirect("/login")
    # QUESTION : how do I redirect them from whatever page they logged in from?
    #   ideas: keep stored in sessions what page the request is coming from

@app.route('/logout', methods=["GET"])
def logout_form():
    """temp logout form"""
    return render_template('logout.html', session=session)


@app.route('/logout', methods=["POST"])
def logout():
    """Log user out"""
    del session['current_user']
    flash("You've been logged out")

    return redirect("/")


@app.route('/register', methods=["GET"])
def register_form():
    """Registration form"""
    return render_template('register.html', session=session)

@app.route('/register', methods=["POST"])
def register():
    """Add user to db"""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    flash("You have been added as a user. Please login")
    return redirect("login")

@app.route('/profile', methods=["GET"])
def register_form():

    return render_template('profile.html')


#### Future Routes ####
# @app.route('/details/<rideid>')
# def ride_details():
#     return render_template('details.html', ride_id=ride_id)

# driver profiles

if __name__ == '__main__':
    # Debug for DebugToolbarExtension. Also so server restarts when changes made
    app.debug = True

    # Connection function from model.py
    connect_db(app)

    # Debug Toolbar
    DebugToolbarExtension(app)

    # Allows redirects
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True, host="0.0.0.0")