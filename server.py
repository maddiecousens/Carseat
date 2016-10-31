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

    return render_template('index.html')

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
        return render_template('search.html', rides=rides)

@app.route('/post-ride', methods=["GET"])
def view_rideform():

    return render_template('rideform.html')

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
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():
    pass
    # check if username/password matches
    # log user in
    # flash messages
    # QUESTION : how do I redirect them from whatever page they logged in from?
    #   ideas: keep stored in sessions what page the request is coming from

@app.route('/logout', methods=["POST"])
def logout():
    # logout user
    # delete session
    # flash message
    return redirect('/')

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