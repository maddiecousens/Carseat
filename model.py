"""Modes and database functions for Rideshare Project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils import ArrowType
from sqlalchemy import cast, Time, Date
import arrow

db = SQLAlchemy()

##############################################################################
# Database Models



class User(db.Model):
    """User of the site. Can be driver (as of now)"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fb_userid = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    photo = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.now())
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s, name = %s, email=%s, password=%s>" % (self.user_id, 
                                            self.first_name, self.email, self.password)

class Ride(db.Model):
    """A specific ride"""

    __tablename__ = "rides"

    ride_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    driver = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False) #look into this datatype

    # Start Location
    start_lat = db.Column(db.Float(24), nullable=False)
    start_lng = db.Column(db.Float(24), nullable=False)
    start_name = db.Column(db.String(200), nullable=True)
    start_number = db.Column(db.String(50), nullable=True)
    start_street = db.Column(db.String(100), nullable=True)
    start_city = db.Column(db.String(50), nullable=False)
    start_state = db.Column(db.String(15), nullable=False) #add validation
    start_zip = db.Column(db.String(10), nullable=True)
    # End Location
    end_lat = db.Column(db.Float(24), nullable=False)
    end_lng = db.Column(db.Float(24), nullable=False)
    end_name = db.Column(db.String(200), nullable=True)
    end_number = db.Column(db.String(50), nullable=True)
    end_street = db.Column(db.String(100), nullable=True)
    end_city = db.Column(db.String(50), nullable=False)
    end_state = db.Column(db.String(15), nullable=False) #add validation
    end_zip = db.Column(db.String(10), nullable=True)

    # Date/Time
    start_timestamp = db.Column(db.DateTime, nullable=False)
    end_timestamp = db.Column(db.DateTime, nullable=False)
   
    
    #Details
    mileage = db.Column(db.String(10), nullable=True)   # would there be a way to validate this? API?
    duration = db.Column(db.String(100), nullable=True)
    luggage = db.Column(db.String(50), nullable=True) #number for now.. drop down js
    comments = db.Column(db.Text, nullable=True) #db.Text field??
    pickup_window = db.Column(db.String(50), nullable=True) 
    detour = db.Column(db.String(50), nullable=True) 
    car_type = db.Column(db.String(100), nullable=True)


    user = db.relationship("User",
                            backref=db.backref("rides_offered"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ride ride_id={}, driver={}, start={}, end={}, date={}>".format(self.ride_id, 
            self.driver, self.start_city, self.end_city, self.start_timestamp)


    @classmethod
    def get_rides(cls, **kwargs):
        """Get rides depending on varying search parameters"""


        q = cls.query.options(db.joinedload('user'))

        if kwargs.get('start_lat'):
            deg = float(kwargs.get('deg'))
            start_lat = float(kwargs.get('start_lat'))
            start_lng = float(kwargs.get('start_lng'))

            q = q.filter(
                        ( (cls.start_lat < str(start_lat + deg)) &
                          (cls.start_lat > str(start_lat - deg))
                        ) &
                        ( (cls.start_lng < str(start_lng + deg)) &
                          (cls.start_lng > str(start_lng - deg))
                        ))

        if kwargs.get('end_lat'):
            deg = float(kwargs.get('deg'))
            end_lat = float(kwargs.get('end_lat'))
            end_lng = float(kwargs.get('end_lng'))
            q = q.filter(
                        ( (cls.end_lat < str(end_lat + deg)) &
                          (cls.end_lat > str(end_lat - deg))
                        ) &
                        ( (cls.end_lng < str(end_lng + deg)) &
                          (cls.end_lng > str(end_lng - deg))
                        ))


        if kwargs.get('date_from'):
            date_from = kwargs.get('date_from')

            q = q.filter((cast(cls.start_timestamp, Date) >= date_from))

        if kwargs.get('date_to'):
            date_to = kwargs.get('date_to')
            
            q = q.filter((cast(cls.start_timestamp, Date) <= date_to))

        if kwargs.get('start_time'):
            start_time = kwargs.get('start_time')
            q = q.filter(cast(cls.start_timestamp, Time) >= start_time)

        if kwargs.get('cost'):
            cost = int(kwargs.get('cost'))
            q = q.filter(cls.cost < cost)

        # q = q.order_by(cls.start_timestamp)

        if kwargs.get('order_by') == 'date':
            q = q.order_by(cls.start_timestamp)

        if kwargs.get('order_by') == 'time':
            q = q.order_by(cast(cls.start_timestamp, Time))

        if kwargs.get('order_by') == 'cost':
            q = q.order_by(cls.cost)


        if kwargs.get('limit'):
            limit_number = int(kwargs.get('limit'))
            q = q.limit(limit_number)

        if kwargs.get('offset'):
            offset_number = int(kwargs.get('offset'))
            q = q.offset(offset_number)

        if kwargs.get('count'):
            rides = q.count()
        else:
            rides = q.all()
        print '\n\n{}\n\n'.format(rides)

        return rides
        

class Rider(db.Model):
    """Association table. Users taking Rides"""

    __tablename__ = "riders"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("rides_taking"))

    ride = db.relationship("Ride",
                            backref=db.backref("riders"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rider id={}, ride_id={}, user_id={}>".format(self.id, 
            self.ride_id, self.user_id)


class Request(db.Model):
    """Requests for rides"""

    __tablename__ = "requests"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    requester = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)


    ride = db.relationship("Ride",
                            backref=db.backref("requests"))

    user = db.relationship("User",
                            backref=db.backref("requests"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Requests id={}, ride_id={}, requester={}, seats={}>".format(self.id, 
            self.ride_id, self.requester, self.seats)


##############################################################################
# Helper Functions

def connect_db(app):
    """Connect db to Flask app"""

    # Configure connection to PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rideshare'
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_db(app)
    print "Connected to Database"