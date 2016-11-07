""" Rideshare App """

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, 
                   request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Ride, Rider, Request, connect_db, db

from datetime import datetime, date, timedelta

import geocoder

import arrow
import pytz
from helperfunctions import state_to_timezone



app = Flask(__name__)

# Secret key - required for Flask Sessions and debug toolbar
app.secret_key = "thomothgromoth"

# Fail if Jinja uses undefined variable
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

#############################################################################
# Routes

@app.route('/')
def index():
    """ Homepage """

    return render_template('index.html')

@app.route('/search')
def search_rides():
    """Search database for rides"""

    # If user clicks 'All Rides' from NavBar, show all rides
    if request.args.get('query'):
        rides = Ride.query.options(db.joinedload('user')).order_by(Ride.start_timestamp).all()
        

        for ride in rides:
            # print '\n {} type" {} \n'.format(ride.start_name, type(ride.start_name))
            tz = state_to_timezone(ride.start_state)
            ride.start_timestamp = ride.start_timestamp.replace(tzinfo=pytz.timezone(tz))

            if ride.start_timestamp.date() == date.today():
                ride.start_timestamp = "Today, {}".format(ride.start_timestamp.strftime('%-I:%M %p'))

            elif ride.start_timestamp.date() == (date.today() + timedelta(days=1)):
                ride.start_timestamp = "Tomorrow, {}".format(ride.start_timestamp.strftime('%-I:%M %p'))
            else:
                ride.start_timestamp = ride.start_timestamp.date().strftime('%A, %b %d, %Y %-I:%M %p')
            # ride.start_timestamp = arrow.get(ride.start_timestamp).humanize()
            # print '\n\n'
            # print ride.start_timestamp
 
        return render_template('search.html', rides=rides)

    # If user enters search terms, show rides based off search terms  
    else:
 
        ### At some point remove other arguments for this GET request

        # Eventually add miles as an input field
        miles = 25
        deg = miles_to_degrees(miles)

        start_lat = float(request.args.get('lat'))
        start_lng = float(request.args.get('lng'))
        end_lat = float(request.args.get('lat2'))
        end_lng = float(request.args.get('lng2'))
        
        rides = (Ride.query.options(db.joinedload('user'))
                          .filter(((Ride.start_lat < str(start_lat + deg)) &
                            (Ride.start_lat > str(start_lat - deg))) &
                           ((Ride.start_lng < str(start_lng + deg)) &
                            (Ride.start_lng > str(start_lng - deg))) &
                           ((Ride.end_lat < str(end_lat + deg)) &
                            (Ride.end_lat > str(end_lat - deg))) &
                           ((Ride.end_lng < str(end_lng + deg)) &
                            (Ride.end_lng > str(end_lng - deg))))
                    .order_by(Ride.start_timestamp).all())

        for ride in rides:
            tz = state_to_timezone(ride.start_state)
            ride.start_timestamp = ride.start_timestamp.replace(tzinfo=pytz.timezone(tz))

            if ride.start_timestamp.date() == date.today():
                ride.start_timestamp = "Today, {}".format(ride.start_timestamp.strftime('%-I:%M %p'))

            elif ride.start_timestamp.date() == (date.today() + timedelta(days=1)):
                ride.start_timestamp = "Tomorrow, {}".format(ride.start_timestamp.strftime('%-I:%M %p'))
            else:
                ride.start_timestamp = ride.start_timestamp.date().strftime('%A, %b %d, %Y %-I:%M %p')

        
        return render_template('search.html', rides=rides)

@app.route('/post-ride', methods=["GET"])
def view_rideform():
    """ Form to post new ride """

    return render_template('rideform.html')

@app.route('/googletest', methods=["GET"])
def google_test():
    """  """

    return render_template('googletest.html')

@app.route('/post-ride', methods=["POST"])
def process_rideform():
    """ Add new ride to database """
    
    # ADD: logged-in check
    user = session['current_user']
    driver = session['current_user']

    ###### Store Auto Completed Addresses ########

    start_string = request.form.get('start-address')
    start_lat = request.form.get('lat')
    start_lng = request.form.get('lng')
    start_number = request.form.get('street_number')
    start_street = request.form.get('route')
    start_city = request.form.get('locality')
    start_state = request.form.get('administrative_area_level_1')
    start_zip = request.form.get('postal_code')

    end_string = request.form.get('end-address')
    end_lat = request.form.get('lat2')
    end_lng = request.form.get('lng2')
    end_number = request.form.get('street_number2')
    end_street = request.form.get('route2')
    end_city = request.form.get('locality2')
    end_state = request.form.get('administrative_area_level_1_2')
    end_zip = request.form.get('postal_code2')


    ##### Other Data ######

    cost = request.form.get('cost')
    seats = request.form.get('seats')

    car_type = request.form.get('cartype')
    luggage = request.form.get('luggage')
    comments = request.form.get('comments')

    # date1 = request.form.get('date1')
    # date2 = request.form.get('date2')

    ####### PARSE datetime from datetimepicker ########

    start_time = datetime.strptime(request.form.get('date1'), "%m/%d/%Y %I:%M %p")
    end_time = datetime.strptime(request.form.get('date2'), "%m/%d/%Y %I:%M %p")

    ######## Convert to UTC #########

    # Parse date from form
    leaving = arrow.get(request.form.get('date1'), 'MM/DD/YYYY h:mm A')
    # arriving = arrow.get(request.form.get('date2'), 'MM/DD/YYYY h:mm A')

    # Get starting and leaving timezones via Arrow library
    tz_leaving = state_to_timezone(start_state)
    tz_arriving = state_to_timezone(end_state)

    # Add timezones to Arrow objects
    # leaving_with_tz = start_time.replace(tzinfo=tz_leaving)
    # arriving_with_tz = end_time.replace(tzinfo=tz_arriving)

    leaving_with_tz = start_time.replace(tzinfo=pytz.timezone(tz_leaving))
    arriving_with_tz = end_time.replace(tzinfo=pytz.timezone(tz_arriving))

    

    # Convert to UTC
    # leaving_utc = leaving_with_tz.to('utc')
    # arriving_utc = arriving_with_tz.to('utc')

    leaving_utc = leaving_with_tz.astimezone(pytz.utc)
    arriving_utc = arriving_with_tz.astimezone(pytz.utc)

    ######## Create Ride Instance ############

    ride = Ride(driver=driver,
                seats=seats,
                cost=cost,
                # starting location
                start_lat=start_lat,
                start_lng=start_lng, #eventually change to lng
                start_number=start_number,
                start_street=start_street,
                start_city=start_city,
                start_state=start_state,
                start_zip=start_zip,
                # ending location
                end_lat=end_lat,
                end_lng=end_lng,
                end_number=end_number,
                end_street=end_street,
                end_city=end_city,
                end_state=end_state,
                end_zip=end_zip,
                #details
                start_timestamp=leaving_utc,
                end_timestamp=arriving_utc,

                car_type=car_type,
                luggage=luggage,
                comments=comments
               )

    db.session.add(ride)
    db.session.commit()

    flash("Ride added to DB")

    return redirect('/profile/{}'.format(user)) 



@app.route('/login', methods=["GET"])
def view_login():
    """ Show login form """
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login_process():
    """ Process login """

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
            flash("Logged in as %s" % user.first_name)
            redirect_path = '/profile/{}'.format(user.user_id)
            return redirect(redirect_path) 

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
    """ Temporary logout form """

    del session['current_user']
    flash("You've been logged out")

    return redirect("/")

@app.route('/register', methods=["GET"])
def register_form():
    """ Registration form """

    return render_template('register.html')

@app.route('/register', methods=["POST"])
def register():
    """Add new user to database """

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    flash("You have been added as a user. Please login")

    return redirect("login")


@app.route('/profile/<user_id>', methods=["GET"])
def user_profile(user_id):
    """ Show users home page """
    # Eventually will make this so that you can view your drivers page too

    user = User.query.options(db.joinedload('rides_taking'), db.joinedload('rides_offered')).get(user_id)
    rides_offered = user.rides_offered
    # request_objects = []
    # for ride in rides_offered:
    #     if ride.requests:
    #         request_objects.append

    rides_taking = user.rides_taking

    return render_template('profile.html', user=user, 
                                           rides_offered=rides_offered, 
                                           rides_taking=rides_taking)

@app.route('/request-seats', methods=["POST"])
def request_seats():
    """ Add request for a seat to database """
    
    # Grab number of seats requested
    seats = request.form.get('seats')

    # Grab ride_id from html
    ride_id = request.form.get('ride_id')

    # Grab requester from session
    requester = session['current_user']

    # Make request instance
    new_request = Request(ride_id=ride_id, requester=requester, seats=seats)

    db.session.add(new_request)
    db.session.commit()
    flash('You have requested this ride')

    path = '/profile/{}'.format(requester)
    return redirect(path)


@app.route('/request-approval', methods=["POST"])
def request_approval():
    """Approve or reject request"""

    # Grab whether the approve or deny request was clicked
    approval = request.form.get('approvedeny')

    # Grab other information from html/session
    ride_id = request.form.get('ride_id')
    requester = request.form.get('requester')
    seats = request.form.get('seats')
    request_id = request.form.get('request_id')
    current_user = session['current_user']

    # If request is approved
    if approval == 'Approve':
        # Query for Request object
        ride_request = Request.query.get(request_id)

        # Query for Ride object
        ride = Ride.query.get(ride_id)
        # Subtract number of seats from Ride
        ride.seats = ride.seats - int(seats)

        # Create new Rider object
        rider = Rider(ride_id=ride_id, user_id=requester, seats=seats)

        # Delete Request Row
        db.session.delete(ride_request)
        db.session.add(rider)
        db.session.commit()

        flash("Request Approved")

    # If request is rejected
    else:
        # Query for Request object
        ride_request = Request.query.get(request_id)

        # Delete Request
        db.session.delete(ride_request)
        db.session.commit()
        flash("Request Denied")

    path = '/profile/{}'.format(current_user)
    return redirect(path)

#### Future Routes ####
# @app.route('/details/<rideid>')
# def ride_details():
#     return render_template('details.html', ride_id=ride_id)

def miles_to_degrees(miles):
    MILE_TO_DEGREE = 69.0
    return miles / MILE_TO_DEGREE

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