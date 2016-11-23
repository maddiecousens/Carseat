""" Rideshare App """

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash, 
                   session)
from sqlalchemy import cast, Time
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Ride, Rider, Request, connect_db, db

from datetime import datetime, date, timedelta, time
import pytz

import geocoder

from helperfunctions import state_to_timezone, miles_to_degrees

import os
import googlemaps

import facebook

import math


app = Flask(__name__)

# Secret key - required for Flask Sessions and debug toolbar
app.secret_key = "thomothgromoth"

# Fail if Jinja uses undefined variable
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

GOOGLE_KEY = os.environ["GOOGLE_KEY"]

#############################################################################
# Routes

@app.route('/')
def index():
    """ Homepage """

    return render_template('index.html')

##################################                               
####### Searching Routes #########
##################################

@app.route('/search')
def search_rides():
    """Searches database for rides"""

    # initialize to show 10 results ordered by date
    limit = 10
    order_by = 'date'

    ### If user clicks 'All Rides' ###
    if request.args.get('query'):
        start_time = "12:00 AM"
        start_state = ''
        start_time = datetime.strptime(start_time, '%I:%M %p')
        start_time = to_utc(start_state, start_time).time()

        date_from = "10/21/2016"
        date_from = datetime.strptime(date_from, '%m/%d/%Y')
        date_from = to_utc(start_state, date_from).date()
        cost = 50

        # Query database for all rides
        rides = Ride.get_rides(start_time=start_time, date_from=date_from, cost=cost, limit=limit, order_by=order_by)


        # Round up page count with + 1
        total_count = Ride.get_rides(start_time=start_time, date_from=date_from, cost=cost, order_by=order_by, count=True)
        print '\n\ntotal_count: {}\n\n'.format(total_count)
        page_count = int(math.ceil(float(total_count)/float(limit)))

        for ride in rides:
            # convert ride to local timezone
            ride.start_timestamp = to_local(ride.start_state, ride.start_timestamp)
            # turn date object into string for front end
            ride.start_timestamp = to_time_string(ride.start_state, ride.start_timestamp)

        # Render search page, passing rides and page_count for pagination
        return render_template('search.html', rides=rides, page_count=page_count)

    ### If user enters search terms ###
    else:
 
        # Start with 15mile square search
        miles = 15
        deg = miles_to_degrees(miles)
        
        # Get search terms lat/lng
        start_lat = float(request.args.get('lat'))
        start_lng = float(request.args.get('lng'))
        end_lat = float(request.args.get('lat2'))
        end_lng = float(request.args.get('lng2'))

        # Dicts holding search terms to be placed in DOM and used by AJAX when 
        #   user toggles search parameters
        start_search = {"term": request.args.get('searchstring'),
                        "state": request.args.get('administrative_area_level_1'),
                        "lat": start_lat,
                        "lng": start_lng
                       }
        end_search = {"term": request.args.get('searchstring2'),
                      "state": request.args.get('administrative_area_level_1_2'),
                      "lat": end_lat,
                      "lng": end_lng
                      }
        # Get the first 10 results for query
        rides = Ride.get_rides(deg=deg,
                               start_lat=start_lat,
                               start_lng=start_lng,
                               end_lat=end_lat,
                               end_lng=end_lng,
                               limit=limit,
                               order_by=order_by)
        if len(rides) > limit:
            total_count = Ride.get_rides(deg=deg,
                                   start_lat=start_lat,
                                   start_lng=start_lng,
                                   end_lat=end_lat,
                                   end_lng=end_lng,
                                   limit=limit,
                                   order_by=order_by,
                                   count=True)
            # Round up page count with + 1
            page_count = int(math.ceil(float(total_count)/float(limit)))
        else:
            page_count = 1

        for ride in rides:
            # convert ride to local timezone
            ride.start_timestamp = to_local(ride.start_state, ride.start_timestamp)
            # turn date object into string for front end
            ride.start_timestamp = to_time_string(ride.start_state, ride.start_timestamp)

        return render_template('search.html', rides=rides,
                                              start_search=start_search,
                                              end_search=end_search,
                                              page_count=page_count)

@app.route('/search.json')
def json_test():
    """Return new ride results"""

    #Get search terms

    start_term = request.args.get('start_term')
    end_term = request.args.get('end_term')

    user_lat = request.args.get('user_lat')
    user_lng = request.args.get('user_lng')

    start_lat = request.args.get('start_lat')
    start_lng = request.args.get('start_lng')
    end_lat = request.args.get('end_lat')
    end_lng = request.args.get('end_lng')
    start_state = request.args.get("start_state")

    # Get search toggles (time, cost, date)

    start_time = request.args.get("start")
    cost = request.args.get("cost")

    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    limit = request.args.get("limit")
    offset = request.args.get("offset")
    offset = int(offset) * int(limit)
    order_by = request.args.get("order")

    # If there are no search terms, start_state will be an empty string. In this
    # case it it best to use the clients timezone to cater results to dates/ times in their
    # tz.
    if not start_state:
        # Using a try statement, because if google is unable to geocode the user, 
        # I don't want this to error out, any would rather default to 'US/Pacific'
        try:
            start_state = (geocoder.google('{}, {}'.format(user_lat, user_lng))).state
            # adding this check, because sometimes this returns odd strings
            if len(start_state) > 2:
                start_state = ''
        except:
            # Blank start states default to 'US/Pacific'
            start_state = ''

    # convert dates and time to utc to be queried against db
    if date_from:
        date_from = datetime.strptime(date_from, '%m/%d/%Y')
        date_from = to_utc(start_state, date_from).date()

    if date_to:
        date_to = datetime.strptime(date_to, '%m/%d/%Y')
        date_to = to_utc(start_state, date_to).date()

    start_time = datetime.strptime(start_time, '%I:%M %p')
    start_time = to_utc(start_state, start_time).time()


    # Convert miles to lat/lng degrees
    deg = miles_to_degrees(25)


    rides = Ride.get_rides(deg=deg,
                           start_lat=start_lat,
                           start_lng=start_lng,
                           end_lat=end_lat,
                           end_lng=end_lng,
                           start_time=start_time,
                           cost=cost,
                           date_to=date_to,
                           date_from=date_from,
                           limit=limit,
                           offset=offset,
                           order_by=order_by)

    print '\nlimit: {}\noffset: {}\norder_by: {}\ndate_form: {}'.format(limit,offset,order_by, date_from)

    total_count = Ride.get_rides(deg=deg,
                                 start_lat=start_lat,
                                 start_lng=start_lng,
                                 end_lat=end_lat,
                                 end_lng=end_lng,
                                 start_time=start_time,
                                 cost=cost,
                                 date_to=date_to,
                                 date_from=date_from,
                                 count=True)
    print '\ntotal_count: {}\n'.format(total_count)

    json_list = sqlalchemy_to_json(rides, total_count, limit)

    return jsonify(json_list)

##################################                               
######## Test Route #############
##################################

@app.route('/test', methods=["GET"])
def view_test():
    """ Form to post new ride """

    return render_template('googletest5.html')


##################################                               
######## Post Ride Form ##########
##################################

@app.route('/post-ride', methods=["GET"])
def view_rideform():
    """ Form to post new ride """

    return render_template('rideform.html')

@app.route('/post-ride', methods=["POST"])
def process_rideform():
    """ Add new ride to database """

    ## V2. verify on backend. send AJAX request, if errors notify user

    # driver is logged in user
    driver = session['current_user']

    # retrieve form inputs
    seats = int(request.form.get('seats'))
    cost = int(float(request.form.get('cost')))

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

    date = request.form.get('date')
    time = request.form.get('time')

    start_time = datetime.strptime("{} {}".format(date, time), "%m/%d/%Y %I:%M %p")
    # Convert to utc
    start_time = to_utc(start_state, start_time)

    # calculate duration and mileage from gmaps api
    gmaps = googlemaps.Client(key=GOOGLE_KEY)

    try:
        directions_result = gmaps.directions("{},{}".format(start_lat, start_lng),
                                             "{},{}".format(end_lat, end_lng),
                                             traffic_model='best_guess',
                                             departure_time=start_time)

        duration = directions_result[0]['legs'][0]['duration']['text']

        mileage = directions_result[0]['legs'][0]['distance']['text']
    except:
        duration = None
        mileage = None

    luggage = request.form.get('luggage')
    comments = request.form.get('comments')
    pickup_window = request.form.get('pickup-window')
    detour = request.form.get('detour')
    car_type = request.form.get('cartype')
    
    # Create Ride Instance 
    ride = Ride(driver=driver,
                seats=seats,
                cost=cost,
                start_lat=start_lat,
                start_lng=start_lng,
                start_number=start_number,
                start_street=start_street,
                start_city=start_city,
                start_state=start_state,
                start_zip=start_zip,
                end_lat=end_lat,
                end_lng=end_lng,
                end_number=end_number,
                end_street=end_street,
                end_city=end_city,
                end_state=end_state,
                end_zip=end_zip,
                start_timestamp=start_time,
                mileage=mileage, #compute
                duration=duration, #compute
                luggage=luggage,
                comments=comments,
                pickup_window=pickup_window,
                detour=detour,
                car_type=car_type
               )

    # validate fields
    ride = validate_ride(ride)

    #commit to db
    db.session.add(ride)
    db.session.commit()

    flash("Ride added to DB")

    return redirect('/profile/{}'.format(driver))

##################################                               
######### Login/Logout ###########
##################################

@app.route('/check-login.json')
def check_login():
    """ Return True if session variable"""
    logged_in = {
                'logged_in' : bool(session.get("current_user"))
                }

    return jsonify(logged_in)

@app.route("/login", methods=["POST"])
def fb_login_process():
    """ Facebook Process login """

    # retrieve id and access_token
    fb_userid = request.form.get("id")
    fb_user_accesstoken = request.form.get('access_token')

    # If user is in db, add their user_id to session
    if User.query.filter(User.fb_userid == fb_userid).first():
        # Grab user OBJECT
        user = User.query.filter(User.fb_userid == fb_userid).one()
        session['current_user'] = user.user_id

    # If new user, get info from FB Graph API and add to db
    else:
        graph = facebook.GraphAPI(fb_user_accesstoken)
        profile = graph.get_object('me')
        args = {'fields' : 'id,name,email,picture.width(200).height(200)'}
        profile = graph.get_object('me', **args)

        first_name = profile.get('name').split()[0]
        last_name = profile.get('name').split()[1]
        email = profile.get('email')
        image = profile.get('picture')['data']['url']

        # create user instance and commit to db
        user = User(fb_userid=fb_userid, first_name=first_name, last_name=last_name,
                    email=email, image=image)
        db.session.add(user)
        db.session.commit()

        # add user to session
        user = User.query.filter(User.fb_userid == fb_userid).one()
        session['current_user'] = user.user_id
    return "logged in"

@app.route('/logout', methods=["GET"])
def logout_form():
    """ Log user out"""
    if session.get('current_user'):
        del session['current_user']

    return render_template('index.html')


##################################                         
#### Profile Page + Requests #####
##################################


@app.route('/profile/<user_id>')
def user_profile(user_id):
    """ Show users home page """

    # get user with joined loads rides_taking and rides_offered
    user = User.query.options(db.joinedload('rides_taking'), db.joinedload('rides_offered')).get(user_id)
    
    rides_offered = user.rides_offered
    rides_offered_requests = []

    # If there are requests for rides you are offering, append
    for ride in rides_offered:
        if ride.requests:
            rides_offered_requests.append(ride)

    rides_taking = user.rides_taking
    rides_taking_requests = Request.query.filter(Request.requester==user_id).all()

    return render_template('profile.html',
                            user=user,
                            rides_offered=rides_offered,
                            rides_offered_requests=rides_offered_requests,
                            rides_taking=rides_taking,
                            rides_taking_requests=rides_taking_requests
                            )


@app.route('/request-seats', methods=["POST"])
def request_seats():
    """ Add request for a seat to database """
    
    # Retrieve number of seats, ride_id from form
    seats = request.form.get('seats')
    ride_id = request.form.get('ride_id')

    requester = session['current_user']

    # Request instance
    new_request = Request(ride_id=ride_id, requester=requester, seats=seats)

    db.session.add(new_request)
    db.session.commit()

    return redirect('/profile/{}'.format(requester))


@app.route('/request-approval', methods=["POST"])
def request_approval():
    """Approve or reject request"""

    # Approval will be either 'Approve' or 'Deny'
    approval = request.form.get('approvedeny')

    # Retrieve other form information
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

    # If request is rejected
    else:
        # Query for Request object
        ride_request = Request.query.get(request_id)

        # Delete Request
        db.session.delete(ride_request)
        db.session.commit()

    return redirect('/profile/{}'.format(current_user))

### Helper Functions ###

def sqlalchemy_to_json(rides, total_count, limit):
    """Convert sqlalchemy ride objects to json"""

    ## Add more validation

    attributes = ['car_type',
                 'comments',
                 'cost',
                 'detour',
                 'driver',
                 'duration',
                 'end_city',
                 'end_lat',
                 'end_lng',
                 'end_name',
                 'end_number',
                 'end_state',
                 'end_street',
                 'end_zip',
                 'luggage',
                 'mileage',
                 'pickup_window',
                 'ride_id',
                 'seats',
                 'start_city',
                 'start_lat',
                 'start_lng',
                 'start_name',
                 'start_number',
                 'start_state',
                 'start_street',
                 'start_timestamp',
                 'start_zip']

    # Round up page count
    page_count = int(math.ceil(float(total_count)/float(limit)))

    #Initialize json list with page count
    json_list = [{'page_count': page_count},[]]

    for ride in rides:

        ride_dict = {}

        # Add all attributes to temporary dictionary
        for attr in attributes:
            ride_dict[attr] = getattr(ride, attr)
        
        # Convert timestamp to local, add as string to temp_dict
        ride.start_timestamp = to_local(ride.start_state, ride.start_timestamp)
        ride_dict['start_timestamp'] = to_time_string(ride.start_state, ride.start_timestamp)

        # Add driver info, utilizing SQLAlchemy relationships
        ride_dict['user_first_name'] = ride.user.first_name
        ride_dict['user_image'] = ride.user.image
        
        # add ride dictionary to json list
        json_list[1].append(ride_dict)

    return json_list

def to_utc(state, datetime_obj):
    """
    Takes in unaware python datetime object, converts to tz aware, then 
    converts to UTC.

    """
    # Get timezone of starting state or user's state
    tz = state_to_timezone(state)
    # Localize to timezone of state the ride is leaving from
    datetime_aware = pytz.timezone(tz).localize(datetime_obj)
    # Normalize to UTC in order to search DB
    datetime_utc = pytz.utc.normalize(datetime_aware)

    return datetime_utc

def to_local(state, datetime_obj):
    """
    Convert timestamp from database to local time.
    First converts to tz-aware UTC, then to local time given the rides
    starting state.
    """
    # Use state from database to determine timezone
    tz = state_to_timezone(state)
    # Convert timestamp from db to be aware that it is in utc
    utc = datetime_obj.replace(tzinfo=pytz.utc)
    # Convert start_timestamp attribute to timezone of state
    local = pytz.timezone(tz).normalize(utc)

    return local

def to_time_string(state, datetime_obj):
    """
    Converts python datetime object to a string to be displayed on front end.

    Compares to today's date in order to display "Today" or "Tomorrow".

    Timezone to get today's date is computed using the state the ride departs from.
    """

    tz = state_to_timezone(state)

    today = datetime.now(pytz.timezone(tz)).date()

    if datetime_obj.date() == today:
        datetime_str = "Today, {}".format(datetime_obj.strftime('%-I:%M %p'))

    # If ride is tomorrow, adjust attribute to indicate
    elif datetime_obj.date() == (today + timedelta(days=1)):
        datetime_str = "Tomorrow, {}".format(datetime_obj.strftime('%-I:%M %p'))
    # Otherwise change attribute to formatted timestamp string
    else:
        datetime_str = datetime_obj.strftime('%A, %b %d, %Y %-I:%M %p')

    return datetime_str

def validate_ride(ride):
    attributes = ["driver",
                  "seats",
                  "cost",
                  "start_lat",
                  "start_lng",
                  "start_number",
                  "start_street",
                  "start_city",
                  "start_state",
                  "start_zip",
                  "end_lat",
                  "end_lng",
                  "end_number",
                  "end_street",
                  "end_city",
                  "end_state",
                  "end_zip",
                  "start_timestamp",
                  "mileage",
                  "duration",
                  "luggage",
                  "comments",
                  "pickup_window",
                  "detour",
                  "car_type"]

    for attr in attributes:
        if not getattr(ride, attr):
            setattr(ride, attr, None)

    return ride


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